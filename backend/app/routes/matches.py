# routes/matches.py (completed & upcoming)
from flask import Blueprint, jsonify, render_template, redirect, url_for # type: ignore
from app.scraping import cm_scrapper, um_scrapper, url_forebet, forebet_className,user,password,host,port,dbname, team_labels_forebet

# Blueprint
matches_bp = Blueprint('matches', __name__)


# ROUTES
@matches_bp.route('/completed', methods=['GET'])
def completed():
    try:
        cm_scrapper(url_forebet,forebet_className,user,password,host,port,dbname,team_labels_forebet)
        return redirect(url_for('admin.admin_home'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/upcoming', methods=['GET'])
def upcoming():
    try:
        um_scrapper(url_forebet,forebet_className,user,password,host,port,dbname,team_labels_forebet)
        return redirect(url_for('admin.admin_home'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


    