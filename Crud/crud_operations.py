# crud_operations.py
import sqlite3

# Database connection context manager
def connect_db():
    return sqlite3.connect('mydatabase.db')

# User CRUD operations
def create_user(username, email):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
        conn.commit()

def read_users():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
    return users

def update_user(user_id, new_username, new_email):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET username=?, email=? WHERE id=?', (new_username, new_email, user_id))
        conn.commit()

def delete_user(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
        conn.commit()

# Note CRUD operations
def create_note(title, content):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
        conn.commit()

def read_notes():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_notes_view')
        notes = cursor.fetchall()
    return notes

def update_note(note_id, new_title, new_content):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE notes SET title=?, content=? WHERE id=?', (new_title, new_content, note_id))
        conn.commit()

def delete_note(note_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id=?', (note_id,))
        conn.commit()

def read_note_by_id(note_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id=?', (note_id,))
        note = cursor.fetchone()
    return note

# Additional functions
def read_notes_with_users():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT notes.id, notes.title, notes.content, users.username
            FROM notes
            JOIN users ON notes.user_id = users.id
        ''')
        notes = cursor.fetchall()
    return notes

def create_user_notes_view():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS user_notes_view AS
            SELECT notes.id, notes.title, notes.content, users.username
            FROM notes
            JOIN users ON notes.user_id = users.id
        ''')
        conn.commit()
        
def read_added_notes():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM added_notes_view')  # Replace 'added_notes_view' with the appropriate view or table
        added_notes = cursor.fetchall()
    return added_notes

# Example usage of the "stored procedure" function
def add_user_procedure(username, email):
    create_user(username, email)

# Uncomment and use the "stored procedure" as needed
# add_user_procedure('JohnDoe', 'john@example.com')
