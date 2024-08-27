from .completed_matches import main as cm_scrapper
from .upcoming_matches import main as um_scrapper
from .league_standings import main as standings_scrapper
url_forebet = 'https://www.forebet.com/en/football-tips-and-predictions-for-england/premier-league'
url_sofascore = 'https://www.sofascore.com/tournament/football/england/premier-league/17#id:61627'
# CLASSNAMES
sofascore_className = "eHXJll"
forebet_className = "schema"
weekly_round = 2

# DB INFO
user = "test_user"
password = "password"
host = "localhost"
port = 3306
dbname = "bet_tips_validation_web_app"


# DATABASE VARIABLES FOR STANDINGS
cls_table_name = "current_week_league_standings"
pls_table_name = "previous_week_league_standings"


# TEAM LABELS
team_labels_forebet = {
        'Arsenal': 1,
        'Aston Villa': 2,
        'Bournemouth': 3,
        'Brentford': 4,
        'Brighton': 5,
        'Burnley': 6,
        'Chelsea': 7,
        'Crystal Palace': 8,
        'Everton': 9,
        'Fulham': 10,
        'Ipswich Town':11,
        'Leeds United': 12,
        'Leicester City': 13,
        'Liverpool': 14,
        'Manchester City': 15,
        'Manchester United': 16,
        'Newcastle United': 17,
        'Norwich City': 18,
        'Sheffield United': 19,
        'Southampton': 20,
        'Tottenham': 21,
        'West Ham': 22,
        'Luton Town': 23,
        'Wolverhampton': 24,
        'Sheffield United': 25,
        'Nottingham Forest': 26,
    }

team_labels_sofascore = {
        'Arsenal': 1,
        'Aston Villa': 2,
        'Bournemouth': 3,
        'Brentford': 4,
        'Brighton': 5,
        'Burnley': 6,
        'Chelsea': 7,
        'Crystal Palace': 8,
        'Everton': 9,
        'Fulham': 10,
        'Ipswich': 11,
        'Leeds Utd': 12,
        'Leicester': 13,
        'Liverpool': 14,
        'Man City': 15,
        'Man Utd': 16,
        'Newcastle': 17,
        'Norwich': 18,
        'Sheffield': 19,
        'Southampton': 20,
        'Tottenham': 21,
        'West Ham': 22,
        'Luton': 23,
        'Wolves': 24,
        'Sheffield Utd': 25,
        'Forest': 26
    }

# Team List 2024/2025 Premier League Season
teams_list = [
    1, 2, 3, 4, 5, 7, 8, 9, 10,11,
    13, 14, 15, 16, 17, 20,
    21,22,23,26
    ]

teams_list_labels = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
    "Chelsea", "Cristal Palace", "Everton", "Fulham", "Ipswich", "Leicester",
    "Liverpool", "Man City", "Man Utd", "Newcastle", "Southampton", "Tottenham",
    "West Ham", "Wolves", "Forest"
    ]



season_start = True