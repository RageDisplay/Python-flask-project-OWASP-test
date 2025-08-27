import psycopg2
from psycopg2 import Error

def create_auth_table():
    try:
        conn = psycopg2.connect(host="localhost", port="5432", user="postgres", password="pass", database="auth")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()

def create_text_table():
    try:
        conn = psycopg2.connect(host="localhost", port="5432", user="postgres", password="pass", database="auth")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS texts (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                user_id INTEGER REFERENCES users(id)
            )
        ''')
        conn.commit()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if conn:
            cursor.close()
            conn.close()

create_auth_table()
create_text_table()