from queue import Queue
from domain import *
from bs4 import BeautifulSoup
import requests
from Exceptions.http import HTTP_GET_REQUEST_ERROR
from utils import *

def remove_whitespace(sentence):
    return " ".join(sentence.split())


class WebCrawler:
    def __init__(self, base_url):
        self.num_of_threads = 8
        self.base_url = base_url
        self.queue_file = self.get_website_name(self.base_url) + '/queue.txt'
        self.crawled_file = self.get_website_name(self.base_url) + '/crawled.txt'
        self.queue = Queue()
        self.depth = 10
        self.result = {}
        self.crawl()
        self.download_info()

    @staticmethod
    def get_website_name(url):
        return get_domain_name(url).split('.')[0]

    def crawl(self):
        try:
            response = requests.get(self.base_url)
        except HTTP_GET_REQUEST_ERROR:
            print('Failed to perform HTTP GET request on "%s"\n' % self.base_url)
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
        self.result = {
            'url': self.base_url,
            'title': remove_whitespace(title),
            'paragraph': remove_whitespace(paragraph),
            'header1': remove_whitespace(h1),
            'a': remove_whitespace(a),
            'div': remove_whitespace(div)
        }
        return self.result.values()

    def download_info(self):
        filename = self.get_website_name(self.base_url) + '.txt'
        data_to_save = self.result['title'] + ' ' + self.result['paragraph'] + self.result['a'] + self.result['header1'] + self.result['div']
        filename_json = self.get_website_name(self.base_url) + '.json'
        data_to_save_json = {'filename': filename, 'url': self.base_url}
        try:
            saveInfo('../Data/Txt', filename, data_to_save)
            saveInfoJson('../Data/Json', filename_json, data_to_save_json)
        except FileNotFoundError:
            os.mkdir('../Data/Txt')
            self.download_info()
print(WebCrawler('https://roshanlamichhane.tech'))