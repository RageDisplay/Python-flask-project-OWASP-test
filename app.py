from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)

db_path = 'auth.db'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = username
        return redirect(url_for('input_text'))
    else:
        return redirect(url_for('login'))

@app.route('/input_text')
def input_text():
    if 'username' in session:
        return render_template('input.html')
    else:
        return redirect(url_for('login'))

@app.route('/save_text', methods=['POST'])
def save_text():
    if 'username' in session:
        text = request.form['text']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO texts (text) VALUES (?)", (text,))
        conn.commit()
        conn.close()
        return redirect(url_for('display_text', text=text))
    else:
        return redirect(url_for('login'))

@app.route('/display_text')
def display_text():
    if 'username' in session:
        text = request.args.get('text')
        return render_template('output.html', text=text)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = '12345'
    app.run()
