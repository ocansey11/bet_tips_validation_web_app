# routes/complete_matches.py
from flask import Blueprint, jsonify # type: ignore
from app.scraping import cm_scrapper, um_scrapper, url_forebet, forebet_className,user,password,host,port,dbname

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/completed', methods=['GET'])
def completed():
    try:
        cm_scrapper(url_forebet,forebet_className,user,password,host,port,dbname)
        return jsonify({'message': 'Scraping completed and data stored successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/upcoming', methods=['GET'])
def upcoming():
    try:
        um_scrapper(url_forebet,forebet_className,user,password,host,port,dbname)
        return jsonify({'message': 'Scraping completed and data stored successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


    