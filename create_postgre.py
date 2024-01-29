import psycopg2
from datetime import datetime

def create_operations_table():
    conn = psycopg2.connect(
        dbname="calculateur",
        user="postgres",
        password="vincent94",
        host="localhost",
        port="5432",
        client_encoding="UTF8"
    )
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS operations
                    (id SERIAL PRIMARY KEY,
                     expression TEXT,
                     result REAL,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

def create_users_table():
    conn = psycopg2.connect(
        dbname='calculateur',
        user='postgres',
        password="vincent94",
        host='localhost',
        port='5432',
        client_encoding="UTF8"
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(255) NOT NULL,
            lastname VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def add_data():
    conn = psycopg2.connect(
        dbname='calculateur',
        user='postgres',
        password="vincent94",
        host='localhost',
        port='5432',
        client_encoding="UTF8"
    )
    cur = conn.cursor()
    cur.execute('INSERT INTO users (firstname,lastname,username,email,password)' 
                'VALUES (%s,%s,%s,%s,%s)',
                ('vincent','tran','vincent1234','gdfgfg@gmail.com','1234'))
    conn.commit()
    conn.close()

# Appel des fonctions pour créer les tables
create_operations_table()
create_users_table()

