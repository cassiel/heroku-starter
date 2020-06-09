from flask import Flask, request, render_template, jsonify, redirect
from flask_cors import CORS
import urllib.parse
import datetime
import os
import pymongo

# This is appatently needed for MongoDB Atlas ("+srv"), and not much documented;
# but doesn't help for Heroku deployment.
import dns

ON_HEROKU = "ON_HEROKU" in os.environ

if "DB_CLUSTER" in os.environ:
    cluster = os.environ["DB_CLUSTER"]
else:
    cluster = ""

if "DB_USER" in os.environ:
    user = os.environ["DB_USER"]
else:
    user = ""

if "DB_PASS" in os.environ:
    password = os.environ["DB_PASS"]
else:
    password = ""

database = os.environ["DB_NAME"]

# Local database:
CONNECTION_LOCAL="mongodb://localhost:27017/"

# MongoDB Atlas:
CONNECTION_ATLAS=\
    "mongodb+srv://%s:%s@%s.mongodb.net/%s?retryWrites=true&w=majority" \
    % (user, password, cluster, database)

CONNECTION=CONNECTION_ATLAS

print(CONNECTION)

myclient = pymongo.MongoClient(CONNECTION, connect=False)
mydb = myclient[database]
mycol = mydb["customers"]

app = Flask(__name__, static_url_path='', static_folder="static")
CORS(app)

@app.route('/')
def index():
    print(mycol.find_one())
    return render_template('index.html', data=mycol.find())
    #return render_template('index.html', data=[])

if (not ON_HEROKU) and __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
