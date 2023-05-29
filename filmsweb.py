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
commentaires=[]

@app.route("/")
def index():
    
    #return ("<html><body><p1>Hello world</p1></body></html>")
    #return render_template("formulaire_insc.html")
    return redirect("/films")

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
        genre = request.form["genres"]
        nationalite = request.form["nationalite"]

    mycursor.execute('''INSERT INTO Film(titre, duree, anneSortie, synopsis, genre) VALUES (%s, %s, %s, %s, %s)''', (nom_film, duree, annee, synopsis, genre))
    mydb.commit()

    return redirect("/films")

@app.route("/films")
def display_films():

    films.clear()

    mycursor.execute('''SELECT COUNT(*) FROM Film''')
    filmsCount = mycursor.fetchone()

    mycursor.execute('''SELECT * FROM Film''')

    for tmp in mycursor:

        films.append({"idFilm": tmp[0], "titre":tmp[1], "duree":tmp[2], "annee":tmp[3], "synopsis":tmp[4], "genre":tmp[5]})

    return render_template("liste.html", f = films)

#on récupère un film pour faire l'affichage d'une seule page film
def get_film(idFilm):
    mycursor.execute(f"SELECT * FROM Film WHERE idFilm = {idFilm}")
    film = mycursor.fetchone()
    #mycursor.close()
    return film

#là on récup les données pour afficher la page
@app.route('/films/<int:idFilm>', methods=["GET"])
def show_film(idFilm):
    film = get_film(idFilm)
    if film is None:
        return "Film non trouvé"

    commentaires.clear()

    mycursor.execute(f"SELECT * FROM Commentaire WHERE idFilm={idFilm}")

    for tmp in mycursor:

        commentaires.append({"texte":tmp[1], "pseudo":tmp[2]})

    return render_template("/film.html", c = commentaires, film=film)


@app.route("/commentaires/send/<int:idFilm>", methods=["POST"])
def insert_com(idFilm):

    global texte
    global pseudo

    if(request.method == 'POST'):
        texte = request.form["texte"]
        pseudo = request.form["pseudo"]
        

    mycursor.execute('''INSERT INTO Commentaire(texte, pseudo, idFilm) VALUES (%s, %s, %s)''', (texte, pseudo, idFilm))
    mydb.commit()

    return redirect(f"/films/{idFilm}")

# @app.route("/films/<int:idFilm>")

@app.route("/delete/<string:titre>+<int:annee>")
def delete_film(titre, annee):
    mycursor.execute('''DELETE from Film WHERE titre = %s AND anneSortie = %s''', (titre, annee))
    mydb.commit()
    return redirect("/films")

# @app.route("/update/<string:titre>+<int:annee")
# def update_film(titre, annee):


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)