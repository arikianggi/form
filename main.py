from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Dummy user credentials (replace with a proper user authentication mechanism)
AUTHORIZED_USERS = {'admin': 'password'}

# Temporary storage for submitted data (replace with a database in a real application)
submitted_data = []

@app.route('/')
def index():
    return render_template('helpdesk_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Extract form data
    name = request.form['name']
    email = request.form['email']
    issue = request.form['issue']
    
    # Add form data to submitted_data
    submitted_data.append({'name': name, 'email': email, 'issue': issue})

    # Redirect the user to the thank you page
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in AUTHORIZED_USERS and AUTHORIZED_USERS[username] == password:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session and session['logged_in']:
        return render_template('dashboard.html', data=submitted_data)
    else:
        return redirect(url_for('login'))

@app.route('/toggle_completed', methods=['POST'])
def toggle_completed():
    completed_indices = request.form.getlist('completed[]')
    for index in completed_indices:
        submitted_data[int(index) - 1]['completed'] = not submitted_data[int(index) - 1].get('completed', False)
    return redirect(url_for('dashboard'))

def clear_session():
    if session.get('logged_in') and not session['logged_in']:
        session.clear()

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'  # Set a secret key for session management
    app.run(debug=True)
