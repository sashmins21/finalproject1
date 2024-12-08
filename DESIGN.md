Design Goals
1. User-Friendly Interface: The application was designed with simplicity in mind, allowing users to interact with data without requiring technical knowledge.
2. Dynamic Data Fetching: Stats and headshots are fetched dynamically from external APIs to ensure up-to-date information.
3. Responsive Design: CSS styling ensures compatibility across devices, providing a seamless experience on both desktop and mobile.

Key Routes
1. /: Serves the main interface for fetching player stats.
2. /get_stats: Handles API calls to fetch player-specific stats and prepares data for frontend rendering.
3. /run-script: Executes the shot_chart.py script to generate heatmaps.
4. /leaderboard: Displays top player stats in various categories in the 'leaderboard.html' interface.

API Integration: The application integrates with the NBA API to fetch real-time player statistics and headshots. The requests library is used for making HTTP requests.

The backend processes raw data into meaningful formats:
- Pandas is used for handling and transforming tabular data efficiently.
- Rankings are calculated for numeric fields using the rank method, ensuring users can compare player performance easily.
- Non-essential fields like PLAYER_ID, RANK, and TEAM_ID are filtered out before sending data to the frontend.

The frontend is built with a combination of HTML templates, Bootstrap, and custom CSS for styling, with JavaScript handling dynamic interactions.

Custom CSS enhances the aesthetics and responsiveness of the application:
- Theming: Colors and fonts are selected to align with professional sports branding.
- Responsive Design: Bootstrap ensures the layout adapts to various screen sizes.
- Animations: Progress bars animate using @keyframes, providing a visual representation of player rankings.
  
JavaScript is used to fetch data from the backend and dynamically update the UI:
- Dynamic Headshots: Player headshots are retrieved from the NBA’s public URLs and displayed only after a successful data fetch.
- Progress Bars: Player rankings are visualized using animated progress bars, styled with gradients for better clarity.
- Error Handling: Alerts notify users when data is unavailable or an invalid player name is entered.

The shot_chart.py script generates shot charts using matplotlib. This was chosen for its powerful visualization capabilities and ability to customize the chart aesthetics.
- Accepts a player name as inputs.
- Fetches player shooting data.
- Plots shooting percentages across different areas of the court, visualized as a heatmap.
