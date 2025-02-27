import logging
from typing import Any

class Plugin:
    def process(self, url: str, content: Any) -> Any:
        """
        Process the crawled page content.

        :param url: URL of the page.
        :param content: Content to process.
        :return: Processed content.
        """
        return content

class PluginManager:
    def __init__(self) -> None:
        """
        Initialize the PluginManager.
        """
        self.plugins: list[Plugin] = []

    def register(self, plugin: Plugin) -> None:
        """
        Register a plugin for processing crawled pages.

        :param plugin: An instance of a Plugin.
        """
        self.plugins.append(plugin)
        logging.info(f"Registered plugin: {plugin.__class__.__name__}")

    def run_plugins(self, url: str, content: Any) -> Any:
        """
        Run all registered plugins on the given content.

        :param url: The URL associated with the content.
        :param content: The content to process.
        :return: Processed content after all plugins have been applied.
        """
        for plugin in self.plugins:
            try:
                content = plugin.process(url, content)
            except Exception as e:
                logging.error(f"Error in plugin {plugin.__class__.__name__} for {url}: {e}")
        return content
