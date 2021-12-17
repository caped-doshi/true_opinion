from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH)

url = 'https://www.rottentomatoes.com/top/bestofrt/?year=2021'

driver.get(url)

soup = BeautifulSoup(driver.page_source, "html.parser")

table = soup.find('table', {'class':'table'})

dictionary = {}
for tr in table.find_all('tr')[1:]:
    t = tr.find('a').contents[0]
    t = t.replace('\n', '')
    t = t.strip()
    title = t[:len(t)-7]
    date = t[len(t)-5:len(t)-1]

    score_span = tr.find('span', {'class': 'tMeterScore'})
    score = score_span.contents[0]

json_obj = json.dumps(dictionary, indent=4)
with open("rt.json", "w") as outfile:
    outfile.write(json_obj)
driver.close()