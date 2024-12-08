  This project entails of a website that runs through Flask which allows users to view NBA player statistics, generate heatmaps for players based on their performances, and access leaderboards for various categories. Requirements to run this website are as follows: Python 3.7 or later, Flask, pandas, requests, matplotlib, and a modern web browser.

  To view player statistics, navigate to the homepage by running the python file 'app.py' and clicking the link in the terminal (http://127.0.0:5000), enter an NBA player's name (e.g. "LeBron James" or "lebron james" or "LEBRON JAMES") -- not case sensitive --, and click the "Get Stats" button to show their headshot and stats, which are visualized in a carousel for individual metrics that users can click through on the left and ride side of the stat text. Animated progress bars also appear below that indicate player rankings and percentile across the league for each stat category.

  To generate a heatmap for a player, once a valid name is entered, the "Generate Shot Chart" will appear at the bottom of the page and click it to see their shooting accuracy across the court for the 2024-25 NBA season. A window will pop up and to close the shot chart, exit out of the window through the top left button. The shot_chart.py script is called for this, which uses matplotlib to create the heatmap.

  "View Leaderboard" button at the top of the page will show the top 10 players across categories like points, assists, rebounds, and more when you click either the left or right side of the container. Data is dynamically fetched from the NBA's stats API. To return to the homepage, click the "Go Back" button.

  Dynamic player headshots are displayed upon searching for a player. They are only displayed when stats are successfully fetched.
