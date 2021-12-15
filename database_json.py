import json
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
load_dotenv()

uri = getenv('uri')

client = MongoClient(uri)
db = client.get_database("ratings")
collection = db.get_collection("imdb")

d = {}
with open('imdb.json') as json_file:
    d = json.load(json_file)

def find_by_id(id):
    cursor = collection.find({'_id':id})
    return cursor

def update_array(id):
    cursor = collection.update({'_id':'all_movies'}, {'$addToSet': {"arr": id}})
    return 

def process_dict(dictionary):
    for title in dictionary:
        imdb_rating = dictionary[title]
        result = find_by_id(title)
        
        #check if result already exists
        if(result.count() == 0):
            post = {"_id": title, "imdb": imdb_rating}
            collection.insert_one(post)
        else:
            new_val = {"$set": {"imdb": imdb_rating}}
            collection.update_one({"_id":title}, new_val)
        update_array(title)
        
        

process_dict(d)