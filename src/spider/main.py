import asyncio
import logging
from spider.config import config
from spider.spider import Spider
from spider.plugin import PluginManager
from spider.plugins.entity_extraction import EntityExtractionPlugin
from spider.plugins.real_time_metrics import RealTimeMetricsPlugin
from spider.plugins.dynamic_scraper import DynamicScraperPlugin
from spider.utils import init_logging

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
