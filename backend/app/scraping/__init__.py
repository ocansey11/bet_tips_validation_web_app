from .completed_matches import main as cm_scrapper
from .upcoming_matches import main as um_scrapper
from .league_standings import main as standings_scrapper
url_forebet = 'https://www.forebet.com/en/football-tips-and-predictions-for-england/premier-league'
url_sofascore = 'https://www.sofascore.com/tournament/football/england/premier-league/17#id:61627'
# CLASSNAMES
sofascore_className = "eHXJll"
forebet_className = "schema"

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
        'Brighton': 4,
        'Burnley': 5,
        'Chelsea': 6,
        'Crystal Palace': 7,
        'Everton': 8,
        'Fulham': 9,
        'Ipswich Town':10,
        'Leeds United': 11,
        'Leicester City': 12,
        'Liverpool': 13,
        'Manchester City': 14,
        'Manchester United': 15,
        'Newcastle United': 16,
        'Norwich City': 17,
        'Sheffield United': 18,
        'Southampton': 19,
        'Tottenham': 20,
        'West Ham': 21,
        'Luton Town': 22,
        'Wolverhampton': 23,
        'Brentford': 24,
        'Sheffield United': 25,
        'Nottingham Forest': 26
    }

team_labels_sofascore = {
        'Arsenal': 1,
        'Aston Villa': 2,
        'Bournemouth': 3,
        'Brighton': 4,
        'Burnley': 5,
        'Chelsea': 6,
        'Crystal Palace': 7,
        'Everton': 8,
        'Fulham': 9,
        'Ipswich': 10,
        'Leeds Utd': 11,
        'Leicester City': 12,
        'Liverpool': 13,
        'Man City': 14,
        'Man Utd': 15,
        'Newcastle': 16,
        'Norwich': 17,
        'Sheffield': 18,
        'Southampton': 19,
        'Tottenham': 20,
        'West Ham': 21,
        'Luton': 22,
        'Wolves': 23,
        'Brentford': 24,
        'Sheffield Utd': 25,
        'Forest': 26
    }

# Team List 2024/2025 Premier League Season
teams_list = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Burnley",
    "Chelsea", "Cristal Palace", "Everton", "Fulham", "Ipswich", "Leicester City",
    "Liverpool", "Man City", "Man Utd", "Newcastle", "Southampton", "Tottenham",
    "West Ham", "Wolves"
    ]
season_start = False