
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

# username = urllib.parse.quote_plus('arch9503')
# password = urllib.parse.quote_plus('Godlast95!@')   # ! : 33 / @ : 64
username = urllib.parse.quote_plus('TestUser')
password = urllib.parse.quote_plus('godlast')   # ! : 33 / @ : 64
chkParam = username + ":" + password
print(chkParam)

# uri = "mongodb://" + chkParam + "@cluster0.6ou1f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
uri = "mongodb+srv://" + chkParam + "@cluster0.6ou1f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

"""
from pymongo import MongoClient
import urllib.parse
username = urllib.parse.quote_plus('user')
username
'user'
password = urllib.parse.quote_plus('pass/word')
password
'pass%2Fword'
MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
"""