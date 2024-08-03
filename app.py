from flask import Flask, request, redirect, url_for, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {
    'admin': generate_password_hash('your_password')
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('protected'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_password_hash = users.get(username)
    
    if user_password_hash and check_password_hash(user_password_hash, password):
        session['username'] = username
        return redirect(url_for('protected'))
    return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/protected')
def protected():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    return render_template('protected.html')

@app.route('/get_flag', methods=['POST'])
def get_flag():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    try:
        with open('flag.txt', 'r') as file:
            flag = file.read()
        return f'Flag: {flag}'
    except FileNotFoundError:
        return 'Flag file not found', 404

if __name__ == '__main__':
    app.run(debug=True)
