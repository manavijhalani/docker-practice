from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="111.125.208.38",
    database="pomodoro",
    user="postgres",
    password="12345",
    port="5432"
)
cursor = conn.cursor()

# Ensure table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id SERIAL PRIMARY KEY,
        event_name VARCHAR(255),
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        description TEXT
    )
""")
conn.commit()

@app.route('/eventdetails', methods=['POST', 'GET'])
def handle_events():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        try:
            start_time = datetime.fromisoformat(data['startDate'])
            end_time = datetime.fromisoformat(data['endDate'])

            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO events (event_name, start_time, end_time, description) VALUES (%s, %s, %s, %s)",
                    (data['title'], start_time, end_time, data['description'])
                )
                conn.commit()
            
            return jsonify({"message": "Event added successfully", "event": data}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'GET':
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        
        events_list = [
            {
                'id': event[0],
                'event_name': event[1],
                'start_time': event[2].isoformat(),
                'end_time': event[3].isoformat(),
                'description': event[4]
            }
            for event in events
        ]
        return jsonify({"events": events_list}), 200  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)