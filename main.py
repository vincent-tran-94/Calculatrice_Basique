from flask import Flask, send_file, request, render_template
from calcule import calculatrice_NPI
import sqlite3
import csv

"""
MISE EN TEST sur CURL 
curl -X POST -H "Content-Type: application/json" -d '{"expression": "2 3 + 5 *"}' http://localhost:5000/evaluate
curl http://localhost:5000/api/affichage
curl -X GET http://localhost:5000/export_csv
"""

#Création de l'application Flask 
app = Flask(__name__,template_folder='template')

#Insertion des opérations et des résultats sur la base de données calculateur avec l'API REST 
@app.route('/evaluate', methods=['POST'])
def evaluate():
    conn = sqlite3.connect('calculateur.db')
    c = conn.cursor()
    data = request.get_json()
    expression = data['expression']
    result = calculatrice_NPI(expression)
    c.execute("INSERT INTO operations VALUES (?, ?);", (expression, result))
    conn.commit() 
    return {'result': result}

#Affichage de la base de données calculateur avec l'API 
@app.route('/api/affichage')
def affichage():
    conn = sqlite3.connect('calculateur.db')
    c = conn.cursor()
    c.execute("SELECT * FROM operations")
    rows = c.fetchall()
    conn.commit()
    return rows

"""
Application avec l'interface web
"""
#Page d'accueil 
@app.route('/')
def home():
   return render_template('home.html')

#Page insertion des opérations pour effectuer le calculateur NPI
@app.route('/insert')
def insert():
   return render_template('insert.html')

#Ajouter les opérations pour reconnaître sur une base de données
@app.route('/add_operations',methods = ['POST'])
def add_operations():
    if request.method == 'POST':
        try:
            expression = request.form['expression']
            result = calculatrice_NPI(expression)
            with sqlite3.connect("calculateur.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO operations VALUES (?, ?);", (expression, result))
            con.commit()
            msg = "Opération Succès ! Votre opération est enregistrée "
        except:
            msg = "Erreur à l'insertion"
            con.rollback()
        finally:
            return render_template("result.html",msg = msg)


#Affichage de la base de données calculateur sur la page HTML 
@app.route('/list')
def list():
    con = sqlite3.connect("calculateur.db")
    con.row_factory = sqlite3.Row #Affichage ligne par ligne sur notre page HTML
    cur = con.cursor()
    cur.execute("SELECT * FROM operations;")
    rows = cur.fetchall()
    return render_template('database.html',rows=rows)


#Export le fichier CSV à partir d"une base de données calculateur
@app.route('/export_csv',methods =["GET"])
def export_csv():
    conn = sqlite3.connect('calculateur.db')
    c = conn.cursor()
    c.execute("SELECT * FROM operations")
    rows = c.fetchall()
    print(rows)
    conn.close() 
    
    with open('operations.csv','w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['expression', 'resultat'])
        for row in rows:
            writer.writerow(row)

    return send_file('operations.csv')

#Lancement de l'application Flask
if __name__ == '__main__':
    app.run('0.0.0.0',debug= True,port=80)
