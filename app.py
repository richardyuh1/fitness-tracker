from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for events
events = []

@app.route('/')
def index():
    return render_template('index.html', events=events)

@app.route('/add_events', methods=['POST'])
def add_events():
    event = request.form.get('event')
    events.append(event)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
