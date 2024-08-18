from flask import Blueprint, render_template, redirect, url_for # type: ignore
from app.utils import db
from app.models import *

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_home():
    return render_template('admin.html')

@admin_bp.route('/create_tables')
def create_tables():
    db.create_all()
    return redirect(url_for('admin.admin_home'))
    # with current_app.app_context():  # Ensure we're in the app context
    #     db.create_all()
    # return redirect(url_for('admin.admin_home'))



