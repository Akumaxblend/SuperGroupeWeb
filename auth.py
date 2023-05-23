import mysql.connector
from flask import Flask,query,request,render_template,jsonify,abort,redirect, url_for, flash
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

auth = Flask('auth', __name__)
CORS(auth)

mydb = mysql.connector.connect(
    host="localhost",
    user="FilmsWeb",
    password="password",
    database="FilmsWeb"
)
mycursor = mydb.cursor()

@auth.route('/connexion')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    return redirect(url_for('app.profil'))


    return render_template('formulaire_user_connect.html')


@auth.route('/inscription', methods=['POST'])
def insert_user():
    nom = request.form.get["nom"]
    prenom = request.form.get["prénom"]
    username = request.form.get["username"]
    email = request.form.get["email"]
    password = request.form.get["password"]

    # email = request.form.get('email')
    # name = request.form.get('name')
    # password = request.form.get('password')

    user = query.filter_by(email=email).first()
    if user: 
        return redirect(url_for('auth.signup'))
    
    password=generate_password_hash(password, method='sha256')
    #jsp si le password fonctionne
    mycursor.execute('''INSERT INTO Utilisateur (nom, prenom, pseudo, mail, mdp) VALUES (%s, %s, %s, %s, {password})''', (nom, prenom, username, email, password))
    mydb.commit()

    # return render_template('formulaire_insc.html')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return 'Logout'
