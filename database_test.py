import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
load_dotenv()

cluster = MongoClient("mongodb+srv://arvind27kr:" + getenv('pw') + "@movie-data.pxrlp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["ratings"]
collection = db["imdb"]

post1 = {'_id': "avengers", "score": 7.9}
post2 = {'_id': "eternals", "score": 4.3}

post3 = {'_id': "all_movies", "arr": ['avengers', 'eternals']}

results = collection.insert_one(post3)