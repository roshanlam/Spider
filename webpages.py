import glob
from bs4 import BeautifulSoup
import requests
from utils import *
from domain import *

def get_website_name(url):
    return get_domain_name(url).split('.')[0]

def remove_whitespace(sentence):
    return " ".join(sentence.split())

class Webpages:
    def __init__(self, url):
        self.url = url

    def download_content(self):
        directory = "./"
        pathname = directory + "/**/crawled.txt"
        files = glob.glob(pathname, recursive=True)
        for file in files:
            print(file)
            f = open(file, 'r')
            out = f.readlines()
            response = requests.get(out.strip())
            website = BeautifulSoup(response.text, 'lxml')
            title = website.find('title').text
            paragraph = ''
            h1 = ''
            h2 = ''
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

            title = remove_whitespace(title)
            paragraph = remove_whitespace(paragraph)
            header1 = remove_whitespace(h1)
            a = remove_whitespace(a)
            div = remove_whitespace(div)
            data_to_save = title + paragraph + header1 + a + div
            filename = get_website_name(out.strip()) + '.txt'
            filename_json = get_website_name(out.strip()) + '.json'
            data_to_save_json = {'filename': filename, 'url': out.strip()}
            write_file('NewData/'+filename, data_to_save)
            write_json_file('NewData/'+filename_json, data_to_save_json)
