from flask import Flask, request, render_template, session, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_classy_key' 

DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    return render_template('dashboard.html', username=None)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash("Username aur Password are required")
        return redirect(url_for('dashboard'))
        
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        flash("Registration successful!")
    except sqlite3.IntegrityError:
        flash("Username already teken by other user!")
        
    return redirect(url_for('dashboard'))

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    
    if user:
        session['user'] = user['name']
        flash(f"Welcome back, {user['name']}!")
    else:
        flash("Invalid Credentials! Try again.")
        
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)