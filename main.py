import csv

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
        return ("names")
    except:
        return ("Something went wrong")

@app.route("/tracks/", methods=['GET'])
def tracks():
    try:
        return ("tracks")
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
        return ("create_table")
    except:
        return ("Something went wrong")

@app.route("/fill_table/", methods=['GET'])
def fill_table():
    try:
        return ("fill_table")
    except:
        return ("Something went wrong")

if __name__ == "__main__":
    app.run()