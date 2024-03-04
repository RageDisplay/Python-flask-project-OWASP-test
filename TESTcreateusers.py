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
name3 = "user3"
pass1 = "12345"
pass2 = "qwerty"
pass3 = "12345"



hash_name1 = sha256(name1.encode()).hexdigest()
hash_name2 = sha256(name2.encode()).hexdigest()
hash_name3 = sha256(name3.encode()).hexdigest()

hash_pass1 = sha256(pass1.encode()).hexdigest()
hash_pass2 = sha256(pass2.encode()).hexdigest()
hash_pass3 = sha256(pass3.encode()).hexdigest()

add_user(name1, hash_name1 + hash_pass1)
add_user(name2, hash_name2 + hash_pass2)
add_user(name3, hash_name3 + hash_pass3)
