# route/admin.py
from flask import Blueprint, render_template, redirect, url_for # type: ignore
from app.utils import db
from app.models import *
from app.scraping import season_start

# Blueprint
admin_bp = Blueprint('admin', __name__)

# ROUTES
@admin_bp.route('/admin')
def admin_home():
    # return html with season start variable to help instantiate the pls_table with the required team list.
    return render_template('admin.html', season_start=season_start)

@admin_bp.route('/create_tables')
def create_tables():
    db.create_all()
    return redirect(url_for('admin.admin_home'))
  



