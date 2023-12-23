from flask import Flask, request, jsonify, render_template
from crud_operations import create_user, read_users, update_user, delete_user
from crud_operations import create_note, read_notes, update_note, delete_note
from flask import abort


app = Flask(__name__)

# User routes
@app.route('/users', methods=['GET'])
def get_users():
    users = read_users()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    # Ensure required fields are present in the JSON data
    if 'username' not in data or 'email' not in data:
        abort(400, 'Bad Request - Missing required fields')

    try:
        create_user(data['username'], data['email'])
        return 'User added successfully', 201
    except Exception as e:
        print(f"Error adding user: {str(e)}")
        abort(500, 'Internal Server Error')

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_existing_user(user_id):
    data = request.get_json()
    update_user(user_id, data['username'], data['email'])
    return 'User updated successfully'

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_existing_user(user_id):
    delete_user(user_id)
    return 'User deleted successfully'

# New note routes
@app.route('/notes', methods=['GET'])
def get_notes():
    notes = read_notes()

    # Check if the request wants JSON response
    if 'application/json' in request.headers.get('Accept', ''):
        response = jsonify(notes)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Render the template for HTML response
    return render_template('notes.html', notes=notes)
    
# New note routes
@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()

    # Ensure required fields are present in the JSON data
    if 'title' not in data or 'content' not in data:
        abort(400, 'Bad Request - Missing required fields')

    try:
        create_note(data['title'], data['content'])
        return 'Note added successfully', 201
    except Exception as e:
        print(f"Error adding note: {str(e)}")
        abort(500, 'Internal Server Error')
    
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_existing_note(note_id):
    data = request.get_json()
    update_note(note_id, data['title'], data['content'])
    return 'Note updated successfully'

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_existing_note(note_id):
    delete_note(note_id)
    return 'Note deleted successfully'

# Other routes
# Add your other routes here...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
