import sqlite3

"""
Création de la base de données calculateur.db
"""

conn = sqlite3.connect('calculateur.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS operations
            (expression text, resultat real)''')
conn.commit()

def create_users_table():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_users_table()