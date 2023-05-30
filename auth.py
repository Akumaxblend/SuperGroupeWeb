import mysql.connector
from flask import Flask,query,request,session,render_template,jsonify,abort,redirect, url_for, flash
from flask_cors import CORS
import hashlib 

auth = Flask('auth', __name__)
CORS(auth)

mydb = mysql.connector.connect(
    host="localhost",
    user="FilmsWeb",
    password="password",
    database="FilmsWeb"
)
mycursor = mydb.cursor()

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
    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    pwd_hash=hasher.hexdigest()
    
    #jsp si le password fonctionne
    mycursor.execute(f"INSERT INTO Utilisateur (nom, prenom, username, email, password) VALUES ('{nom}', '{prenom}', '{username}', '{email}', '{pwd_hash}')")
    mydb.commit()

    # return render_template('formulaire_insc.html')
    return redirect('profil.html')

@auth.route('/connexion')
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    pwd_hash=hasher.hexdigest()

    query = f"SELECT * FROM Utilisateurs WHERE email = %s AND password = %s"
    mycursor.execute(f"SELECT * FROM Utilisateurs WHERE email = {email} AND password = {pwd_hash}")
    user = mycursor.fetchone()

    if user:
        session['username'] = user[1]  # Supposons que le nom d'utilisateur soit enregistré à l'index 1
        return redirect('/')
    else:
            return "Identifiants invalides. Veuillez réessayer."
    


    #return render_template('formulaire_user_connect.html')




@auth.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')