from flask import Blueprint, jsonify, render_template #type:ignore
from sqlalchemy import inspect
from app.utils import db

tables_bp = Blueprint('table', __name__)

@tables_bp.route('/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    # Dynamically load the table model using the table name
    table = db.Model.metadata.tables.get(table_name)
    
    # if not table:
    #     return jsonify({"error": f"Table '{table_name}' not found"}), 404

    # Execute a query to get all rows from the table
    try:
        data = db.session.query(table).all()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Get column names from the table
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]

    # Prepare data for rendering
    data_values = [{col: getattr(row, col) for col in columns} for row in data]

    # Render data to HTML
    return render_template('admin.html', columns=columns, data_values=data_values)
