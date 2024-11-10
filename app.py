import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for events, mapped by page_id
events = {}

@app.route('/')
def index():
    page_id = str(uuid.uuid4())  # Generate a unique page_id each time the index route is accessed
    print("Generated page ID:", page_id)
    return redirect(url_for('saved', page_id=page_id))  # Redirect to the new page with page_id

@app.route('/<page_id>')
def saved(page_id):
    print("Go to saved for page ID:", page_id)
    page_events = events.get(page_id, {})  # Retrieve events for the specific page_id
    return render_template('calendar.html', events=page_events, page_id=page_id)

@app.route('/<page_id>', methods=['POST'])
def add_events(page_id):
    print("Adding events for page ID:", page_id)
    page_events = events.setdefault(page_id, {})  # Get or create an entry for page_id in the events dict
    received = request.form.to_dict(flat=True)  # Convert form data to a dictionary
    for k, v in received.items():
        page_events[int(k)] = v  # Store events per day in the specific page's dictionary
    return render_template('calendar.html', events=page_events, page_id=page_id)

if __name__ == '__main__':
    app.run(debug=True)
