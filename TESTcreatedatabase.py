import psycopg2

def create_database():
    conn = psycopg2.connect(host="localhost", port="5432", user="postgres", password="pass")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("CREATE DATABASE auth")
    cur.close()
    conn.close()

create_database()