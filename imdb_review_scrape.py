from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv
import random

op = webdriver.ChromeOptions()
op.add_argument('headless')

PATH = "C:\Program Files (x86)\chromedriver.exe" #path on your machine
driver = webdriver.Chrome(PATH, options=op)

urls = []

url_250 = "https://www.imdb.com/chart/top/?sort=us,desc&mode=simple&page=1"
driver.get(url_250)

s = BeautifulSoup(driver.page_source, "html.parser")
all_td = s.find_all('td', {'class': 'titleColumn'})

for td in all_td:
    a = td.find('a', href=True)
    id = a['href'][7:17]
    id = id.replace('/', '')
    review_url = 'https://www.imdb.com/title/' + id + '/reviews?ref_=tt_urv'
    urls.append(review_url)



i = 6
a = 0
b = 0

all_reviews = []

for url in urls:
    #url = url[:37] + 'reviews?' + url[38:]
    driver.get(url)

    star_nums = Select(driver.find_element(By.XPATH, value='//*[@id="main"]/section/div[2]/div[1]/form/div/div[3]/select'))
    stars = [x.text for x in driver.find_elements(By.TAG_NAME, value="option")]
    i = 6
    while i < 16:
        # go to the number of stars
        star_nums.select_by_visible_text(stars[i])

        # keep loading more reviews
        if(len(driver.find_elements(By.ID, value="load-more-trigger")) > 0): 
            load_more_button = driver.find_element(By.ID, value="load-more-trigger")
            while(load_more_button.is_displayed()):
                load_more_button.click()
                load_more_button = driver.find_element(By.ID, value="load-more-trigger")

        star_nums = Select(driver.find_element(By.XPATH, value='//*[@id="main"]/section/div[2]/div[1]/form/div/div[3]/select'))
        stars = [x.text for x in driver.find_elements(By.TAG_NAME, value="option")]
        i += 1
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        list_items = soup.find_all('div', {'class' :'show-more__control'})
        for list in list_items:
            content_text = list.text
            content_text = content_text.replace('\n', '')
            if(len(content_text) > 0):
                temp_ar = [content_text, i-6]
                all_reviews.append(temp_ar)
                a+=1
    b+= 1
    print(b)
    print(a)

random.shuffle(all_reviews)

with open('reviews.csv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['text', 'review'])
    writer.writerows(all_reviews)





    
