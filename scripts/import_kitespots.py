import csv
import sqlite3
import os
from pathlib import Path

# Create the database directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Connect to SQLite database (will be created if it doesn't exist)
conn = sqlite3.connect('data/kitespots.db')
cursor = conn.cursor()

# Create table for kitespots
cursor.execute('''
CREATE TABLE IF NOT EXISTS kitespots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    country TEXT,
    latitude REAL,
    longitude REAL,
    difficulty TEXT,
    water_type TEXT,
    search_text TEXT
)
''')

# Create index for faster text search
cursor.execute('CREATE INDEX IF NOT EXISTS idx_kitespots_search ON kitespots(search_text)')

# Path to your CSV file - update this to your actual path
csv_path = Path('data/kitespots.csv')

# Check if CSV exists
if not csv_path.exists():
    print(f"CSV file not found at {csv_path}. Please place your CSV file at this location.")
    conn.close()
    exit(1)

# Import data from CSV - using tab as delimiter since the file appears to be tab-separated
with open(csv_path, 'r', encoding='utf-8') as f:
    # Skip the header row if it exists
    first_line = f.readline().strip()
    f.seek(0)  # Go back to the beginning of the file
    
    # Determine if the file has a header by checking if the first row contains column names
    has_header = 'name' in first_line and 'location' in first_line
    
    # Create CSV reader with tab delimiter
    csv_reader = csv.reader(f, delimiter=',')
    
    # Skip header if it exists
    if has_header:
        next(csv_reader)
    
    # Clear existing data
    cursor.execute('DELETE FROM kitespots')
    
    for row in csv_reader:
        if len(row) >= 7:  # Ensure we have all required columns
            name = row[0].strip()
            location = row[1].strip()
            country = row[2].strip()
            
            # Handle potential empty or non-numeric values for coordinates
            try:
                latitude = float(row[3].strip())
            except (ValueError, IndexError):
                latitude = None
                
            try:
                longitude = float(row[4].strip())
            except (ValueError, IndexError):
                longitude = None
                
            difficulty = row[5].strip() if len(row) > 5 else ''
            water_type = row[6].strip() if len(row) > 6 else ''
            
            # Create a search_text field that combines name, location and country for better search
            search_text = f"{name} {location} {country}".lower()
            
            # Insert into database
            cursor.execute('''
            INSERT INTO kitespots (name, location, country, latitude, longitude, difficulty, water_type, search_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, location, country, latitude, longitude, difficulty, water_type, search_text))

# Commit changes and close connection
conn.commit()
print(f"Successfully imported kitespots into database. Total records: {cursor.lastrowid}")
conn.close()

