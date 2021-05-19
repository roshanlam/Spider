import requests, pathlib
from bs4 import BeautifulSoup
import json
import requests

from .utils import save

def crawl(url, depth, filename):
    try:
        response = requests.get(url)
    except:
        print('Failed to perform HTTP GET request on "%s"\n' % url)
        return
    website = BeautifulSoup(response.text, 'lxml')
    try:
        title = website.find('title').text
        paragraph = ''
        h1 = ''
        a = ''
        div = ''
        for tag in website.findAll():
            if tag.name == 'p':
                paragraph += tag.text.strip().replace('\n', '')
            if tag.name == 'h1':
                h1 += tag.text.strip().replace('\n', '')
            if tag.name == 'a':
                a += tag.text.strip().replace('\n', '')
            if tag.name == 'div':
                div += tag.text.strip().replace('\n', '')
    except:
        return
    result = {
        'url': url,
        'title': title,
        'paragraph': paragraph,
        'header1' : h1,
        'a': a,
        'div' : div
    }
    return result.values()

info = crawl('https://roshanlamichhane.tech', 5, 'roshan')
print(info)
save("Data", "roshan", info)
