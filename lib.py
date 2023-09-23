import logging

import aiohttp
from bs4 import BeautifulSoup
import requests
import hashlib
import redis
from pybloom_live import BloomFilter
import os
from scipy.stats import poisson
import numpy as np


class HTMLParser:
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.links = self.get_links()
        self.texts = self.get_texts()
        self.imgs = self.get_imgs()

    def get_links(self):
        links = self.soup.find_all('a')
        return [link.get('href') for link in links]

    def get_texts(self):
        return self.soup.get_text()

    def get_imgs(self):
        imgs = self.soup.find_all('img')
        return [img.get('src') for img in imgs]

    def has_popups(self) -> bool:
        pass


class DuplicatesPipeline:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.crawled_urls = BloomFilter(capacity=1000000, error_rate=0.01)
        self.crawled_content_hashes = BloomFilter(capacity=1000000, error_rate=0.01)

    def is_duplicate_url(self, url):
        if url in self.crawled_urls or self.redis_client.exists(f"url:{url}"):
            return True
        self.crawled_urls.add(url)
        self.redis_client.set(f"url:{url}", 1)
        return False

    def is_duplicate_content(self, content):
        fingerprint = self.simhash(content)
        if fingerprint in self.crawled_content_hashes or self.redis_client.exists(f"content:{fingerprint}"):
            return True
        self.crawled_content_hashes.add(fingerprint)
        self.redis_client.set(f"content:{fingerprint}", 1)
        return False

    def load_urls_from_data_folder(self):
        self._load_urls_from_data_folder()

    def _load_urls_from_data_folder(self):
        data_folder = 'Data'
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        pipeline = self.redis_client.pipeline()  # Create a Redis pipeline

        all_urls = set()

        # Collect all URLs from crawled.txt files
        for project_name in os.listdir(data_folder):
            project_path = os.path.join(data_folder, project_name)
            if os.path.isdir(project_path):
                crawled_file_path = os.path.join(project_path, 'crawled.txt')
                if os.path.exists(crawled_file_path):
                    try:
                        with open(crawled_file_path, 'r') as file:
                            for url in file:
                                url = url.strip()
                                if url:
                                    all_urls.add(url)
                    except IOError as e:
                        print(f"Error reading file {crawled_file_path}: {e}")

        # Check existence in Redis in batches
        batch_size = 1000  # or any other number that makes sense for your setup
        urls_list = list(all_urls)
        for i in range(0, len(urls_list), batch_size):
            batch = urls_list[i:i + batch_size]
            existing_urls = self.redis_client.mget([f"url:{url}" for url in batch])
            for j, exists in enumerate(existing_urls):
                if not exists:
                    pipeline.set(f"url:{batch[j]}", 1)

        pipeline.execute()  # Execute all the batched operations

    def _load_urls_from_redis(self):
        for key in self.redis_client.scan_iter("url:*"):
            url = key.decode().split(":", 1)[1]
            self.crawled_urls.add(url)

    def simhash(self, content):
        words = content.split()
        frequency = {}
        for word in words:
            frequency[word] = frequency.get(word, 0) + 1

        v = [0] * 256
        for word, freq in frequency.items():
            hashed = int(hashlib.sha3_256(word.encode()).hexdigest(), 16)
            for i in range(256):
                bitmask = 1 << i
                if hashed & bitmask:
                    v[i] += freq
                else:
                    v[i] -= freq

        fingerprint = 0
        for i in range(256):
            if v[i] >= 0:
                fingerprint += 1 << i
        return fingerprint


class QueuePipeline(DuplicatesPipeline):
    pass

# pipeline to use for any sitatuion where Naive Bayes is deemed as
# important to use
class NaiveBayes:
    pass

# Todo: Detect if webpage is scam or not, use Naive Bayes here to train
# model to see if webpage is scam.
class SpamDetector:
    def calc(self) -> int:
        return

    def is_spam(self) -> bool:
        return

# Todo: Implement Freshness of WebPages using Poisson Distrubution
class Freshness:
    def __init__(self, url):
        self.url = url
        self.previous_hash = None
        self.updates = 0

    async def get_content_hash(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    return hashlib.sha256(content.encode()).hexdigest()  # Using SHA-256
                else:
                    logging.error(f"Failed to retrieve {url}, status code: {response.status}")
                    return None

    def check_update(self):
        current_hash = self.get_content_hash()
        if self.previous_hash and self.previous_hash != current_hash:
            self.updates += 1
        self.previous_hash = current_hash

    def predict_updates(self, time_period, average_updates):
        average_updates = time_period * average_updates
        rv = poisson(average_updates)
        return rv.pmf(self.updates)

# Todo: Classify WebPage into categories. ex: [["url/": {
#   "url/something/something": ["Business", "News"],
# }]
class Classification:
    pass
