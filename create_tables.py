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

mycursor.execute(''' create table Utilisateur (idUser int primary key auto_increment, nom varchar(50), prenom varchar(50), pseudo varchar(50), mail varchar(50), mdp varchar (256))''')

mycursor.execute('''create table Film (idFilm int primary key auto_increment,  titre varchar(50), duree int, anneSortie int, synopsis varchar(140), genre varchar(50), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, creator int, CONSTRAINT fk_idUser FOREIGN KEY (creator) REFERENCES Utilisateur(idUser))''')

# mycursor.execute('''create table AVu(idFilm int, idUser int, CONSTRAINT fk_idFilm FOREIGN KEY (idFilm) REFERENCES Film(idFilm), CONSTRAINT fk_idUser FOREIGN KEY (idUser) REFERENCES Utilisateur(idUser))''')

# mycursor.execute('''create table AAime(idFilm int, idUser int, CONSTRAINT fk_idFilm2 FOREIGN KEY (idFilm) REFERENCES Film(idFilm), CONSTRAINT fk_idUser2 FOREIGN KEY (idUser) REFERENCES Utilisateur(idUser))''')

mycursor.execute('''create table Commentaire(idCom int primary key auto_increment, texte varchar(140), pseudo varchar(50), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, idFilm int, creator int, CONSTRAINT fk_idUser2 FOREIGN KEY (creator) REFERENCES Utilisateur(idUser), CONSTRAINT fk_idFilm3 FOREIGN KEY (idFilm) REFERENCES Film(idFilm) ON DELETE CASCADE)''')
#date ajout
mydb.commit()