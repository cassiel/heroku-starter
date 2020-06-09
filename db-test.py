import pymongo
import os

# DB_USER and DB_PASS aren't needed for CONNECTION_LOCAL, but the environment variables
# still need to be set.

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

myclient = pymongo.MongoClient(CONNECTION)

mydb = myclient[database]
mycol = mydb["customers"]
mydict = { "name": "Jim", "address": "Highway 999" }

# Add some data:
x = mycol.insert_one(mydict)

# Retrieve some data:
for x in mycol.find():
    print(x)
