# -*- coding: utf-8 -*-

import mysql.connector
from flask import Flask,request,render_template,jsonify,abort, redirect
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="FilmsWeb",
    password="password",
    database="FilmsWeb"
)

mycursor = mydb.cursor()

# mycursor.execute('''select * from Genre''')
# etuds = mycursor.fetchall()
# mydb.commit()
# print(etuds)

films = []

@app.route("/")
def index():
    
    #return ("<html><body><p1>Hello world</p1></body></html>")
    return render_template("formulaire_insc.html")

@app.route("/inscription", methods=['POST'])
def insert_user():

    global prenom
    global nom
    global username
    global email
    global password 

    # Version GET

    # nom = request.args.get("name")
    # prix = request.args.get("price")
    # description = request.args.get("depiction")

    # Version POST

    if(request.method == 'POST'):
        nom = request.form["nom"]
        prenom = request.form["prénom"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        #games.append( {"name":nom, "price":prix, "depiction":description})
    
    mycursor.execute('''INSERT INTO Utilisateur (nom, prenom, pseudo, mail, mdp) VALUES (%s, %s, %s, %s, %s)''', (nom, prenom, username, email, password))
    mydb.commit()
        
    return render_template("liste.html")

@app.route("/connexion")
def login():
   return render_template('formulaire_user_connect.html')

@app.route("/profil")
def profil_user():
    return render_template("useraccount.html")


@app.route("/saisie_film")
def form_films():
    return render_template("formulaire_film.html")

@app.route("/film/send", methods=["POST"])
def insert_film():

    global nom_film
    global duree
    global annee
    global synopsis
    global genre 
    global nationalite

    if(request.method == 'POST'):
        nom_film = request.form["nom"]
        duree = request.form["duree"]
        annee = request.form["année"]
        synopsis = request.form["synopsis"]
        genre = request.form["genre"]
        nationalite = request.form["nationalite"]

    mycursor.execute('''INSERT INTO Film(titre, duree, anneSortie, synopsis) VALUES (%s, %s, %s, %s)''', (nom_film, duree, annee, synopsis))
    mydb.commit()

    return redirect("/films")

@app.route("/films")
def display_films():

    mycursor.execute('''SELECT COUNT(*) FROM Film''')
    filmsCount = mycursor.fetchone()

    mycursor.execute('''SELECT * FROM Film''')

    for tmp in mycursor:

        films.append({"titre":tmp[0], "duree":tmp[1], "annee":tmp[2], "synopsis":tmp[3]})

    return render_template("liste.html", f = films)





if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)