import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Set the path to the SQLite database file
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
 # Disable tracking modifications for performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the database
db = SQLAlchemy(app)

# In-memory storage for events, mapped by page_id
events = {}

@app.route('/')
def index():
    # Generate a unique page_id each time the index route is accessed
    page_id = str(uuid.uuid4())
    print("Generated page ID:", page_id)
    # Redirect to the new page with page_id
    return redirect(url_for('saved', page_id=page_id))

@app.route('/<page_id>')
def saved(page_id):
    print("Go to saved for page ID:", page_id)
    # Retrieve events for the specific page_id
    page_events = events.get(page_id, {}) 
    return render_template('calendar.html', events=page_events, page_id=page_id)

@app.route('/<page_id>', methods=['POST'])
def add_events(page_id):
    print("Adding events for page ID:", page_id)
    # Get or create an entry for page_id in the events dict
    page_events = events.setdefault(page_id, {})
    # Convert form data to a dictionary
    received = request.form.to_dict(flat=True)
    for k, v in received.items():
        # Store events per day in the specific page's dictionary
        page_events[int(k)] = v
    return render_template('calendar.html', events=page_events, page_id=page_id)

if __name__ == '__main__':
    app.run(debug=True)
