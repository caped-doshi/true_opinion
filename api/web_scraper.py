import json
import ssl

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_content(url) -> BeautifulSoup:
    req = Request(url, headers={ 'User-Agent': 'Moazilla/5.0' })
    page = urlopen(req).read()
    
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def get_data(tr) -> dict:
    data = {}

    a = tr.find('a', attrs={ 'class': 'title' })
    if a != None:
        data['title'] = a.find('h3').text
    
    div = tr.find('div', attrs={ 'class': 'clamp-details' })
    if div != None:
        data['date'] = div.find('span').text

    return data

def get_url_data(url, num_searches) -> list[dict]:
    content = get_content(url)

    tables = content.findAll('table', attrs={ 'class': 'clamp-list' })

    all_data = []

    i = 0
    for table in tables:
        for tr in table.findAll('tr'):
            data = get_data(tr)
            if len(data) > 0:
                all_data.append(data)
                i += 1
            
            if i >= num_searches:
                tables.clear()
                break

    return all_data
