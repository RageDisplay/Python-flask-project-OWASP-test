from flask import Flask, render_template, request, redirect, session, url_for, make_response, send_file, abort, jsonify
from flask_wtf.csrf import generate_csrf
import secrets, sqlite3, os, psycopg2

from hashlib import sha256

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(32)

db_path = 'auth.db'
login_data = {}

@app.route('/')
def login():
    csrf_token = generate_csrf()
    session['csrf_token'] = csrf_token
    return render_template('login.html', csrf_token=csrf_token)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    global login_data
    
    csrf_token = session.get('csrf_token')
    
    if not csrf_token:
        abort(403)

    username = request.form['username']
    password = sha256((sha256(username.encode()).hexdigest() + sha256((request.form['password']).encode()).hexdigest()).encode()).hexdigest()
    
    login_data = {'username': username, 'password': password}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        session['username'] = username
        return redirect(url_for('input_text', csrf_token=csrf_token))
    else:
        return redirect(url_for('login'))

@app.route('/input_text')
def input_text():
    if 'username' in session:
        csrf_token = session.get('csrf_token')
        return render_template('input.html', csrf_token=csrf_token)
    else:
        return redirect(url_for('login'))

@app.route('/save_text', methods=['GET', 'POST'])
def save_text():
    if 'username' in session:
        global login_data
        csrf_token = session.get('csrf_token')
        
        if not csrf_token:
            abort(403)
        
        if request.method == 'POST':
            text = request.form['text']
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (login_data['username'], login_data['password'],))
            user_id = cursor.fetchone()
            user_id = user_id[0]
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
    csrf_token = session.get('csrf_token')
    return render_template('output.html', text_combined=text_combined, csrf_token=csrf_token)
    
@app.route('/download', methods=['POST'])
def download_file():
    csrf_token = session.get('csrf_token')
    
    if not csrf_token:
        abort(403)
        
    text_to_download = request.form['text']
    response = make_response(text_to_download)
    response.headers["Content-Disposition"] = "attachment; filename=text_from_db.txt"
    return response

@app.route('/search', methods=['GET', 'POST'])
def search():
    csrf_token = session.get('csrf_token')
    
    if not csrf_token:
        abort(403)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        query = request.form.get('query')
        cursor.execute('SELECT * FROM texts WHERE user_id LIKE ?', (query,))
        result = cursor.fetchall()
        conn.close()
        csrf_token = session.get('csrf_token')
        return render_template('search.html', result=result, csrf_token=csrf_token)
    else:
        csrf_token = session.get('csrf_token')
        return render_template('search.html', result='', csrf_token=csrf_token)
    
@app.route('/dwld')
def downloadprom():
        csrf_token = session.get('csrf_token')
        return render_template('download.html', csrf_token=csrf_token)
    
@app.route('/downloadfile', methods=['GET', 'POST'])
def download_manual():
    csrf_token = session.get('csrf_token')
    
    if not csrf_token:
        abort(403)
        
    download_direct = os.path.dirname(os.path.abspath(__file__))
    filename = request.form.get('filename', '')
    file_path = os.path.join(download_direct, filename)
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e), 500
    
if __name__ == '__main__':
    app.secret_key = '123456789'
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=7000, debug=True)