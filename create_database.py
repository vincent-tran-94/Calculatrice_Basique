import sqlite3

"""
Création de la base de données calculateur.db
"""
def create_operations():
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
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL, 
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_operations() 
create_users_table()