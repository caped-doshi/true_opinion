from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH)

url = "https://www.rottentomatoes.com/search?search="
movie_name = "Eternals"

#manipulate the url
url += movie_name

driver.get(url)

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

#get the first element of the search results
ul = soup.find('ul', {'slot': 'list'})
element = ul.find('search-page-media-row')

print("Tomato meter score: " + element.attrs['tomatometerscore'])

driver.close()