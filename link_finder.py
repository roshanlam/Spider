from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Set

class LinkFinder:
    def __init__(self, base_url: str, page_url: str) -> None:
        """
        Initialize the LinkFinder.

        :param base_url: The base URL to resolve relative links.
        :param page_url: The URL of the page being parsed.
        """
        self.base_url = base_url
        self.page_url = page_url
        self.links: Set[str] = set()

    def feed(self, html: str) -> None:
        """
        Parse HTML content and extract links.

        :param html: HTML content as a string.
        """
        soup = BeautifulSoup(html, 'lxml')
        for tag in soup.find_all('a', href=True):
            absolute_link = urljoin(self.base_url, tag['href'])
            self.links.add(absolute_link)

    def page_links(self) -> Set[str]:
        """
        Get the set of extracted links.

        :return: A set of URLs.
        """
        return self.links
