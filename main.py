import sys
import threading
from queue import Queue
from spider import Spider
from domain import *
from utils import *


class Main:
    def __init__(self, url):
        self.NUMBER_OF_THREADS = 8
        self.url = url
        self.queue_file = self.get_website_name(url) + '/queue.txt'
        self.crawled_file = self.get_website_name(url) + '/crawled.txt'
        self.queue = Queue()
        self.crawl = self.crawl(self.queue_file, self.queue)
        self.create_jobs = self.create_jobs(self.queue_file, self.queue)

    @staticmethod
    def get_website_name(url):
        return get_domain_name(url).split('.')[0]

    def run(self):
        Spider(self.PROJECT_NAME, self.HOMEPAGE, self.DOMAIN_NAME)
        self.crawl = self.crawl(self.queue_file, self.queue)
        self.create_workers = self.create_workers(
            self.NUMBER_OF_THREADS, self.work)

    def create_workers(self, NUMBER_OF_THREADS, work):
        for _ in range(NUMBER_OF_THREADS):
            t = threading.Thread(target=work)
            t.daemon = True
            t.start()

    def work(self, queue):
        while True:
            url = queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            queue.task_done()

    def create_jobs(self, QUEUE_FILE, queue):
        for link in file_to_set(QUEUE_FILE):
            queue.put(link)
        queue.join()
        self.crawl(QUEUE_FILE)

    def crawl(self, QUEUE_FILE, queue):
        queued_links = file_to_set(QUEUE_FILE)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + ' links in the queue')
            self.create_jobs(QUEUE_FILE, queue)

