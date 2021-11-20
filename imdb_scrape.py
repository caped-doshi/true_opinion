from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH)

url = "https://www.imdb.com/"

driver.get(url)
#currently at the main page

movie_name = "Avengers"

search = driver.find_element(By.ID,"suggestion-search")

search.send_keys(movie_name)
#search for the movie

search_button = driver.find_element(By.ID,"suggestion-search-button")
search_button.click()
#click search

#Select the first title
td = driver.find_elements(By.CLASS_NAME, "result_text")[0]

#select the link for the movie
link_text = td.find_element(By.CSS_SELECTOR,'a').text
movie_link = driver.find_element(By.LINK_TEXT, link_text)
#click the link
movie_link.click()

#imdb is out of 10 stars
ratings = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div[1]/a')
ratings_link = driver.find_element(By.LINK_TEXT,ratings.text)
ratings_link.click()

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

#get the first value of the table
text_div = soup.find('div', {'class': "bigcell"})
print(text_div.text) #works

#print(stars.text + "out of 10 stars")
driver.back()
driver.close()