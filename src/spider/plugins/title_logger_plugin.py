import logging
from bs4 import BeautifulSoup
from plugin import Plugin

class TitleLoggerPlugin(Plugin):
    """
    A custom plugin that extracts the title from a crawled page and logs it.

    How It Works:
      1. Receives the URL and HTML content of a crawled page.
      2. Uses BeautifulSoup with the lxml parser to extract the <title> tag.
      3. Logs the title if found; otherwise, logs that no title was found.
      4. Returns the unmodified HTML content.
    """

    def process(self, url: str, content: str) -> str:
        """
        Process the crawled page content by extracting and logging the title.

        :param url: The URL of the crawled page.
        :param content: The HTML content of the page.
        :return: The original, unmodified content.
        """
        try:
            soup = BeautifulSoup(content, 'lxml')
            title_tag = soup.find('title')
            if title_tag and title_tag.string:
                title = title_tag.string.strip()
                logging.info(f"Page Title for {url}: {title}")
            else:
                logging.info(f"No title found for {url}")
        except Exception as e:
            logging.error(f"Error processing title for {url}: {e}")
        return content
