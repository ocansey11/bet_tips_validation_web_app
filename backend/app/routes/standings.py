# routes/standings.py
# Import Libraries and objects
from flask import Blueprint, jsonify,  redirect, url_for # type: ignore
from app.scraping import standings_scrapper, teams_list, cls_table_name, pls_table_name, url_sofascore,sofascore_className, user,password,host,port,dbname, team_labels_sofascore 
from sqlalchemy import create_engine
import pandas as pd # type: ignore

# Blueprint
standings_bp = Blueprint('standings', __name__)


# ROUTES
@standings_bp.route('/previous', methods=['GET'])
def previous():
    try:
        standings_scrapper(pls_table_name,url_sofascore,sofascore_className, user,password,host,port,dbname,team_labels_sofascore )
        return redirect(url_for('admin.admin_home')) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@standings_bp.route('/current', methods=['GET'])
def current():
    try:
        standings_scrapper(cls_table_name,url_sofascore,sofascore_className,user,password,host,port,dbname,team_labels_sofascore)
        return redirect(url_for('admin.admin_home')) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Have more control over league table data
@standings_bp.route('/create_league_standings', methods=['POST'])
def create_initial_table():
    try:
        # Sort and prepare the initial data
        # teams_list.sort()
        initial_data = pd.DataFrame([{'team': team, 'pld': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'gf': 0, 'ga': 0, 'last_5_matches': None, 'ppg_last_5_Matches': 0, 'points': 0} for team in teams_list])    

        ##### NOTE : I need to change this part. I am creating too many engines within the app. I have several engines within the scraping directory for all the various scrappers (main)
        #  Database Connection and Insertion. 
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}')
        initial_data.to_sql(pls_table_name, con=engine, if_exists='replace', index=False)

        # return to /admin
        return redirect(url_for('admin.admin_home')) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500 