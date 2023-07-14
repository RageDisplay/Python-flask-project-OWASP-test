import sqlite3

def add_user(username, password):
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

add_user('jo', '123')
add_user('ja', 'qwerty')

