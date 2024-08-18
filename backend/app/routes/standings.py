# routes/upcoming_matches.py
from flask import Blueprint, jsonify # type: ignore
from app.scraping import standings_scrapper, cls_table_name, pls_table_name, url_sofascore,sofascore_className, user,password,host,port,dbname, team_labels_sofascore 

standings_bp = Blueprint('standings', __name__)

@standings_bp.route('/previous', methods=['GET'])
def previous():
    try:
        standings_scrapper(pls_table_name,url_sofascore,sofascore_className, user,password,host,port,dbname,team_labels_sofascore )
        return jsonify({'message': 'Scraping completed and data stored successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@standings_bp.route('/current', methods=['GET'])
def current():
    try:
        standings_scrapper(cls_table_name,url_sofascore,sofascore_className,user,password,host,port,dbname,team_labels_sofascore)
        return jsonify({'message': 'Scraping completed and data stored successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    