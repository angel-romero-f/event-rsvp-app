# Event RSVP App

A simple event management app where users can browse events and RSVP.

## Quick Setup

Requires Python 3.7+.

```bash
./setup.sh    # creates venv, installs dependencies, seeds database
./run.sh      # starts the server
```

Then open http://localhost:5000

## Project Structure

```
app.py              ← Backend: Flask API routes
schema.sql          ← Database schema
seed.py             ← Seeds the database with sample data

static/
  index.html        ← Event listing page
  event.html        ← Event detail page
  js/
    index.js        ← JS for the listing page
    event.js        ← JS for the detail page
  css/
    styles.css      ← Custom styles
```
