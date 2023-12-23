import sqlite3

# Connect to the database (creates a new one if not exist)
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Create a users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL  -- Add this line for the password column
    )
''')

# Create a notes table with the user_id and created_at columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER,  -- Add this line to create the user_id column
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Use DEFAULT to set the timestamp
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Create a trigger to automatically add a timestamp when a new note is added
# Note: This trigger is no longer needed with the DEFAULT CURRENT_TIMESTAMP in the table definition

# Create the user_notes_view
from crud_operations import create_user_notes_view
create_user_notes_view()

# Commit changes and close the connection
conn.commit()
conn.close()