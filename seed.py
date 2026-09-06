import sqlite3
import os

DB_FILE = 'database.db'

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

with open('schema.sql', 'r') as f:
    cursor.executescript(f.read())

users = [
    ('Alice Chen', 'alice@example.com'),
    ('Bob Martinez', 'bob@example.com'),
    ('Carol Wang', 'carol@example.com'),
    ('David Kim', 'david@example.com'),
    ('Emma Silva', 'emma@example.com'),
]

cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', users)

events = [
    (
        'Python Workshop: Web Scraping',
        'Learn how to scrape websites using BeautifulSoup and requests. We\'ll build a real scraper together.',
        'TechHub Downtown',
        '2026-10-15T18:00:00',
        30
    ),
    (
        'React Fundamentals',
        'Introduction to React for beginners. We\'ll cover components, props, state, and hooks.',
        'CodeSpace Arena',
        '2026-10-20T19:00:00',
        25
    ),
    (
        'Database Design Best Practices',
        'Deep dive into relational database design, normalization, and indexing strategies.',
        'DevCenter Coworking',
        '2026-10-22T18:30:00',
        15
    ),
    (
        'Introduction to Docker',
        'Containerize your applications with Docker. Hands-on session with practical examples.',
        'TechHub Downtown',
        '2026-10-28T17:00:00',
        20
    ),
    (
        'Git and GitHub Workflow',
        'Master version control with Git. Learn branching, merging, rebasing, and collaboration workflows.',
        'StartupLoft',
        '2026-09-01T18:00:00',
        40
    ),
]

cursor.executemany(
    'INSERT INTO events (title, description, location, date, capacity) VALUES (?, ?, ?, ?, ?)',
    events
)

rsvps = [
    (2, 1, 'confirmed'),
    (3, 1, 'confirmed'),
    (4, 1, 'confirmed'),
    (5, 1, 'confirmed'),
    (1, 2, 'confirmed'),
    (2, 2, 'confirmed'),
    (3, 2, 'confirmed'),
    (4, 2, 'confirmed'),
    (5, 2, 'confirmed'),
    (1, 3, 'confirmed'),
    (2, 3, 'confirmed'),
    (3, 3, 'confirmed'),
    (4, 3, 'confirmed'),
    (5, 3, 'confirmed'),
    (2, 4, 'confirmed'),
    (3, 4, 'confirmed'),
    (4, 4, 'confirmed'),
]

cursor.executemany(
    'INSERT INTO rsvps (user_id, event_id, status) VALUES (?, ?, ?)',
    rsvps
)

conn.commit()
conn.close()

print('Database seeded successfully!')
print('Events created:')
print('  1. Python Workshop (30 capacity, 4 confirmed)')
print('  2. React Fundamentals (25 capacity, 5 confirmed)')
print('  3. Database Design (15 capacity, 5 confirmed - nearly full!)')
print('  4. Docker Workshop (20 capacity, 3 confirmed)')
print('  5. Git Workshop (40 capacity, 0 confirmed - past event)')
