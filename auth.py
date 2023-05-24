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
    #TODO transformer query en requête sql
    user = 'SELECT email FROM Utilisateur where mail=%s'
    pass_user = 'SELECT mdp FROM Utilisateur where email=%s'
    mycursor.execute(user, (str(email)))
    mycursor.execute(pass_user, (str(email)))

    if not user or not check_password_hash(pass_user, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    return redirect(url_for('app.profil'))


    #return render_template('formulaire_user_connect.html')


@auth.route('/inscription', methods=['POST'])
def insert_user():
    nom = request.form.get["nom"]
    prenom = request.form.get["prénom"]
    username = request.form.get["username"]
    email = request.form.get["email"]
    password = request.form.get["password"]

    #A FAIRE POUR VERIFIER SI LE COMPTE EXISTE DEJA
    #user = query.filter_by(email=email).first()
    #if user: 
    #    return redirect(url_for('auth.signup'))
    
    pwd_hash=generate_password_hash(password, method='sha256')
    #jsp si le password fonctionne
    mycursor.execute('''INSERT INTO Utilisateur (nom, prenom, pseudo, mail, mdp) VALUES (%s, %s, %s, %s, %s)''', (nom, prenom, username, email, pwd_hash))
    mydb.commit()

    # return render_template('formulaire_insc.html')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return 'Logout'
