from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
from flask import render_template, session
import sqlite3

app = Flask(__name__)
app.secret_key = '#jerryD123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

# Define the User and Note models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

# Create the database tables
with app.app_context():
    db.create_all()

# Database Connection
def connect_db():
    return sqlite3.connect('mydatabase.db')

# Database Setup
def create_user_notes_view():
    # Create view
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE VIEW IF NOT EXISTS user_notes_view AS
            SELECT notes.id, notes.title, notes.content, users.username
            FROM notes
            JOIN users ON notes.user_id = users.id
        ''')
        conn.commit()
        
    # Drop existing trigger and view if they exist
    with connect_db() as conn:
        conn.execute('DROP TRIGGER IF EXISTS log_note_changes;')
        conn.execute('DROP VIEW IF EXISTS user_notes_view;')
        conn.commit()
        
    # Create stored procedure
    query_add_user = '''
        CREATE PROCEDURE AddUser(username_param VARCHAR(50), email_param VARCHAR(50), password_param VARCHAR(50))
        BEGIN
            INSERT INTO users (username, email, password) VALUES (username_param, email_param, password_param);
        END;
    '''
    with connect_db() as conn:
        conn.execute(query_add_user)
        conn.commit()

    # Create table for changes log
    query_create_log_table = '''
        CREATE TABLE IF NOT EXISTS note_changes_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER,
            change_type TEXT,
            change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    '''
    with connect_db() as conn:
        conn.execute(query_create_log_table)
        conn.commit()
    
    # Create trigger
    query_log_note_changes = '''
        CREATE TRIGGER log_note_changes
        AFTER INSERT OR UPDATE OR DELETE ON notes
        BEGIN
            -- Your trigger logic here
            -- For example, you might print a message to the console
            -- or perform other actions based on the type of change.
            -- This can be customized based on your requirements.
            -- Note: The example below prints a message to the console.
            SELECT 'Note change logged: ' || 
                   CASE
                       WHEN OLD.id IS NULL THEN 'INSERT'
                       WHEN NEW.id IS NULL THEN 'DELETE'
                       ELSE 'UPDATE'
                   END AS change_type,
                   datetime('now');
        END;
    '''
    with connect_db() as conn:
        conn.execute(query_log_note_changes)
        conn.commit()

# Flask Routes
# Flask Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Perform user authentication (replace this with your actual authentication logic)
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Log in the user
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # Display an error message if authentication fails
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/index')
def index():
    # Display all notes
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Insert a new user directly into the 'users' table
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Automatically log in the user after registration
        session['logged_in'] = True
        session['username'] = username
        
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = 1  # Replace with the actual user ID (you may implement user authentication)
        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', note=note)

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/notes_with_users')
def notes_with_users():
    # Perform a SQL JOIN to fetch notes with user information
    query = '''
        SELECT notes.id, notes.title, notes.content, users.username
        FROM notes
        JOIN users ON notes.user_id = users.id
    '''
    result = db.session.execute(text(query))
    notes_with_users = [dict(row) for row in result]
    return render_template('notes_with_users.html', notes_with_users=notes_with_users)

if __name__ == '__main__':
    app.run(debug=True)

