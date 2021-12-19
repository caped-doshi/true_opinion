#Importing Libraries required to run this program
import tweepy
import pandas as pd
import requests
import json 
from langdetect import detect
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
load_dotenv()

#Assign keys required to access the Twitter API
class Twitter_Query:
    def __init__(self):
        self.consumer_key = getenv('consumer_key')
        self.consumer_secret = getenv('consumer_secret')
        self.access_token=getenv('access_token')
        self.access_token_secret=getenv('access_token_secret')
        self.bearer_token = getenv('bearer_token')

        self.auth= tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        self.auth.set_access_token(self.access_token,self.access_token_secret)

        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def query(self, query: str):
        tweets_list = tweepy.Cursor(self.api.search_tweets, q=query, lang='en', since_id=0).items(100)
        i = 0
        tweets = list()
        for tweet in tweets_list:
            i += 1
            text = tweet.text
            tweets.append(text)
            favourite_count = tweet.favorite_count
            retweet_count = tweet.retweet_count
            created_at = tweet.created_at
            line = {'text' : text, 'favourite_count' : favourite_count, 'retweet_count' : retweet_count, 'created_at' : created_at}
        return tweets
        
