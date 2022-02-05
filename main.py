import threading
from queue import Queue
from spider import Spider
from domain import *
from utils import *

def get_website_name(url):
        return get_domain_name(url).split('.')[0]

def remove_whitespace(sentence):
    return " ".join(sentence.split())

class Main:
    def __init__(self, base_url):
        self.PROJECT_NAME = get_website_name(base_url)
        self.HOMEPAGE = base_url
        self.DOMAIN_NAME = get_domain_name(self.HOMEPAGE)
        self.QUEUE_FILE = 'Data/' + self.PROJECT_NAME + '/queue.txt'
        self.CRAWLED_FILE = 'Data/' + self.PROJECT_NAME + '/crawled.txt'
        self.NUMBER_OF_THREADS = 8
        self.queue = Queue()
        Spider(self.PROJECT_NAME, self.HOMEPAGE, self.DOMAIN_NAME)
        self.create_workers()
        self.crawl()


    # Create worker threads (will die when main exits)
    def create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()


    # Do the next job in the queue
    def work(self):
        while True:
            url = self.queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            self.queue.task_done()


    # Each queued link is a new job
    def create_jobs(self):
        for link in file_to_set(self.QUEUE_FILE):
            self.queue.put(link)
        self.queue.join()
        self.crawl()


    # Check if there are items in the queue, if so crawl them
    def crawl(self):
        queued_links = file_to_set(self.QUEUE_FILE)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + ' links in the queue')
            self.create_jobs()
    
#Main('https://cnn.com')
#Main('https://www.bbc.com')
#Main('foxnews.com')

import glob
from bs4 import BeautifulSoup
import requests

def download_content():
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
download_content()
