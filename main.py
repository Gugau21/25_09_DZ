import sqlite3
import random

from flask import Flask
from faker import Faker

app = Flask(__name__)
fake = Faker()


@app.route("/", methods=["GET"])
def index():
    return "Main"


@app.errorhandler(404)
def page_not_found(error):
    return "О ні, сторінка не знайдена!", 404


@app.route("/names/", methods=["GET"])
def names():
    con = sqlite3.connect("tables.db")
    cur = con.cursor()
    try:
        unique_names = cur.execute(
            "SELECT COUNT(DISTINCT first_name) FROM customers"
        ).fetchone()[0]
        text = str(unique_names)
    except sqlite3.OperationalError:
        return "Table does not exist"
    con.commit()
    return "Number of unique names: " + text


@app.route("/tracks/", methods=["GET"])
def tracks():
    con = sqlite3.connect("tables.db")
    cur = con.cursor()
    try:
        text = str(cur.execute("SELECT COUNT(ID) FROM tracks").fetchone()[0])
    except sqlite3.OperationalError:
        return "Table does not exist"
    con.commit()
    return "Number of tracks: " + text


@app.route("/tracks-sec/", methods=["GET"])
def tracks_sec():
    con = sqlite3.connect("tables.db")
    cur = con.cursor()
    try:
        text = (
            "Sum of song lengths: "
            + str(cur.execute("SELECT SUM(length_in_sec) FROM tracks").fetchone()[0])
            + " sec<br>Tracks:<br>"
        )
        for row in cur.execute("SELECT * FROM tracks"):
            text += " ".join(map(str, row)) + "<br>"
    except sqlite3.OperationalError:
        return "Table does not exist"
    con.commit()
    return text


@app.route("/create_table/", methods=["GET"])
def create_table():
    con = sqlite3.connect("tables.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS customers "
        "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        "first_name CHAR(255) NOT NULL, "
        "last_name CHAR(255));"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS tracks "
        "(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
        "artist CHAR(255) NOT NULL, "
        "length_in_sec int NOT NULL, "
        "release_date DATE NOT NULL);"
    )
    con.commit()
    return "Table created"


@app.route("/fill_table/", methods=["GET"])
def fill_table():
    con = sqlite3.connect("tables.db")
    cur = con.cursor()
    try:
        for id in range(200):
            name = fake.name().split(" ")
            cur.execute(
                "INSERT INTO customers (first_name, last_name) VALUES(?, ?)",
                (name[0], name[1]),
            )
        for id in range(200):
            artist = fake.name()
            length_in_sec = random.randint(60, 180)
            release_date = fake.date()
            cur.execute(
                "INSERT INTO tracks (artist, length_in_sec, release_date)VALUES(?, ?, ?)",
                (artist, length_in_sec, release_date),
            )
    except sqlite3.OperationalError:
        return "Table does not exist"
    con.commit()
    return "Table filled"


if __name__ == "__main__":
    app.run()
