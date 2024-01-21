from flask import Flask, send_file, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from calcule import calculatrice
import sqlite3
import csv



"""
MISE EN TEST sur CURL 
curl -X POST -H "Content-Type: application/json" -d '{"expression": "2 3 + 5 *"}' http://localhost:5000/evaluate
curl http://localhost:5000/api/affichage
curl -X GET http://localhost:5000/export_csv
"""

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vous devez vérifier les informations d'identification dans votre base de données
        with sqlite3.connect("accounts.db") as con:
            cur = con.cursor()
            cur.execute("SELECT username, password FROM users WHERE username = ?;", (username,))
            user_data = cur.fetchone()

            if user_data and check_password_hash(user_data[1], password):
                session['username'] = request.form['username']
                user = User(user_id=username)
                login_user(user)
                return redirect(url_for('home'))  # Fix here
            else:
                flash("Invalid username or password", "error")  # Flash message for error

    return render_template('login.html')


# Logout route
@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))



# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']


        # Vous devez hasher le mot de passe avant de le stocker dans la base de données
        hashed_password = generate_password_hash(password, method='sha256')

        with sqlite3.connect("accounts.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (firstname,lastname,email, username, password) VALUES (?,?,?,?,?);", (firstname,lastname,email,username, hashed_password))
            con.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

#Insertion des opérations et des résultats sur la base de données calculateur avec l'API REST 
@app.route('/evaluate', methods=['POST'])
def evaluate():
    conn = sqlite3.connect('calculateur.db')
    c = conn.cursor()
    data = request.get_json()
    expression = data['expression']
    result, operation_type = calculatrice(expression)
    operands_str = ' '.join(map(str, operation_type))
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
@app.route('/home')
@login_required 
def home():
    if 'username' in session:
        image_path = url_for('static', filename='calculatrice.jpg')
        return render_template('home.html',image_path=image_path)
    else:
        return redirect(url_for('login'))

#Page insertion des opérations pour effectuer le calculateur NPI
@app.route('/insert')
@login_required
def insert():
   return render_template('insert.html')

#Ajouter les opérations pour reconnaître sur une base de données
@app.route('/add_operations',methods = ['POST'])
@login_required
def add_operations():
    if request.method == 'POST':
        try:
            expression = request.form['expression']
            result = calculatrice(expression)
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
@login_required
def list():
    con = sqlite3.connect("calculateur.db")
    con.row_factory = sqlite3.Row #Affichage ligne par ligne sur notre page HTML
    cur = con.cursor()
    cur.execute("SELECT * FROM operations;")
    rows = cur.fetchall()
    return render_template('database.html',rows=rows)


#Export le fichier CSV à partir d"une base de données calculateur
@app.route('/export_csv',methods =["GET"])
@login_required
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




# Your existing routes go here


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
