from flask import Flask, render_template, request, redirect, session, url_for, make_response, send_file
import sqlite3, os
from hashlib import sha256

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
    
    passwordenter = request.form['password']
    
    usernamesault = sha256(username.encode()).hexdigest()
    
    password = usernamesault + sha256(passwordenter.encode()).hexdigest()
    
    login_data = {'username': username, 'password': password}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    #query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    #cursor.execute(query)
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
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
        global login_data
        
        if request.method == 'POST':
            text = request.form['text']
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            #user_idget ="SELECT id FROM users WHERE username = '" + login_data['username'] + "' AND password = '" + login_data['password'] + "'"
            #cursor.execute(user_idget)
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (login_data['username'], login_data['password'],))
            user_id = cursor.fetchone()
            user_id = user_id[0]
            #ins = "INSERT INTO texts (text, user_id) VALUES (?, ?)"
            #cursor.execute(ins, (text, user_id))
            cursor.execute('INSERT INTO texts (text, user_id) VALUES (?, ?)', (text, user_id))
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

    global text_combined
    text_combined = ', '.join(text[0] for text in texts)
    return render_template('output.html', text_combined=text_combined)
    
@app.route('/download', methods=['POST'])
def download_file():
    text_to_download = request.form['text']
    response = make_response(text_to_download)
    response.headers["Content-Disposition"] = "attachment; filename=text_from_db.txt"
    return response

@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if request.method == 'POST':
        query = request.form.get('query')
        #command = "SELECT * FROM texts WHERE user_id LIKE '%" + query + "%'"   #'OR+1=1--   '; echo cat /
        #cursor.execute(command)
        cursor.execute('SELECT * FROM texts WHERE user_id LIKE ?', (query,))
        result = cursor.fetchall()
        conn.close()
        return render_template('search.html', result=result)
    else:
        return render_template('search.html', result='')
    
@app.route('/dwld')
def downloadprom():
        return render_template('download.html')
    
@app.route('/downloadfile', methods=['GET', 'POST'])
def download_manual():
    download_direct = os.path.dirname(os.path.abspath(__file__))
    filename = request.form.get('filename', '')
    file_path = os.path.join(download_direct, filename)

    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e), 500
    
if __name__ == '__main__':
    app.secret_key = '12345'
    app.run()