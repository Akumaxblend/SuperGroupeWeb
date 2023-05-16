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

# ------------------------------------------------------------------------------------------------------------------------------------
# Création des différentes tables 


mycursor.execute('''drop table if exists AVu CASCADE''')
mycursor.execute('''drop table if exists AAime CASCADE''')
mycursor.execute('''drop table if exists Commentaire CASCADE''')
mycursor.execute('''drop table if exists Film CASCADE''')
mycursor.execute('''drop table if exists Genre CASCADE''')
mycursor.execute('''drop table if exists Nationalite CASCADE''')
mycursor.execute('''drop table if exists Utilisateur CASCADE''')



mycursor.execute('''create table Genre (idGenre int primary key auto_increment, nomG varchar(50))''')

mycursor.execute('''create table Nationalite (idNationalite int primary key auto_increment, nomN varchar(50))''')

mycursor.execute('''create table Film (idFilm int primary key auto_increment,  titre varchar(50), duree int, anneSortie int, synopsis varchar(140), idGenre int, idNationalite int, CONSTRAINT fk_idgenre FOREIGN KEY (idGenre) REFERENCES Genre(idGenre), CONSTRAINT fk_idnationalite FOREIGN KEY (idNationalite) REFERENCES Nationalite(idNationalite))''')

mycursor.execute(''' create table Utilisateur (idUser int primary key auto_increment, nom varchar(50), prenom varchar(50), pseudo varchar(50), mail varchar(50), mdp varchar (50))''')

mycursor.execute('''create table AVu(idFilm int, idUser int, CONSTRAINT fk_idFilm FOREIGN KEY (idFilm) REFERENCES Film(idFilm), CONSTRAINT fk_idUser FOREIGN KEY (idUser) REFERENCES Utilisateur(idUser))''')

mycursor.execute('''create table AAime(idFilm int, idUser int, CONSTRAINT fk_idFilm2 FOREIGN KEY (idFilm) REFERENCES Film(idFilm), CONSTRAINT fk_idUser2 FOREIGN KEY (idUser) REFERENCES Utilisateur(idUser))''')

mycursor.execute('''create table Commentaire(idCom int primary key auto_increment, texte varchar(140), idFilm int, idUser int, CONSTRAINT fk_idFilm3 FOREIGN KEY (idFilm) REFERENCES Film(idFilm), CONSTRAINT fk_idUser3 FOREIGN KEY (idUser) REFERENCES Utilisateur(idUser))''')

mydb.commit()

# ------------------------------------------------------------------------------------------------------------------------------------

mycursor.execute('''insert into Genre values(2,'sf'), (3,'aventure'), (4,'policier')''')

mycursor.execute('''insert into Nationalite values(1, 'français'), (2, 'anglais'), (3, 'américain')''')

mycursor.execute('''insert into Film values (1, 'OSS 117', 120, 2012, 'rien rien tqt', 3, 1)''')

mydb.commit()


ajout = input("quel nom voulez vous ajouter ?")

mycursor.execute('''Insert into Genre values(5,%s)''',(ajout,))
mydb.commit()

# mycursor.execute('''Delete from etudiants where id = 2''')
# mydb.commit()

mycursor.execute('''select * from Genre''')
etuds = mycursor.fetchall()
mydb.commit()
print(etuds)

@app.route("/")
def index():
    
    #return ("<html><body><p1>Hello world</p1></body></html>")
    return render_template("liste.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)