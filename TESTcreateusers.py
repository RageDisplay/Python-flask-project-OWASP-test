import sqlite3
from hashlib import sha256

def add_user(username, password):
    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

name1 = "user1"
name2 = "user2"
pass1 = "12345"
pass2 = "qwerty"

hash_pass1 = sha256(pass1.encode()).hexdigest()
hash_pass2 = sha256(pass2.encode()).hexdigest()

add_user(name1, hash_pass1)
add_user(name2, hash_pass2)

