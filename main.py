import csv
import sqlite3
import random

from flask import  Flask
from faker import Faker

app = Flask(__name__)
fake = Faker()

@app.route("/", methods=['GET'])
def index():
    return 'Main'

@app.errorhandler(404)
def page_not_found(error):
    return 'О ні, сторінка не знайдена!', 404

@app.route("/names/", methods=['GET'])
def names():
    try:
        con = sqlite3.connect("tables.db")
        cur = con.cursor()
        text = ""
        for row in cur.execute("SELECT COUNT(DISTINCT first_name) FROM customers"):
            text += str(row[0])
        con.commit()

        return ("Number of unique names: " + text)
    except:
        return ("Something went wrong")

@app.route("/tracks/", methods=['GET'])
def tracks():
    try:
        con = sqlite3.connect("tables.db")
        cur = con.cursor()
        text = ""
        for row in cur.execute("SELECT COUNT(ID) FROM tracks"):
            text += str(row[0])
        con.commit()

        return ("Number of tracks: " + text)
    except:
        return ("Something went wrong")

@app.route("/tracks-sec/", methods=['GET'])
def tracks_sec():
    try:
        return ("tracks-sec")
    except:
        return ("Something went wrong")

@app.route("/create_table/", methods=['GET'])
def create_table():
    try:
        con = sqlite3.connect("tables.db")
        cur =  con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS customers "
                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "first_name CHAR(255) NOT NULL, "
                    "last_name CHAR(255));")
        cur.execute("CREATE TABLE IF NOT EXISTS tracks "
                    "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "artist CHAR(255) NOT NULL, "
                    "length_in_sec int NOT NULL, "
                    "release_date DATE NOT NULL);")
        con.commit()
        return ("create_table")
    except:
        return ("Something went wrong")

@app.route("/fill_table/", methods=['GET'])
def fill_table():
    try:
        con = sqlite3.connect("tables.db")
        cur = con.cursor()
        data = []
        for id in range(200):
            name = fake.name().split(" ")
            cur.execute("INSERT INTO customers (first_name, last_name) VALUES(?, ?)", (name[0], name[1]))
        for id in range(200):
            artist = fake.name()
            lengthInSec = random.randint(60, 180)
            releaseDate = fake.date()
            cur.execute("INSERT INTO tracks (artist, length_in_sec, release_date)VALUES(?, ?, ?)", (artist, lengthInSec, releaseDate))
        con.commit()
        return ("fill_table")
    except:
        return ("Something went wrong")

if __name__ == "__main__":
    app.run()