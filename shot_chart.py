import sys

import numpy as np
import pandas as pd

# nba_api
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats

# matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
import matplotlib.colors as mcolors


# get_player_shotchartdetail: player_name, season_id -> player_shotchart_df, league_avg
def get_player_shotchartdetail(player_name, season_id):
    # Fetch players from the NBA API
    nba_players = players.get_players()
    print(f"Number of players fetched: {len(nba_players)}")  # Debugging

    # Perform a case-insensitive search for the player
    player_dict = next((player for player in nba_players if player['full_name'].lower() == player_name.lower()), None)
    
    # Handle the case where the player is not found
    if not player_dict:
        raise ValueError(f"Player '{player_name}' not found in the NBA player database. Check for typos or formatting.")

    # Fetch career stats for the player
    career = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    career_df = career.get_data_frames()[0]

    # Get the team ID for the given season
    team_id = career_df.loc[career_df['SEASON_ID'] == season_id, 'TEAM_ID']
    if team_id.empty:
        raise ValueError(f"No team found for player '{player_name}' in season '{season_id}'.")

    # Fetch shot chart details
    shotchartlist = shotchartdetail.ShotChartDetail(
        team_id=int(team_id),
        player_id=int(player_dict['id']),
        season_type_all_star='Regular Season',
        season_nullable=season_id,
        context_measure_simple="FGA"
    ).get_data_frames()

    return shotchartlist[0], shotchartlist[1]




# draw court function
def draw_court(ax=None, color="blue", lw=1, outer_lines=False):

    if ax is None:
        ax = plt.gca()

    # Basketball Hoop
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # outer box
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # inner box
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Free Throw Top Arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)

    # Free Bottom Top Arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)

    # Restricted Zone
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three Point Line
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    # list of court shapes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc]

    #outer_lines=True
    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)


# Shot Chart Function
def shot_chart(data, title="", color="b", xlim=(-250, 250), ylim=(422.5, -47.5), line_color="blue",
               court_color="white", court_lw=2, outer_lines=False,
               flip_court=False, gridsize=30,
               ax=None, despine=False):

    if ax is None:
        ax = plt.gca()

    if not flip_court:
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else:
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom="off", labelleft="off")
    ax.set_title(title, fontsize=18)

    # Draw the court using the draw_court function
    draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)

    # Separate the x and y coordinates of the shots
    x = data['LOC_X']
    y = data['LOC_Y']

    # Use a logarithmic normalization to make the scale more dynamic
    norm = mcolors.LogNorm(vmin=1, vmax=data.shape[0] // 5)  # Adjust vmax for desired contrast

    # Create a hexbin heatmap with logarithmic normalization
    hb = ax.hexbin(x, y, gridsize=gridsize, extent=(xlim[0], xlim[1], ylim[1], ylim[0]),
                   cmap='Reds', mincnt=1, norm=norm)

    # Add a colorbar for the heatmap
    cb = plt.colorbar(hb, ax=ax, shrink=0.6)
    cb.set_label("Frequency of Shots")

    # Set the spines to match the rest of court lines
    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    return ax



if __name__ == "__main__":

    # Accept 2 arguments
    ## First argument is the player name
    ## Second argument is the season id

    player_name = sys.argv[1]
    season_id = sys.argv[2]

    # title
    title = player_name + " Shot Chart " + season_id

    # Get Shotchart Data using nba_api
    player_shotchart_df, league_avg = get_player_shotchartdetail(player_name, season_id)

    # Draw Court and plot Shot Chart
    shot_chart(player_shotchart_df, title=title)
    # Set the size for our plots
    plt.rcParams['figure.figsize'] = (12, 11)
    plt.show()