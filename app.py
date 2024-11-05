from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for events
events = {}

page_id = "saved"

@app.route('/')
def index():
    return render_template('calendar.html', events=events)

@app.route('/{}'.format(page_id))
def saved():
    print(events)
    return render_template('calendar.html', events=events)

@app.route('/add_events', methods=['POST'])
def add_events():
    global events
    received = request.form.to_dict(flat=True)  # Converts form data to a dictionary
    print("Received events:", received)  # For debugging
    for k,v in received.items():
        events[int(k)] = v
    return redirect(url_for('saved'))

if __name__ == '__main__':
    app.run(debug=True)
