import asyncio
import aiohttp
import async_timeout
import logging
from typing import Optional
from utils import normalize_url
from link_finder import LinkFinder
from plugin import PluginManager
from storage import save_page

class Spider:
    def __init__(self, start_url: str, config: dict, plugin_manager: Optional[PluginManager] = None) -> None:
        """
        Initialize the Spider.

        :param start_url: The starting URL for crawling.
        :param config: Configuration dictionary.
        :param plugin_manager: Optional PluginManager for processing pages.
        """
        self.start_url = normalize_url(start_url)
        self.config = config
        self.visited = set()
        self.to_visit: asyncio.Queue[str] = asyncio.Queue()
        self.to_visit.put_nowait(self.start_url)
        self.plugin_manager = plugin_manager if plugin_manager else PluginManager()
        # Limit concurrent connections.
        self.semaphore = asyncio.Semaphore(10)

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """
        Fetch a URL asynchronously.

        :param session: The aiohttp session.
        :param url: The URL to fetch.
        :return: The response text if successful; None otherwise.
        """
        try:
            async with async_timeout.timeout(self.config['timeout']):
                headers = {'User-Agent': self.config['user_agent']}
                async with session.get(url, headers=headers) as response:
                    if response.status == 200 and 'text/html' in response.headers.get('Content-Type', ''):
                        return await response.text()
                    else:
                        logging.warning(f"Skipping URL {url}: status {response.status} or invalid content type")
                        return None
        except Exception as e:
            logging.error(f"Exception fetching {url}: {e}")
            return None

    async def process_url(self, session: aiohttp.ClientSession, url: str) -> None:
        """
        Process a single URL: fetch, process via plugins, save, and extract further links.

        :param session: The aiohttp session.
        :param url: The URL to process.
        """
        normalized_url = normalize_url(url)
        if normalized_url in self.visited:
            return
        self.visited.add(normalized_url)
        logging.info(f"Processing {normalized_url}")
        async with self.semaphore:
            content = await self.fetch(session, normalized_url)
        if content:
            # Process the content via plugins.
            processed_content = self.plugin_manager.run_plugins(normalized_url, content)
            # Save the content in the database.
            save_page(normalized_url, processed_content)
            # Extract and enqueue links.
            finder = LinkFinder(self.start_url, normalized_url)
            finder.feed(content)
            for link in finder.page_links():
                norm_link = normalize_url(link)
                if norm_link not in self.visited:
                    await self.to_visit.put(norm_link)

    async def crawl(self) -> None:
        """
        Begin the crawling process.
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            while not self.to_visit.empty():
                url = await self.to_visit.get()
                tasks.append(asyncio.create_task(self.process_url(session, url)))
                # Respect rate limits between requests.
                await asyncio.sleep(self.config['rate_limit'])
            if tasks:
                await asyncio.gather(*tasks)
