from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)

db_path = 'auth.db'
login_data = {}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global login_data
    
    username = request.form['username']
    password = request.form['password']
    
    login_data = {'username': username, 'password': password}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)
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

@app.route('/save_text', methods=['GET', 'POST'])
def save_text():
    if 'username' in session:
        user_id = request.args.get('user_id')
        global login_data
        
        if request.method == 'POST':
            text = request.form['text']
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            user_idget ="SELECT id FROM users WHERE username = '" + login_data['username'] + "' AND password = '" + login_data['password'] + "'"
            cursor.execute(user_idget)
            user_id = cursor.fetchone()
            user_id = user_id[0]
            sqli = "INSERT INTO texts (text, user_id) VALUES (?, ?)"
            cursor.execute(sqli, (text, user_id))
            conn.commit()
            conn.close()
            return redirect(url_for('display_text', user_id=user_id))
    else:
        return redirect(url_for('login'))


@app.route('/display_text')
def display_text():
    user_id = request.args.get('user_id')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM texts WHERE user_id=?', (user_id,))
    texts = cursor.fetchall()
    conn.close()

    if texts:
        text_combined = ', '.join(text[0] for text in texts)
        return f'Texts for User ID {user_id}: {text_combined}'
    else:
        return f'Texts not found for User ID {user_id}'
    
if __name__ == '__main__':
    app.secret_key = '12345'
    app.run()