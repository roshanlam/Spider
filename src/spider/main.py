import asyncio
import logging
from config import config
from spider import Spider
from plugin import PluginManager
from plugins.entity_extraction import EntityExtractionPlugin
from plugins.real_time_metrics import RealTimeMetricsPlugin
from plugins.dynamic_scraper import DynamicScraperPlugin
from utils import init_logging

def main() -> None:
    """
    Entry point for the crawler.
    """
    init_logging(logging.INFO)
    plugin_manager = PluginManager()
    # Register custom plugins here, e.g.:
    plugin_manager.register(EntityExtractionPlugin())
    plugin_manager.register(RealTimeMetricsPlugin())
    plugin_manager.register(DynamicScraperPlugin())
    crawler = Spider(config['start_url'], config, plugin_manager)
    asyncio.run(crawler.crawl())

if __name__ == '__main__':
    main()
