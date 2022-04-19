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
    
Main('https://cnn.com')
Main('https://www.bbc.com')
Main('foxnews.com')
