import json
import twitter

with open('keys.key', 'r') as f:
    credentials = json.load(f)

api = twitter.Api(**credentials)

def get_queries(movie, delta_days, delta_months, delta_years) -> list[str]:
    months = [ 
        'January', 
        'February', 
        'March', 
        'April', 
        'May', 
        'June', 
        'July', 
        'August',
        'September',
        'November',
        'December'
    ]

    queries = []
    title = movie['title']
    date_tokens = movie['date'].split(' ')

    # Get the new month index
    old_month = months.index(date_tokens[0]) + 1
    old_day = int(date_tokens[1].replace(',', ''))
    old_year = int(date_tokens[2])
    
    old_date = str(old_year) + '-' + str(old_month) + '-' + str(old_day)

    # Get the new month, day, and year
    month = old_month + delta_months + 1
    if month > 12:
        month -= 12
    
    day = old_day + delta_days
    year = old_year + delta_years

    new_date = str(year) + '-' + str(month) + '-' + str(day)

    # Query since the release of the movie 
    # until that date plus a specified delta of time
    since_until = ' since:' + old_date + ' until:' + new_date

    queries.append(title + 'movie' + since_until)
    
    return queries

def get_tweets(movie_data, limit=10, delta_days=7, delta_months=0, delta_years=0) -> list[dict]:
    movie_tweets = []
    for movie in movie_data:
        queries = get_queries(movie, delta_days, delta_months, delta_years)

        i = 0
        for query in queries:
            if i > limit:
                break

            for tweet in api.GetSearch(query):
                movie_tweets.append({ movie['title']: tweet.text })
                i += 1
    
    return movie_tweets
