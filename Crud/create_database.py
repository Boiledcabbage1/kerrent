# create_database.py
import sqlite3

# Connect to the database (creates a new one if not exist)
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create a users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

# Create a notes table with the user_id and created_at columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER,  -- Add this line to create the user_id column
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Create a trigger to automatically add a timestamp when a new note is added
cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS add_timestamp AFTER INSERT ON notes
    BEGIN
        UPDATE notes SET created_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
''')

# Create the user_notes_view
from crud_operations import create_user_notes_view
create_user_notes_view()

# Commit changes and close the connection
conn.commit()
conn.close()
