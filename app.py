import sqlite3
import sys
from flask import Flask, jsonify, request, send_from_directory

if sys.version_info < (3, 7):
    print("Error: Python 3.7 or higher is required")
    sys.exit(1)

app = Flask(__name__, static_folder='static')

CURRENT_USER_ID = 1
DB_FILE = 'database.db'

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def promote_from_waitlist(event_id, db):
    """Promote the next person from waitlist to confirmed"""
    cursor = db.cursor()

    cursor.execute('''
        SELECT user_id
        FROM rsvps
        WHERE event_id = ? AND status = 'waitlisted'
        LIMIT 1
    ''', (event_id,))

    next_person = cursor.fetchone()
    if next_person:
        cursor.execute('''
            UPDATE rsvps
            SET status = 'confirmed'
            WHERE user_id = ? AND event_id = ?
        ''', (next_person['user_id'], event_id))
        db.commit()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/event.html')
def event_page():
    return send_from_directory('static', 'event.html')

@app.route('/api/me', methods=['GET'])
def get_current_user():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name FROM users WHERE id = ?', (CURRENT_USER_ID,))
    user = cursor.fetchone()
    db.close()
    return jsonify({'name': user['name']})

@app.route('/api/events', methods=['GET'])
def get_events():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
        SELECT
            e.id,
            e.title,
            e.description,
            e.location,
            e.date,
            e.capacity,
            COALESCE(COUNT(CASE WHEN r.status = 'confirmed' THEN 1 END), 0) as confirmed_count,
            (SELECT status FROM rsvps WHERE event_id = e.id AND user_id = ?) as user_rsvp
        FROM events e
        LEFT JOIN rsvps r ON e.id = r.event_id
        GROUP BY e.id
        ORDER BY e.date
    ''', (CURRENT_USER_ID,))

    events = []
    for row in cursor.fetchall():
        events.append({
            'id': row['id'],
            'title': row['title'],
            'description': row['description'],
            'location': row['location'],
            'date': row['date'],
            'capacity': row['capacity'],
            'spots_remaining': row['capacity'] - row['confirmed_count'],
            'current_user_rsvp': row['user_rsvp']
        })

    db.close()
    return jsonify(events)

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = cursor.fetchone()

    if not event:
        db.close()
        return jsonify({'error': 'Event not found'}), 404

    cursor.execute('''
        SELECT COUNT(*) as count
        FROM rsvps
        WHERE event_id = ? AND status = 'confirmed'
    ''', (event_id,))
    confirmed_count = cursor.fetchone()['count']

    cursor.execute('''
        SELECT u.name, u.email
        FROM rsvps r
        JOIN users u ON r.user_id = u.id
        WHERE r.event_id = ? AND r.status = 'confirmed'
        ORDER BY r.created_at
    ''', (event_id,))
    attendees = [{'name': row['name'], 'email': row['email']} for row in cursor.fetchall()]

    cursor.execute('''
        SELECT COUNT(*) as count
        FROM rsvps
        WHERE event_id = ? AND status = 'waitlisted'
    ''', (event_id,))
    waitlist_count = cursor.fetchone()['count']

    cursor.execute('''
        SELECT status
        FROM rsvps
        WHERE event_id = ? AND user_id = ?
    ''', (event_id, CURRENT_USER_ID))
    user_rsvp = cursor.fetchone()
    current_user_rsvp = user_rsvp['status'] if user_rsvp else None

    waitlist_position = None
    if current_user_rsvp == 'waitlisted':
        cursor.execute('''
            SELECT COUNT(*) + 1 as position
            FROM rsvps
            WHERE event_id = ? AND status = 'waitlisted' AND created_at < (
                SELECT created_at FROM rsvps WHERE event_id = ? AND user_id = ?
            )
        ''', (event_id, event_id, CURRENT_USER_ID))
        waitlist_position = cursor.fetchone()['position']

    db.close()

    return jsonify({
        'id': event['id'],
        'title': event['title'],
        'description': event['description'],
        'location': event['location'],
        'date': event['date'],
        'capacity': event['capacity'],
        'spots_remaining': event['capacity'] - confirmed_count,
        'attendees': attendees,
        'current_user_rsvp': current_user_rsvp,
        'waitlist_count': waitlist_count,
        'waitlist_position': waitlist_position
    })

@app.route('/api/events/<int:event_id>/rsvp', methods=['POST'])
def rsvp_event(event_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT capacity FROM events WHERE id = ?', (event_id,))
    event = cursor.fetchone()

    if not event:
        db.close()
        return jsonify({'error': 'Event not found'}), 404

    cursor.execute('''
        SELECT COUNT(*) as count
        FROM rsvps
        WHERE event_id = ? AND status = 'confirmed'
    ''', (event_id,))
    confirmed_count = cursor.fetchone()['count']

    if confirmed_count <= event['capacity']:
        cursor.execute('''
            INSERT INTO rsvps (user_id, event_id, status)
            VALUES (?, ?, 'confirmed')
            ON CONFLICT(user_id, event_id)
            DO UPDATE SET status = 'confirmed'
        ''', (CURRENT_USER_ID, event_id))
    else:
        cursor.execute('''
            INSERT INTO rsvps (user_id, event_id, status)
            VALUES (?, ?, 'waitlisted')
            ON CONFLICT(user_id, event_id)
            DO UPDATE SET status = 'waitlisted'
        ''', (CURRENT_USER_ID, event_id))

    db.commit()
    db.close()

    return get_event(event_id)

@app.route('/api/events/<int:event_id>/cancel', methods=['POST'])
def cancel_rsvp(event_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT id FROM events WHERE id = ?', (event_id,))
    if not cursor.fetchone():
        db.close()
        return jsonify({'error': 'Event not found'}), 404

    cursor.execute('''
        UPDATE rsvps
        SET status = 'cancelled'
        WHERE user_id = ? AND event_id = ?
    ''', (CURRENT_USER_ID, event_id))

    db.commit()
    db.close()

    return get_event(event_id)

@app.route('/api/events/<int:event_id>/leave-waitlist', methods=['POST'])
def leave_waitlist(event_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT id FROM events WHERE id = ?', (event_id,))
    if not cursor.fetchone():
        db.close()
        return jsonify({'error': 'Event not found'}), 404

    cursor.execute('''
        UPDATE rsvps
        SET status = 'cancelled'
        WHERE user_id = ? AND event_id = ? AND status = 'waitlisted'
    ''', (CURRENT_USER_ID, event_id))

    db.commit()
    db.close()

    return get_event(event_id)

if __name__ == '__main__':
    app.run(debug=True)
