#!/bin/bash

echo "Setting up Event RSVP App..."
echo ""

# Create virtual environment
echo "1. Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "2. Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "3. Installing dependencies..."
pip install -r requirements.txt

# Seed database
echo "4. Seeding database..."
python seed.py

echo ""
echo "Setup complete! To run the app:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open http://localhost:5000 in your browser"
