# utils/sql_utils.py

from sqlalchemy import text
from sqlalchemy import create_engine

def get_mysql_engine(user, password, host, port, database):
    """
    Create a MySQL engine. If the password is None or an empty string, it omits it from the connection string.
    """
    if password:
        connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    else:
        connection_string = f'mysql+pymysql://{user}@{host}:{port}/{database}'
    
    return create_engine(connection_string)



def execute_sql(engine, sql_script):
    """
    Execute the provided SQL script.
    """
    with engine.connect() as connection:
        connection.execute(text(sql_script))

        
# These scripts are for merging pairs of data. However over time, i will have csv files from these processes. Hence Training and testing data will be appended by just downloading and importing these csv files. 



# SQL CODES CREATING THE VIEWS
CREATE_VIEW_TRAIN_DATA = """
CREATE VIEW combined_train_data AS
SELECT 
    cm.*,
    h.pos AS home_team_pos,
    h.pld AS home_team_matches_played,
    h.wins AS home_team_wins,
    h.draws AS home_team_draws,
    h.losses AS home_team_losses,
    h.gf AS home_team_gf,
    h.ga AS home_team_ga,
    h.ppg_last_5_matches AS home_team_ppg_last_5_matches,
    h.points AS home_team_points,
    a.pos AS away_team_pos,
    a.pld AS away_team_matches_played,
    a.wins AS away_team_wins,
    a.draws AS away_team_draws,
    a.losses AS away_team_losses,
    a.gf AS away_team_gf,
    a.ga AS away_team_ga,
    a.ppg_last_5_matches AS away_team_ppg_last_5_matches,
    a.points AS away_team_points
    FROM 
    completed_matches cm
    LEFT JOIN 
    previous_week_league_standings AS h ON cm.home = h.team
    LEFT JOIN 
    previous_week_league_standings AS a ON cm.away = a.team;
"""

CREATE_VIEW_TEST_DATA  = """
CREATE VIEW combined_test_data AS
SELECT 
	um.*,
    home_team.pos AS home_team_pos,
    home_team.pld AS home_team_matches_played,
    home_team.wins AS home_team_wins,
    home_team.draws AS home_team_draws,
    home_team.losses AS home_team_losses,
    home_team.gf AS home_team_gf,
    home_team.ga AS home_team_ga,
    home_team.ppg_Last_5_Matches AS home_team_ppg_last_5_matches,
    home_team.points AS home_team_points,
    away_team.pos AS away_team_pos,
    away_team.pld AS away_team_matches_played,
    away_team.wins AS awaycurrent_week_league_standings_team_wins,
    away_team.draws AS away_team_draws,
    away_team.losses AS away_team_losses,
    away_team.gf AS away_team_gf,
    away_team.ga AS away_team_ga,
    away_team.ppg_Last_5_Matches AS away_team_ppg_last_5_matches,
    away_team.points AS away_team_points
FROM 
    upcoming_matches um
INNER JOIN 
    current_week_league_standings home_team ON um.home = home_team.team
INNER JOIN 
    current_week_league_standings away_team ON um.away = away_team.team;

"""

# SQL CODES INSERTING NEW DATA THROUGH VIEWS
INSERT_VIEW_TRAIN_DATA = """ 
INSERT INTO training_data (
    home_team_id, away_team_id, date_and_time, home_win_probability, 
    draw_probability, away_win_probability, team_to_win_prediction, 
    average_goals_prediction, weather_in_degrees, odds, full_time_score, 
    score_at_halftime, date, time, home_team_score_prediction, 
    away_team_score_prediction, home_team_full_time_score, 
    away_team_full_time_score, home_team_halftime_score, 
    away_team_halftime_score, prediction_result, day_of_week, 
    month, weekly_round, home_team_pos, home_team_matches_played, 
    home_team_wins, home_team_draws, home_team_losses, home_team_gf, 
    home_team_ga, home_team_ppg_last_5_matches, home_team_points, 
    away_team_pos, away_team_matches_played, away_team_wins, 
    away_team_draws, away_team_losses, away_team_gf, away_team_ga, 
    away_team_ppg_last_5_matches, away_team_points
)
SELECT 
    home_team_id, away_team_id, date_and_time, home_win_probability, 
    draw_probability, away_win_probability, team_to_win_prediction, 
    average_goals_prediction, weather_in_degrees, odds, full_time_score, 
    score_at_halftime, date, time, home_team_score_prediction, 
    away_team_score_prediction, home_team_full_time_score, 
    away_team_full_time_score, home_team_halftime_score, 
    away_team_halftime_score, prediction_result, day_of_week, 
    month, weekly_round, home_team_pos, home_team_matches_played, 
    home_team_wins, home_team_draws, home_team_losses, home_team_gf, 
    home_team_ga, home_team_ppg_last_5_matches, home_team_points, 
    away_team_pos, away_team_matches_played, away_team_wins, 
    away_team_draws, away_team_losses, away_team_gf, away_team_ga, 
    away_team_ppg_last_5_matches, away_team_points
FROM combined_train_data;
"""

INSERT_VIEW_TEST_DATA = """ 
INSERT INTO testing_data SELECT * FROM combined_test_data;
"""

# SQL CODES DROPPING THE VIEWS
DROP_VIEW_COMBINED_TRAIN_DATA = """
DROP VIEW IF EXISTS combined_train_data;
"""

DROP_VIEW_COMBINED_TEST_DATA = """
DROP VIEW IF EXISTS combined_test_data;
"""



# -- CREATE EVENT append_training_data
# -- ON SCHEDULE EVERY 1 WEEK
# -- DO
# -- INSERT INTO training_data
# -- SELECT * FROM combined_train_data;


# -- CREATE EVENT append_testing_data
# -- ON SCHEDULE EVERY 1 WEEK
# -- DO
# -- INSERT INTO testing_data
# -- SELECT * FROM combined_test_data;



# FOR USER WHO ARE COPYING THE ALREADY ACCUMULATED TRAINING AND TESTING DATA FOR DATA ANALYSIS OR ANY OTHER PURPOSES USE THE FOLLOWING OPERATIONS
# THE IDEA IS TO CREATE A TRAINING AND TESTING DATA TABLE IN YOUR DB.
# COPY THE CSV DATA FOR BOTH TESTING AND TRAINING DATA FROM  THE csv DIRECTORY IN THE MAIN BRANCH - I WILL BE UPDATING THESE CSVS' WEEKLY 
# INSERT THE training_data and testing_data CSV data  INTO THE VARIOUS TABLE TO GET A JUMP START TO TRAIN YOUR MODELS OR DO YOUR ANALYSIS

CREATE_TABLE_TRAINING_DATA_FOR_CSV_INSERTION =  """
CREATE TABLE training_data (
    home INT,
    away INT,
    home_win_probability DOUBLE,
    draw_probability DOUBLE,
    away_win_probability DOUBLE,
    team_to_win_prediction INT,
    average_goals_prediction DOUBLE,
    weather_in_degrees TEXT,
    odds DOUBLE,
    full_time_score TEXT,
    score_at_halftime TEXT,
    date DATETIME,
    time TIME,
    home_team_score_prediction INT,
    away_team_score_prediction INT,
    home_team_full_time_score INT,
    away_team_full_time_score INT,
    home_team_halftime_score INT,
    away_team_halftime_score INT,
    prediction_result INT,
    day_of_week INT,
    month INT,
    weekly_round INT,
    home_team_pos INT,
    home_team_matches_played INT,
    home_team_wins INT,
    home_team_draws INT,
    home_team_losses INT,
    home_team_gf INT,
    home_team_ga INT,
    home_team_ppg_last_5_matches DOUBLE,
    home_team_points INT,
    away_team_pos INT,
    away_team_matches_played INT,
    away_team_wins INT,
    away_team_draws INT,
    away_team_losses INT,
    away_team_gf INT,
    away_team_ga INT,
    away_team_ppg_last_5_matches DOUBLE,
    away_team_points INT
);
"""


CREATE_TABLE_TESTING_DATA_FOR_CSV_INSERTION =  """
CREATE TABLE testing_data (
    home INT,
    away INT,
    home_win_probability DOUBLE,
    draw_probability DOUBLE,
    away_win_probability DOUBLE,
    team_to_win_prediction INT,
    scoreline_prediction TEXT,
    average_goals_prediction DOUBLE,
    weather_in_degrees TEXT,
    odds DOUBLE,
    date DATETIME,
    time TIME,
    home_team_score_prediction INT,
    away_team_score_prediction INT,
    day_of_week INT,
    month INT,
    weekly_round INT,
    home_team_pos INT,
    home_team_matches_played INT,
    home_team_wins INT,
    home_team_draws INT,
    home_team_losses INT,
    home_team_gf INT,
    home_team_ga INT,
    home_team_ppg_last_5_matches DOUBLE,
    home_team_points INT,
    away_team_pos INT,
    away_team_matches_played INT,
    away_team_wins INT,
    away_team_draws INT,
    away_team_losses INT,
    away_team_gf INT,
    away_team_ga INT,
    away_team_ppg_last_5_matches DOUBLE,
    away_team_points INT
);

"""