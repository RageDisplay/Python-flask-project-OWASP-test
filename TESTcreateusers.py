import psycopg2
from psycopg2 import Error
from hashlib import sha256

def add_user(username, password):
    try:
        conn = psycopg2.connect(host="localhost", port="5432", user="postgres", password="pass", database="auth")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
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

hash_namesum1 = hash_name1 + hash_pass1
hash_namesum2 = hash_name2 + hash_pass2
hash_namesum3 = hash_name3 + hash_pass3

extrahash1 = sha256(hash_namesum1.encode()).hexdigest()
extrahash2 = sha256(hash_namesum2.encode()).hexdigest()
extrahash3 = sha256(hash_namesum3.encode()).hexdigest()

add_user(name1, extrahash1)
add_user(name2, extrahash2)
add_user(name3, extrahash3)
