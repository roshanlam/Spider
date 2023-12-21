import logging

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import requests
import hashlib
import redis
from pybloom_live import BloomFilter
import os
from scipy.stats import poisson
import numpy as np

import requests
import datetime
import difflib
from bs4 import BeautifulSoup
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import re
import time


class RateLimiter:
    def __init__(self, rate):
        self.rate = rate
        self.last_called = time.time()

    async def wait(self):
        time_since_last_call = time.time() - self.last_called
        sleep_time = max(0, (1 / self.rate))
        await asyncio.sleep(sleep_time - time_since_last_call)
        self.last_called = time.time()


def respect_robots_txt(url):
    try:
        robots_txt = requests.get(f'{url}/robots.txt').text
        if 'Disallow: /' in robots_txt:
            return False
        return True
    except requests.ReqeustException:
        return True


class ContentImportance:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.model.eval()

    def get_embedding(self, content):
        tokens = self.tokenizer(content, return_tensors='pt',
                                truncation=True, padding='max_length', max_length=512)
        with torch.no_grad():
            outputs = self.model(**tokens)
        return outputs['last_hidden_state'][:, 0, :].numpy()

    def calculate_importance_weight(self, content):
        sentences = [s.strip() for s in content.split('.') if s]
        content_embedding = self.get_embedding(content)
        sentence_embeddings = [self.get_embedding(
            sentence) for sentence in sentences]
        similarities = [cosine_similarity(content_embedding, sentence_embedding)[
            0][0] for sentence_embedding in sentence_embeddings]
        importance_weight = sum(similarities) / \
            len(sentences) if sentences else 0
        return importance_weight


class Freshness:
    def __init__(self):
        self.content_importance = ContentImportance()
        self.last_content = None
        self.last_modified_date = None

    def calculate_difference(self, old_content, new_content):
        s = difflib.SequenceMatcher(None, old_content, new_content)
        return s.ratio()

    def freshness_algorithm(self, old_content, new_content, last_modified_date):
        now = datetime.datetime.now()
        change_ratio = self.calculate_difference(old_content, new_content)
        days_since_modification = (
            now - last_modified_date).days if last_modified_date else 0
        time_decay = 1 / (1 + days_since_modification)
        importance_weight = self.content_importance.calculate_importance_weight(
            new_content)
        freshness_score = time_decay * change_ratio * importance_weight * 100
        return freshness_score

    async def check_update(self, new_content):
        freshness_score = None
        now = datetime.datetime.now()

        if self.last_content:
            freshness_score = self.freshness_algorithm(
                self.last_content, new_content, self.last_modified_date)

        self.last_content = new_content
        self.last_modified_date = now

        return freshness_score

    def predict_updates(self, time_period, average_updates):
        average_updates = time_period * average_updates
        rv = poisson(average_updates)
        return rv.pmf(self.updates)


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
        if self.soup.find_all('script', string=lambda text: 'popup' in text.lower()):
            return True
        return False


class DuplicatesPipeline:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.crawled_urls = BloomFilter(capacity=1000000, error_rate=0.01)
        self.crawled_content_hashes = BloomFilter(
            capacity=1000000, error_rate=0.01)

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
            existing_urls = self.redis_client.mget(
                [f"url:{url}" for url in batch])
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
    def add_to_queue(self, url):
        if not self.is_duplicate_url(url):
            self.crawled_urls.add(url)
            self.redis_client.set(f"url:{url}", 1)
            return True
        return False


# pipeline to use for any sitatuion where Naive Bayes is deemed as
# important to use


class NaiveBayes:
    pass

# Todo: Detect if webpage is scam or not, use Naive Bayes here to train
# model to see if webpage is scam.


class SpamDetector:
    def __init__(self, dataset):
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()
        self.dataset = dataset

    def train(self):
        X = self.vectorizer.fit_transform(self.dataset['content'])
        y = self.dataset['label']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2)
        self.classifier.fit(X_train, y_train)
        return self.classifier.score(X_test, y_test)

    def is_spam(self, content):
        content_vector = self.vectorizer.transform([content])
        return self.classifier.predict(content_vector)[0]
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
                    # Using SHA-256
                    return hashlib.sha256(content.encode()).hexdigest()
                else:
                    logging.error(
                        f"Failed to retrieve {url}, status code: {response.status}")
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
