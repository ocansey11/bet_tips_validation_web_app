# models.py
from app.utils import db
from sqlalchemy import PrimaryKeyConstraint

class CompletedMatches(db.Model):
    __tablename__ = 'completed_matches'
    home = db.Column(db.Integer, primary_key=True)
    away = db.Column(db.Integer, primary_key=True)
    date_and_time = db.Column(db.String(20), primary_key=True)
    home_win_probability = db.Column(db.Float)
    draw_probability = db.Column(db.Float)
    away_win_probability = db.Column(db.Float)
    team_to_win_prediction = db.Column(db.Integer)
    average_goals_prediction = db.Column(db.Float)
    weather_in_degrees = db.Column(db.String(5))
    odds = db.Column(db.Float)
    full_time_score = db.Column(db.String(10))
    score_at_halftime = db.Column(db.String(10))
    date = db.Column(db.DateTime)
    time = db.Column(db.Time)
    home_team_score_prediction = db.Column(db.Integer)
    away_team_score_prediction = db.Column(db.Integer)
    home_team_full_time_score = db.Column(db.Integer)
    away_team_full_time_score = db.Column(db.Integer)
    home_team_halftime_score = db.Column(db.Integer)
    away_team_halftime_score = db.Column(db.Integer)
    prediction_result = db.Column(db.Integer)
    day_of_week = db.Column(db.Integer)
    month = db.Column(db.Integer)
    weekly_round = db.Column(db.Integer)
    
    __table_args__ = (
        PrimaryKeyConstraint('home', 'away', 'date_and_time'),
    )
   


class UpcomingMatches(db.Model):
    __tablename__ = 'upcoming_matches'
    home = db.Column(db.Integer, primary_key=True)
    away = db.Column(db.Integer, primary_key=True)
    date_and_time = db.Column(db.String(20), primary_key=True)
    home_win_probability = db.Column(db.Float)
    draw_probability = db.Column(db.Float)
    away_win_probability = db.Column(db.Float)
    team_to_win_prediction = db.Column(db.Integer)
    scoreline_prediction = db.Column(db.String(10))
    average_goals_prediction = db.Column(db.Float)    
    weather_in_degrees = db.Column(db.String(5))
    odds = db.Column(db.Float)
    date = db.Column(db.DateTime)
    time = db.Column(db.Time)
    home_team_score_prediction = db.Column(db.Integer)
    away_team_score_prediction = db.Column(db.Integer)
    day_of_week = db.Column(db.Integer)
    month = db.Column(db.Integer)
    weekly_round = db.Column(db.Integer)

    __table_args__ = (
        PrimaryKeyConstraint('home', 'away', 'date_and_time'),
    )
   


class CurrentWeekLeagueStandings(db.Model):
    __tablename__ = 'current_week_league_standings'
    pos = db.Column(db.Integer,primary_key=True)
    team = db.Column(db.Integer)
    pld = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    gf = db.Column(db.Integer)
    ga = db.Column(db.Integer)
    last_5_matches = db.Column(db.String(6))
    ppg_last_5_matches = db.Column(db.Float)
    points = db.Column(db.Integer)


class PreviousWeekLeagueStandings(db.Model):
    __tablename__ = 'previous_week_league_standings'
    pos = db.Column(db.Integer,primary_key=True)
    team = db.Column(db.Integer)
    pld = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    gf = db.Column(db.Integer)
    ga = db.Column(db.Integer)
    last_5_matches = db.Column(db.String(6))
    ppg_last_5_matches = db.Column(db.Float)
    points = db.Column(db.Integer)


class TestingData(db.Model):
    __tablename__ = 'testing_data'
    home = db.Column(db.Integer, primary_key=True)
    away = db.Column(db.Integer, primary_key=True)
    date_and_time = db.Column(db.String(20), primary_key=True)
    home_win_probability = db.Column(db.Float)
    draw_probability = db.Column(db.Float)
    away_win_probability = db.Column(db.Float)
    team_to_win_prediction = db.Column(db.Integer)
    scoreline_prediction = db.Column(db.String(10))
    average_goals_prediction = db.Column(db.Float)
    weather_in_degrees = db.Column(db.String(5))
    odds = db.Column(db.Float)
    date = db.Column(db.DateTime)
    time = db.Column(db.Time)
    home_team_score_prediction = db.Column(db.Integer)
    away_team_score_prediction = db.Column(db.Integer)
    day_of_week = db.Column(db.Integer)
    month = db.Column(db.Integer)
    weekly_round = db.Column(db.Integer)
    home_team_pos = db.Column(db.Integer)
    home_team_matches_played = db.Column(db.Integer)
    home_team_wins = db.Column(db.Integer)
    home_team_draws = db.Column(db.Integer)
    home_team_losses = db.Column(db.Integer)
    home_team_gf = db.Column(db.Integer)
    home_team_ga = db.Column(db.Integer)
    home_team_ppg_last_5_matches = db.Column(db.Float)
    home_team_points = db.Column(db.Integer)
    away_team_pos = db.Column(db.Integer)
    away_team_matches_played = db.Column(db.Integer)
    away_team_wins = db.Column(db.Integer)
    away_team_draws = db.Column(db.Integer)
    away_team_losses = db.Column(db.Integer)
    away_team_gf = db.Column(db.Integer)
    away_team_ga = db.Column(db.Integer)
    away_team_ppg_last_5_matches = db.Column(db.Float)
    away_team_points = db.Column(db.Integer)

    __table_args__ = (
        PrimaryKeyConstraint('home', 'away', 'date_and_time'),
    )


class TrainingData(db.Model):
    __tablename__ = 'training_data'
    home = db.Column(db.Integer, primary_key=True)
    away = db.Column(db.Integer, primary_key=True)
    date_and_time = db.Column(db.String(20), primary_key=True)
    home_win_probability = db.Column(db.Float)
    draw_probability = db.Column(db.Float)
    away_win_probability = db.Column(db.Float)
    team_to_win_prediction = db.Column(db.Integer)
    average_goals_prediction = db.Column(db.Float)
    weather_in_degrees = db.Column(db.String(5))
    odds = db.Column(db.Float)
    full_time_score = db.Column(db.String(10))
    score_at_halftime = db.Column(db.String(10))
    date = db.Column(db.DateTime)
    time = db.Column(db.Time)
    home_team_score_prediction = db.Column(db.Integer)
    away_team_score_prediction = db.Column(db.Integer)
    home_team_full_time_score = db.Column(db.Integer)
    away_team_full_time_score = db.Column(db.Integer)
    home_team_halftime_score = db.Column(db.Integer)
    away_team_halftime_score = db.Column(db.Integer)
    prediction_result = db.Column(db.Integer)
    day_of_week = db.Column(db.Integer)
    month = db.Column(db.Integer)
    weekly_round = db.Column(db.Integer)
    home_team_pos = db.Column(db.Integer)
    home_team_matches_played = db.Column(db.Integer)
    home_team_wins = db.Column(db.Integer)
    home_team_draws = db.Column(db.Integer)
    home_team_losses = db.Column(db.Integer)
    home_team_gf = db.Column(db.Integer)
    home_team_ga = db.Column(db.Integer)
    home_team_ppg_last_5_matches = db.Column(db.Float)
    home_team_points = db.Column(db.Integer)
    away_team_pos = db.Column(db.Integer)
    away_team_matches_played = db.Column(db.Integer)
    away_team_wins = db.Column(db.Integer)
    away_team_draws = db.Column(db.Integer)
    away_team_losses = db.Column(db.Integer)
    away_team_gf = db.Column(db.Integer)
    away_team_ga = db.Column(db.Integer)
    away_team_ppg_last_5_matches = db.Column(db.Float)
    away_team_points = db.Column(db.Integer)

    __table_args__ = (
        PrimaryKeyConstraint('home', 'away', 'date_and_time'),
    )

