import sqlite3

"""
Création de la base de données calculateur.db
"""

conn = sqlite3.connect('calculateur.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS operations
            (expression text, resultat real)''')
conn.commit()