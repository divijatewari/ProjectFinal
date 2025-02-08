Python 3.13.1 (tags/v3.13.1:0671451, Dec  3 2024, 19:06:28) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from flask import Flask, request, jsonify
... from datetime import datetime
... import sqlite3
... import os
... 
... app = Flask(name)
... 
... db_path = 'metro.db'
... 
... # Ensure the database exists
... if not os.path.exists(db_path):
...     open(db_path, 'w').close()
... 
... # Initialize the database
... def init_db():
...     try:
...         conn = sqlite3.connect(db_path, check_same_thread=False)
...         cursor = conn.cursor()
...         cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
...                             id INTEGER PRIMARY KEY AUTOINCREMENT,
...                             name TEXT,
...                             gender TEXT,
...                             from_station TEXT,
...                             to_station TEXT,
...                             coach TEXT,
...                             emergency BOOLEAN,
...                             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
...         conn.commit()
...     except sqlite3.Error as e:
...         print(f"Database error: {e}")
...     finally:
...         conn.close()
... 
... init_db()
... 
... @app.route('/book', methods=['POST'])
... def book_ticket():
    try:
        data = request.json
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO bookings (name, gender, from_station, to_station, coach, emergency)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (data['name'], data['gender'], data['from_station'], data['to_station'], data['coach'], data['emergency']))
        conn.commit()
        return jsonify({'message': 'Booking successful'})
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {e}'})
    finally:
        conn.close()

@app.route('/next_metro', methods=['GET'])
def get_next_metro():
    now = datetime.now().strftime('%H:%M:%S')
    return jsonify({'next_metro': now})

@app.route('/bookings', methods=['GET'])
def get_bookings():
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bookings')
        bookings = cursor.fetchall()
        return jsonify({'bookings': bookings})
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {e}'})
    finally:
        conn.close()

@app.route('/delete_booking/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        conn.commit()
        return jsonify({'message': 'Booking deleted'})
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {e}'})
    finally:
        conn.close()

if name == 'main':
    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=5000)
    except Exception as e:
