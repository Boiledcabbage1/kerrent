from flask import Flask, render_template, request, redirect
from crud_operations import read_users, read_notes, create_note

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('home.html')

# New route for notes
@app.route('/notes', methods=['GET', 'POST'])
def view_notes():
    if request.method == 'POST':
        data = request.get_json()
        create_note(data['title'], data['content'])
        return 'Note added successfully', 201

    notes = read_notes()
    return render_template('notes.html', notes=notes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
