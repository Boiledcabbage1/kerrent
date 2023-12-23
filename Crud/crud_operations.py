# crud_operations.py
import sqlite3
import hashlib

# Database connection context manager
def connect_db():
    return sqlite3.connect('mydatabase.db')

# User CRUD operations
def create_user(username, email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
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
def create_note(title, content, user_id=None):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)', (title, content, user_id))
        conn.commit()
        
def read_notes():
    with connect_db() as conn:
        cursor = conn.cursor()

        # Log the structure of the 'user_notes_view'
        cursor.execute('PRAGMA table_info(user_notes_view)')
        view_info = cursor.fetchall()
        print('User Notes View structure:', view_info)

        cursor.execute('SELECT * FROM user_notes_view')
        notes = cursor.fetchall()
        print('Fetched notes:', notes)  # Log the fetched notes
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

        # Log the structure of the 'user_notes_view'
        cursor.execute('PRAGMA table_info(user_notes_view)')
        view_info = cursor.fetchall()
        print('User Notes View structure:', view_info)

        # Retrieve notes with users using INNER JOIN
        cursor.execute('''
            SELECT notes.id, notes.title, notes.content, notes.user_id, users.username
            FROM notes
            INNER JOIN users ON notes.user_id = users.id
        ''')
        notes = cursor.fetchall()

        # Log the fetched notes with users and the actual content of 'notes' and 'users' tables
        print('Fetched notes with users:', notes)
        cursor.execute('SELECT * FROM notes')
        print('Content of notes table:', cursor.fetchall())
        cursor.execute('SELECT * FROM users')
        print('Content of users table:', cursor.fetchall())

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
        cursor.execute('SELECT * FROM user_notes_view')
        added_notes = cursor.fetchall()
        print('Added notes:', added_notes)  # Add this line to log the added notes
    return added_notes

def authenticate_user(username, password):
    try:
        # Retrieve user from the database based on the provided username
        user = get_user_by_username(username)

        # Check if the user exists and if the provided password matches the stored password
        if user:
            stored_password_hash = user['password']
            provided_password_hash = hash_password(password)

            print('Stored Password Hash:', stored_password_hash)
            print('Provided Password Hash:', provided_password_hash)

            if stored_password_hash == provided_password_hash:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        # Log the exception details
        print(f"Exception during authentication: {str(e)}")
        return False
    
def get_user_by_username(username):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
    
    if user:
        # Convert the tuple to a dictionary with column names as keys
        user_dict = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'password': user[3]
            # Add more columns if needed
        }
        return user_dict
    else:
        return None

def check_password(provided_password, stored_password_hash):
    # Hash the provided password using the same algorithm and parameters used for storage
    hashed_provided_password = hashlib.sha256(provided_password.encode()).hexdigest()

    # Compare the hashed provided password with the stored password hash
    print('Provided Password:', hashed_provided_password)
    print('Stored Password Hash:', stored_password_hash)
    
    result = hashed_provided_password == stored_password_hash
    print('Password Match Result:', result)

    return result

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Example usage of the "stored procedure" function
def add_user_procedure(username, email):
    create_user(username, email)

# Uncomment and use the "stored procedure" as needed
# add_user_procedure('JohnDoe', 'john@example.com')
