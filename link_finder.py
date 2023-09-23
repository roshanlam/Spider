from html.parser import HTMLParser
from urllib import parse
from typing import Set
import logging

class LinkFinder(HTMLParser):
    def __init__(self, base_url: str, page_url: str):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links: Set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self) -> Set[str]:
        return self.links

    def error(self, message: str) -> None:
        logging.error(f"Error encountered by the parser in {self.page_url}: {message}")
