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
dbname = "bet_model_testing"

# DATABASE VARIABLES FOR STANDINGS
pls_table_name = "current_week_league_standings"
cls_table_name = "previous_week_league_standings"


