from pymongo import MongoClient
from config import Config
uri="mongodb+srv://stocksalesdata:9zZ1k5obkbfK4ER7@solardb.ykgyl2r.mongodb.net/?retryWrites=true&w=majority&appName=SolarDB"
client = MongoClient(uri)
db = client['solar']


