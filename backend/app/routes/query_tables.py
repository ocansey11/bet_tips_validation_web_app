from flask import Blueprint, jsonify, render_template #type:ignore
from sqlalchemy import inspect
from app.utils import db
from app.scraping import team_labels_forebet
from sqlalchemy import func, String
# import String #type:ignore


tables_bp = Blueprint('table', __name__)

@tables_bp.route('/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    # Handle if the table is not found or an issue occurs
    try:
        table = db.Model.metadata.tables.get(table_name)  
        if table is None:
            return jsonify({"error": f"Table '{table_name}' not found"}), 404

        # Proceed with your data query or processing
        data = db.session.query(func.cast(table.c.date, String).label('date'),table).all()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Get column names from the table
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]

    # Reversed team labels to map numeric values to team names
    team_labels_reverse = {v: k for k, v in team_labels_forebet.items()}

    # Prepare data for rendering
    data_values = []
    for row in data:
        try:
            # Convert row data into a dictionary of column values
            row_data = {col: getattr(row, col) for col in columns}

            # Map the numeric values in home/away columns
            if 'home' in row_data and 'away' in row_data:
                row_data['home'] = team_labels_reverse.get(row_data['home'], "Unknown Team")
                row_data['away'] = team_labels_reverse.get(row_data['away'], "Unknown Team")

            # Map the numeric values in team column for league standing table
            if 'team' in row_data:
                row_data['team'] = team_labels_reverse.get(row_data['team'], "Unknown Team")
            
            # Append the processed row data to the final list
            data_values.append(row_data)
        
        except Exception as e:
            # Return the error and the row_data that caused it
            return jsonify({"error": str(e), "problematic_row": row_data}), 500

    # Render data to HTML
    return render_template('admin.html', columns=columns, data_values=data_values)
