# -*- coding: utf-8 -*-

import mysql.connector
from flask import Flask,request,session,    render_template,jsonify,abort, redirect
from flask_cors import CORS
import random
import hashlib 

app = Flask(__name__)
app.secret_key = 'filmsweb'
CORS(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="FilmsWeb",
    password="password",
    database="FilmsWeb"
)

mycursor = mydb.cursor()

films = []
commentaires=[]

@app.route("/")
def index():
    return redirect("/films")

def utilisateur_connecte(fonction):
    def verifie_connexion():
        if 'username' in session:
            # L'utilisateur est connecté, exécutez la route protégée
            return fonction()
        else:
            # L'utilisateur n'est pas connecté, redirigez-le vers la page de connexion
            return redirect('/login')
    return verifie_connexion

@app.route("/profil")
@utilisateur_connecte
def profil_user():

    films.clear()

    mycursor.execute('''SELECT * FROM Film WHERE creator = %s ORDER BY created_at DESC''', (session['idUser'],))

    for tmp in mycursor:

        films.append({"idFilm": tmp[0], "titre":tmp[1], "duree":tmp[2], "annee":tmp[3], "synopsis":tmp[4], "genre":tmp[5], "creator":tmp[7]})

    return render_template("profil.html", films = films)


@app.route("/saisie_film")
@utilisateur_connecte
def form_films():
    return render_template("formulaire_film.html")

@app.route("/film/send", methods=["POST"])
@utilisateur_connecte
def insert_film():

    global nom_film
    global duree
    global annee
    global synopsis
    global genre

    if(request.method == 'POST'):
        nom_film = request.form["nom"]
        duree = request.form["duree"]
        annee = request.form["année"]
        synopsis = request.form["synopsis"]
        genre = request.form["genres"]
        

    user_id = session['idUser']
    print(user_id)
    mycursor.execute('''INSERT INTO Film(titre, duree, anneSortie, synopsis, genre, creator) VALUES (%s, %s, %s, %s, %s,%s)''', (nom_film, duree, annee, synopsis, genre,user_id))
    mydb.commit()

    return redirect("/films")

@app.route("/films")
def display_films():

    films.clear()

    mycursor.execute('''SELECT * FROM Film ORDER BY created_at DESC''')

    for tmp in mycursor:

        films.append({"idFilm": tmp[0], "titre":tmp[1], "duree":tmp[2], "annee":tmp[3], "synopsis":tmp[4], "genre":tmp[5], "creator":tmp[7]})

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

        commentaires.append({"texte":tmp[1], "pseudo":tmp[2], "created_at":tmp[3]})

    return render_template("/film.html", c = commentaires, film=film)


@app.route("/commentaires/send/<int:idFilm>+<string:username>", methods=["POST"])
@utilisateur_connecte
def insert_com(idFilm, username):

    global texte
    global pseudo

    if(request.method == 'POST'):
        texte = request.form["texte"]
        pseudo = username
        

    mycursor.execute('''INSERT INTO Commentaire(texte, pseudo, idFilm) VALUES (%s, %s, %s)''', (texte, pseudo, idFilm))
    mydb.commit()

    return redirect(f"/films/{idFilm}")

# @app.route("/films/<int:idFilm>")

@app.route("/delete/<string:titre>+<int:annee>")
@utilisateur_connecte
def delete_film(titre, annee):
    mycursor.execute('''DELETE from Film WHERE titre = %s AND anneSortie = %s''', (titre, annee))
    mydb.commit()
    return redirect("/films")

@app.route("/update/<string:titre>+<int:annee>")
@utilisateur_connecte
def update_film(titre, annee):
    mycursor.execute('''SELECT * from Film WHERE titre = %s AND anneSortie = %s''', (titre, annee))
    film = mycursor.fetchone()
    return render_template("formulaire_film_modif.html", f = film)

@app.route("/update/send/<int:id>", methods=["POST"])
@utilisateur_connecte
def send_update_film(id):

    global nom_film
    global duree
    global annee
    global synopsis
    global genre 


    if(request.method == 'POST'):
        nom_film = request.form["nom"]
        duree = request.form["duree"]
        annee = request.form["année"]
        synopsis = request.form["synopsis"]
        genre = request.form["genres"]

    mycursor.execute('''UPDATE Film SET titre=%s, duree=%s, anneSortie=%s, synopsis=%s, genre=%s WHERE idFilm=%s''', (nom_film, duree, annee, synopsis, genre, id))
    mydb.commit()

    return redirect("/films")

@app.route("/inscription")
def return_insc():
    return render_template("formulaire_insc.html")

@app.route("/connexion")
def return_connexion():
    return render_template("formulaire_user_connect.html")

@app.route('/inscription/send', methods=['POST'])
def insert_user():
    nom = request.form["nom"]
    prenom = request.form["prénom"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    #A FAIRE POUR VERIFIER SI LE COMPTE EXISTE DEJA
    #user = query.filter_by(email=email).first()
    #if user: 
    #    return redirect(url_for('auth.signup'))
    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    pwd_hash=hasher.hexdigest()
    
    #jsp si le password fonctionne
    mycursor.execute(f"INSERT INTO Utilisateur (nom, prenom, pseudo, mail, mdp) VALUES ('{nom}', '{prenom}', '{username}', '{email}', '{pwd_hash}')")
    mydb.commit()

    # return render_template('formulaire_insc.html')
    return redirect('/films')

@app.route('/connexion/send', methods=["POST"])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    hasher = hashlib.sha256()
    hasher.update(password.encode('utf-8'))
    pwd_hash=hasher.hexdigest()

    mycursor.execute("SELECT * FROM Utilisateur WHERE mail = %s AND mdp = %s LIMIT 0,1", (email, pwd_hash))
    user = mycursor.fetchone()

    if user:
        session['username'] = user[2]  # Supposons que le nom d'utilisateur soit enregistré à l'index 1
        session['idUser'] = user[0]
        session['pseudo'] = user[3]
        print(session['pseudo'])
        return redirect('/')
    else:
            return "Identifiants invalides. Veuillez réessayer."

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')



@app.route('/page-securisee')
@utilisateur_connecte
def page_securisee():
    return "Ceci est une page sécurisée. L'utilisateur doit être connecté pour y accéder."


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)