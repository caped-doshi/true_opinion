import json

from flask import Flask

import web_scraper
import nlp

app = Flask(__name__)

@app.route('/movie_data')
def movie_data() -> dict:
    top_movies = 'https://www.metacritic.com/browse/movies/release-date/theaters/date'
    data = web_scraper.get_url_data(top_movies, 10)
    return { 'movie_data': str(data) }

@app.route('/movie_tweets')
def movie_tweets() -> dict:
    top_movies = 'https://www.metacritic.com/browse/movies/release-date/theaters/date'
    data = web_scraper.get_url_data(top_movies, 10)
    tweet_data = nlp.get_tweets(data)

    return str(tweet_data)