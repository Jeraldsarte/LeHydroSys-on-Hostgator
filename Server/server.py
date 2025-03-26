from flask import Flask, request, jsonify
import pymysql  # Use pymysql instead of mysql.connector for HostGator
import os
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load Database Configuration from Environment Variables (or manually define them)
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "your_hostgator_db_host"),
    "user": os.getenv("MYSQL_USER", "your_hostgator_username"),
    "password": os.getenv("MYSQL_PASSWORD", "your_hostgator_password"),
    "database": os.getenv("MYSQL_DATABASE", "your_hostgator_database"),
}

# Function to create a new database connection
def connect_db():
    while True:
        try:
            db = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)  # DictCursor for dictionary response
            return db
        except pymysql.MySQLError as err:
            print(f"🔴 Database Connection Error: {err}. Retrying in 5s...")
            time.sleep(5)

# 📌 Fetch Sensor Data with Date Filtering (for Graphs)
@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    try:
        db = connect_db()
        cursor = db.cursor()

        # Get date range from request parameters
        start_date = request.args.get('start_date', None)  # e.g., "2025-03-26"
        end_date = request.args.get('end_date', None)      # e.g., "2025-03-27"

        query = "SELECT * FROM sensor_data WHERE 1"  # Base query

        params = []
        if start_date:
            query += " AND timestamp >= %s"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= %s"
            params.append(end_date)

        query += " ORDER BY timestamp DESC"

        cursor.execute(query, tuple(params))
        data = cursor.fetchall()

        cursor.close()
        db.close()

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {e}"}), 500

# 📌 Health Check API
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "database": "connected"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # For local testing only
