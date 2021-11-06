from flask import Flask
import time
import web_scraper

app = Flask(__name__)

@app.route('/movie_data')
def scrape_web():
    top_movies = 'https://www.metacritic.com/browse/movies/release-date/theaters/date'
    data = web_scraper.get_url_data(top_movies, 10)
    return { 'movie_data': str(data) }