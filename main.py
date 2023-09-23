import threading
from queue import Queue
from spider import Spider
from domain import get_domain_name
from utils import file_to_set

class CrawlerManager:
    def __init__(self, base_url: str):
        self.NUMBER_OF_THREADS = 20
        self.base_url = base_url
        self.website_name = self._get_website_name(base_url)
        self.queue_file = f"Data/{self.website_name}/queue.txt"
        self.crawled_file = f"Data/{self.website_name}/crawled.txt"
        self.queue = Queue()
        self.spider = Spider(self.website_name, self.base_url, get_domain_name(self.base_url))

    @staticmethod
    def _get_website_name(url: str) -> str:
        return get_domain_name(url).split('.')[0]

    def run(self):
        """Start the crawling process."""
        self._create_workers()
        self._process_queue()

    def _create_workers(self):
        """Create worker threads."""
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self._work)
            t.daemon = True
            t.start()

    def _work(self):
        """Define the work each thread should do."""
        while True:
            url = self.queue.get()
            self.spider.crawl_page(threading.current_thread().name, url)
            self.queue.task_done()

    def _create_jobs(self):
        """ Fill the queue with tasks"""
        for link in file_to_set(self.queue_file):
            self.queue.put(link)
        self.queue.join()
        self._process_queue()

    def _process_queue(self):
        """ Process queue util it is empty"""
        while file_to_set(self.queue_file):
            self._create_jobs()

if __name__ == "__main__":
    CrawlerManager('https://google.com').run()
