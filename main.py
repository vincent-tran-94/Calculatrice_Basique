from flask import Flask, send_file, request, render_template, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from calcule import calculatrice
from chat import get_response
from create_postgre import get_db_connection
import csv


"""
Tests des opérations et téléchargement du fichier CSV en utilisant CURL
curl -X POST -H "Content-Type: application/json" -d '{"expression": "2 3 + 5 *"}' http://localhost:5000/evaluate
curl -X GET http://localhost:5000/export_csv 
"""

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'my_secret_key'  # Change this to a random secret key

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
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username, password FROM users WHERE username = %s;", (username,))
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
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Vous devez hasher le mot de passe avant de le stocker dans la base de données
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (firstname, lastname, username, email, password)' 
                    'VALUES (%s, %s, %s, %s, %s)', 
                    (firstname,lastname,username,email, hashed_password))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

#Insertion des opérations et des résultats sur la base de données calculateur 
@app.route('/evaluate', methods=['POST'])
def evaluate():
    conn = get_db_connection()
    c = conn.cursor()
    data = request.get_json()
    expression = data['expression']
    result = calculatrice(expression)
    c.execute("INSERT INTO operations (expression,result) VALUES (%s, %s);", (expression, result))
    conn.commit() 
    return {'result': result}



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

#Page insertion des opérations pour effectuer le calculateur 
@app.route('/insert')
@login_required
def insert():
   return render_template('insert.html')

#Ajouter les opérations pour reconnaître sur une base de données
"""
Renvoie une expression en entrée pour avoir une sortie d'un résultat"
"""
@app.route('/add_operations',methods = ['POST'])
@login_required
def add_operations():
    if request.method == 'POST':
        try:
            expression = request.form['expression']
            result = calculatrice(expression)
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO operations (expression,result) VALUES (%s, %s);", (expression, result))
            conn.commit()
            msg = "Opération Succès ! Votre opération est enregistrée "
        except:
            msg = "Erreur à l'insertion"
            conn.rollback()
        finally:
            return render_template("insert.html",msg = msg)


  
        
# Ajoutez cette route pour supprimer une opération en utilisant une expression avec la méthode POST
@app.route('/delete_operation', methods=['POST'])
@login_required
def delete_operation():
    if request.method == 'POST':
        expression = request.form['expression']
        conn = get_db_connection()
        c = conn.cursor()

        # Vérifiez d'abord si l'opération existe dans la base de données
        c.execute("SELECT * FROM operations WHERE expression = %s;", (expression,))
        existing_operation = c.fetchone()

        if existing_operation:
            # Si l'opération existe, supprimez-la de la base de données
            c.execute("DELETE FROM operations WHERE expression = %s;", (expression,))
            conn.commit()
            msg = f"L'opération avec l'expression '{expression}' a été supprimée avec succès."
        else:
            msg = f"L'opération avec l'expression '{expression}' n'existe pas dans la base de données."

        conn.close()
        return render_template("result.html", msg=msg)
        
@app.route('/delete_all_operations', methods=['POST'])
@login_required
def delete_all_operations():
    if request.method == 'POST':
        conn = get_db_connection()
        c = conn.cursor()
        try:
            # Supprimez toutes les opérations de la base de données
            c.execute("DELETE FROM operations;")
            conn.commit()
            msg = "Toutes les opérations ont été supprimées avec succès."
        except Exception as e:
            msg = f"Erreur lors de la suppression de toutes les opérations: {str(e)}"
            conn.rollback()
        finally:
            conn.close()
            return render_template("result.html", msg=msg)


#Affichage de la base de données calculateur sur la page HTML 
@app.route('/list')
@login_required
def list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, expression, result, to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') FROM operations ORDER BY created_at DESC")
    rows = cur.fetchall()
    return render_template('database.html',rows=rows)


#Export le fichier CSV à partir d"une base de données calculateur
@app.route('/export_csv',methods =["GET"])
@login_required
def export_csv():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, expression, result, to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') FROM operations ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close() 
    
    with open('operations.csv','w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['expression', 'resultat','date_et_heure'])
        for row in rows:
            writer.writerow(row)

    return send_file('operations.csv')

@app.get("/insert")
@login_required
def index_get(): 
    return render_template("insert.html")

@app.post("/predict")
@login_required
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer":response}
    return jsonify(message)


# Your existing routes go here

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

