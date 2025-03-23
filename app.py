from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import json

app = Flask(__name__, static_folder='static')

# Database Connection (For locations only)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="UniversityNavigation"
    )

# Fetch all locations
@app.route('/locations', methods=['GET'])
def get_locations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM locations")
    locations = cursor.fetchall()
    conn.close()
    return jsonify(locations)

# Load directions from JSON file
def load_directions():
    with open("directions.json", "r") as file:
        return json.load(file)

# API to get text-based directions
@app.route('/directions', methods=['GET'])
def get_directions():
    start_id = request.args.get('start')
    end_id = request.args.get('end')

    directions_data = load_directions()
    route_key = f"{start_id}-{end_id}"

    if route_key in directions_data:
        return jsonify({"directions": directions_data[route_key]})
    else:
        return jsonify({"error": "No predefined directions found for this route"}), 404

# Serve Frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)