from pymongo import MongoClient
from config import Config
uri=Config.MONGO_URI
client = MongoClient(uri)
db = client['solar']


