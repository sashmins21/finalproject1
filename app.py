from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
import subprocess

app = Flask(__name__)

# Function to fetch NBA data
# Update get_nba_data to handle PLAYER_ID
def get_nba_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.nba.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data: {response.status_code}")

    data = response.json()
    table_headers = data['resultSet']['headers']
    df = pd.DataFrame(data['resultSet']['rowSet'], columns=table_headers)

    # Ensure PLAYER_ID is included
    if 'PLAYER_ID' not in table_headers:
        raise ValueError("PLAYER_ID not found in data headers.")
    return df


# Calculate ranks for each stat in the DataFrame
def calculate_ranks(df):
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        df[f"{col}_RANK"] = df[col].rank(ascending=False, method='min')
    return df

# Create leaderboard
def create_leaderboard(stat_categories, nba_data):
    leaderboard = {}
    for category in stat_categories:
        if category not in nba_data.columns:
            continue
        nba_data[category] = pd.to_numeric(nba_data[category], errors='coerce')
        sorted_df = nba_data.sort_values(by=category, ascending=False).head(10)
        leaderboard[category] = sorted_df[['PLAYER', category, 'TEAM']]
    return leaderboard

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to run Python script for generating shot chart
@app.route("/run-script", methods=["POST"])
def run_script():
    try:
        data = request.json
        player_name = data.get("player_name")
        result = subprocess.run(
            ["python3", "shot_chart.py", player_name, "2024-25"],  # Adjust season if needed
            capture_output=True,
            text=True
        )
        return jsonify({"success": True, "output": result.stdout})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Route to fetch player stats and ranks
@app.route('/get_stats', methods=['POST'])
def get_stats():
    try:
        # Get player name from request
        data = request.json
        player_name = data.get('playerName')
        if not player_name:
            return jsonify({'error': 'Player name is required.'})

        # Fetch NBA data
        text_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2024-25&SeasonType=Regular%20Season&StatCategory=PTS'
        nba_data = get_nba_data(text_url)

        # Calculate ranks
        nba_data = calculate_ranks(nba_data)

        # Match player (case insensitive)
        player_data = nba_data[nba_data['PLAYER'].str.lower() == player_name.lower()]

        # Handle player not found
        if player_data.empty:
            return jsonify({'error': f'Player {player_name} not found.'})

        # Convert player data to dict and include PLAYER_ID
        stats = player_data.to_dict(orient='records')[0]

        # Convert all values to JSON-serializable types
        stats = {key: (int(value) if isinstance(value, pd.Int64Dtype) else value)
                 for key, value in stats.items()}
        
        # Exclude unnecessary categories
        excluded_categories = {'PLAYER_ID', 'RANK', 'TEAM_ID', 'PLAYER', 'TEAM'}
        filtered_stats = {key: value for key, value in stats.items() if key.upper() not in excluded_categories}
        
        return jsonify(stats)

    except Exception as e:
        return jsonify({'error': str(e)})



# Route for the leaderboard page
@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

# Route to fetch leaderboard data
@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        # NBA API URL
        text_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2024-25&SeasonType=Regular%20Season&StatCategory=PTS'
        nba_data = get_nba_data(text_url)

        # Define stat categories
        stat_categories = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FT_PCT', '3P_PCT']

        # Create leaderboard
        leaderboard = create_leaderboard(stat_categories, nba_data)

        # Convert to JSON
        leaderboard_json = {category: df.to_dict(orient='records') for category, df in leaderboard.items()}
        return jsonify(leaderboard_json)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)