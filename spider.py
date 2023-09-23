from typing import Set, Deque
from bs4 import BeautifulSoup
from collections import deque
import threading
import asyncio
import aiohttp

from link_finder import LinkFinder
from domain import get_domain_name
from utils import create_project_dir, create_data_files, file_to_set, set_to_file
from lib import HTMLParser, DuplicatesPipeline

class Spider:
    def __init__(self, project_name: str, base_url: str, domain_name: str):
        self.project_name = project_name
        self.base_url = base_url
        self.domain_name = domain_name
        self.queue_file = f"Data/{self.project_name}/queue.txt"
        self.crawled_file = f"Data/{self.project_name}/crawled.txt"
        self.queue: Deque[str] = deque()
        self.crawled: Set[str] = set()
        self.duplicates_pipeline = DuplicatesPipeline()
        self.duplicates_pipeline.load_urls_from_data_folder()  # Load URLs from Data folder into Redis
        self.lock = threading.Lock()
        self.boot()

    def boot(self):
        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        self.queue = deque(file_to_set(self.queue_file))
        self.crawled = file_to_set(self.crawled_file)

    async def fetch(self, url, session):
        async with session.get(url) as response:
            return await response.text()

    async def gather_links_async(self, page_url: str) -> Set[str]:
        try:
            async with aiohttp.ClientSession() as session:
                html = await self.fetch(page_url, session)
                if html:
                    parser = HTMLParser(page_url)
                    return set(parser.links)
        except Exception as e:
            print(f"Error gathering links from {page_url}: {e}")
        return set()

    def gather_links(self, page_url: str) -> Set[str]:
        return asyncio.run(self.gather_links_async(page_url))

    def crawl_page(self, thread_name: str, page_url: str) -> None:
        print(f"{thread_name} now crawling {page_url}")
        print(f"Queue {len(self.queue)} | Crawled {len(self.crawled)}")
        self.add_links_to_queue(self.gather_links(page_url))
        with self.lock:
            self.crawled.add(page_url)
            self.update_files()

    def add_links_to_queue(self, links: Set[str]) -> None:
        for url in links:
            if url in self.crawled or url in self.queue:
                continue
            if self.domain_name != get_domain_name(url):
                continue
            with self.lock:
                self.queue.append(url)

    def update_files(self) -> None:
        set_to_file(set(self.queue), self.queue_file)
        set_to_file(self.crawled, self.crawled_file)
