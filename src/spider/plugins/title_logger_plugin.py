import logging
from bs4 import BeautifulSoup
from spider.plugin import Plugin

class TitleLoggerPlugin(Plugin):
    async def should_run(self, url: str, content: str) -> bool:
        return True

    async def process(self, url: str, content: str) -> str:
        """
        Extracts the <title> tag from the HTML content using BeautifulSoup (with lxml)
        and logs the title if found. Otherwise, logs that no title was found.
        Returns the unmodified content.
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
