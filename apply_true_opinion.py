from movie_tweets import Twitter_Query
from movie_review_model_test import Reconstructed_Model
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
load_dotenv()

uri = getenv('uri')

class True_Opinion:
    def __init__(self):
        client = MongoClient(uri)
        db = client.get_database("ratings")
        self.collection = db.get_collection("imdb")
        self.tq = Twitter_Query()
        self.rm = Reconstructed_Model("test.h5")

    def true_opinion_exists(self, movie_name: str):
        filter = {"_id": movie_name}
        cursor = self.collection.find({"$and":[filter,{ "true_opinion": { "$exists": True}}]})
        #check if a score already exists for the true opinion
        print(cursor.count())
        if cursor.count() == 0:
            return False
        else:
            return True
        
    
    def get_true_opinion(self,movie_name: str):
        filter = " -filter:retweets"
        self.pred_sentences = self.tq.query(movie_name+filter)
        true_opinion = self.rm.get_sentiment_analysis(self.pred_sentences)
        return true_opinion

    def set_true_opinion(self, movie_name:str):
        if not self.true_opinion_exists(movie_name):
            true_opinion = self.get_true_opinion(movie_name)
            new_val = {"$set": {'true_opinion': str(true_opinion)}}
            filter = {"_id": movie_name}
            self.collection.update_one(filter, new_val)
            print(true_opinion)

        
search = "Bloodshot"

t = True_Opinion()
t.set_true_opinion(search)