# Event RSVP App

A simple event management app where users can browse events and RSVP.

## Requirements

- Python 3.7 or higher
- Flask 2.0+

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or with pip3:
```bash
pip3 install -r requirements.txt
```

2. Seed the database:
```bash
python seed.py
```

3. Run the app:
```bash
python app.py
```

4. Open http://localhost:5000 in your browser

## Troubleshooting

If `python` doesn't work, try `python3`:
```bash
python3 seed.py
python3 app.py
```

## Features

- Browse upcoming events
- View event details and attendee lists
- RSVP to events (with capacity limits)
- Cancel RSVPs
