# app.py

from flask import Flask, request, jsonify, render_template, redirect
from crud_operations import create_user, read_users, update_user, delete_user
from crud_operations import create_note, read_notes, update_note, delete_note
from flask import abort
from crud_operations import authenticate_user


app = Flask(__name__, static_folder='static')

# User routes
@app.route('/users', methods=['GET'])
def get_users():
    users = read_users()
    return jsonify(users)

# User routes
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    # Ensure required fields are present in the JSON data
    if 'username' not in data or 'email' not in data or 'password' not in data:
        abort(400, 'Bad Request - Missing required fields')

    try:
        create_user(data['username'], data['email'], data['password'])
        return 'User added successfully', 201
    except Exception as e:
        # Handle the exception and print or log the error for debugging
        print(f"Error adding user: {str(e)}")
        return jsonify({'error': 'Registration failed. Please try again later.'}), 500
    
    
# Login route
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    # Ensure required fields are present in the JSON data
    if 'username' not in data or 'password' not in data:
        abort(400, 'Bad Request - Missing required fields')

    try:
        # Perform authentication logic here (compare passwords, check credentials, etc.)
        # For simplicity, let's assume you have a function named 'authenticate_user' in 'crud_operations.py
        user_authenticated = authenticate_user(data['username'], data['password'])

        if user_authenticated:
            return 'Login successful', 200
        else:
            abort(401, 'Unauthorized - Incorrect username or password')
    except Exception as e:
        # Log the exception details
        print(f"Exception during login: {str(e)}")
        abort(500, 'Internal Server Error - Please try again later')


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_existing_user(user_id):
    data = request.get_json()
    update_user(user_id, data['username'], data['email'])
    return 'User updated successfully'

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_existing_user(user_id):
    delete_user(user_id)
    return 'User deleted successfully'

# Note routes
@app.route('/notes', methods=['GET', 'POST'])
def manage_notes():
    if request.method == 'POST':
        data = request.get_json()
        create_note(data['title'], data['content'], data.get('user_id'))
        return 'Note added successfully', 201

    notes = read_notes()

    # Check if the request wants JSON response
    if 'application/json' in request.headers.get('Accept', ''):
        response = jsonify(notes)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Render the template for HTML response
    return render_template('notes.html', notes=notes)

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_existing_note(note_id):
    data = request.get_json()
    update_note(note_id, data['title'], data['content'])
    return 'Note updated successfully'

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_existing_note(note_id):
    delete_note(note_id)
    return 'Note deleted successfully'

# Home route
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)