from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH, options=op)

url = 'https://www.imdb.com/search/title/?title_type=feature&year=2020-01-01,2020-12-31&view=simple'

driver.get(url)
next_button_exists = True

dictionary = {} #string for movie pointing to an int for score

counter = 0

while counter < 100:

    soup = BeautifulSoup(driver.page_source, "html.parser")
    titles = soup.find_all('div', {'class': 'col-title'})
    ratings = soup.find_all('div', {'class': 'col-imdb-rating'})

    processed_ratings = []
    processed_titles = []

    i = 0
    while i < len(ratings):
        rating = ratings[i]
        if len(rating.find_all('strong')) > 0:
            r = rating.find('strong').next
            r = r.replace(' ', '')
            r = r.replace('\n', '')
            processed_ratings.append(r)
        else:
            del ratings[i]
            del titles[i]
            i-=1
        i += 1
    for title in titles:
        t = title.find('a').contents[0]
        processed_titles.append(t)

    for i in range(0, len(processed_titles)):
        dictionary[processed_titles[i]] = str(processed_ratings[i])
    
    processed_ratings = []
    processed_titles = []
    
    print(counter)

    if len(driver.find_elements(By.LINK_TEXT, value='Next »')):
        next_button = driver.find_element(By.LINK_TEXT, value='Next »')
        counter += 1
        next_button.click()
    else:
        next_button_exists = False

json_obj = json.dumps(dictionary, indent=4)
with open("imdb.json", "w") as outfile:
    outfile.write(json_obj)
driver.close()

