import json
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from models import db, Page

def create_app():
    app = Flask(__name__)
    
    # Set the path to the SQLite database file
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'app.db')
    # Disable tracking modifications for performance
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the app with the db object
    db.init_app(app)

    @app.route('/')
    def index():
        # Generate a unique page_id each time the index route is accessed
        page_id = str(uuid.uuid4())
        print("Generated page ID:", page_id)
        # Redirect to the new page with page_id
        return redirect(url_for('saved', page_id=page_id))

    @app.route('/favicon.ico')
    def favicon():
        return '', 204  # Respond with an empty response (status 204) for favicon

    @app.route('/<page_id>')
    def saved(page_id):
        print("Go to saved for page ID:", page_id)
        # Retrieve events for the specific page_id
        events = get_events_from_db(page_id)
        print("saved events:", events)
        return render_template('calendar.html', events=events, page_id=page_id)

    @app.route('/<page_id>', methods=['POST'])
    def add_events(page_id):
        print("Adding events for page ID:", page_id)
        # Convert form data to a dictionary
        events = request.form.to_dict(flat=True)
        print("add events:", events)
        add_events_to_db(page_id, events)
        return render_template('calendar.html', events=events, page_id=page_id)

    def add_events_to_db(page_id, events):
        # Check if the page_id already exists in the database
        page = Page.query.filter_by(id=page_id).first()
        if page:
            # Update the existing page with the new events
            page.events = json.dumps(events)
        else:
            # Add a new page
            page = Page(id=page_id, events=json.dumps(events))
            db.session.add(page)
        db.session.commit()
    
    def get_events_from_db(page_id):
        # Query a specific page by id
        page = Page.query.filter_by(id=page_id).first()
        if page:
            return json.loads(page.events)
        return {}

    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
