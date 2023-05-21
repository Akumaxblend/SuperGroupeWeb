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


mycursor.execute('''drop table if exists AVu CASCADE''')
mycursor.execute('''drop table if exists AAime CASCADE''')
mycursor.execute('''drop table if exists Commentaire CASCADE''')
mycursor.execute('''drop table if exists Film CASCADE''')
mycursor.execute('''drop table if exists Genre CASCADE''')
mycursor.execute('''drop table if exists Nationalite CASCADE''')
mycursor.execute('''drop table if exists Utilisateur CASCADE''')

mydb.commit()