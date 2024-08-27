# routes/matches.py (completed & upcoming)
from flask import Blueprint, jsonify, render_template, redirect, url_for # type: ignore
from app.processing import merge_tables
from app.utils import get_mysql_engine, execute_sql, CREATE_VIEW_TRAIN_DATA, INSERT_VIEW_TRAIN_DATA
from app.scraping import user,password,host,port,dbname
from app.utils import db

# Blueprint
training_bp = Blueprint('training', __name__)


# ROUTES
@training_bp.route('/training', methods=['GET'])
def training():
    try:
        merge_tables( user, password, host, port, dbname, CREATE_VIEW_TRAIN_DATA,INSERT_VIEW_TRAIN_DATA, get_engine=get_mysql_engine, execute_engine=execute_sql)
        return redirect(url_for('admin.admin_home'))
    except Exception as e:
        # Handle exceptions
        db.session.rollback()  # Rollback transaction in case of error
        raise
    finally:
        db.session.close() 

 