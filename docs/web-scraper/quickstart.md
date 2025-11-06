# Web Scraper Plugin - Quick Start Guide

Get started with the WebScraperPlugin in just 3 simple steps!

## Step 1: Add the Plugin Import

Open `src/spider/main.py` and add the import at the top:

```python
from spider.plugins.web_scraper_plugin import WebScraperPlugin
```

Your imports should now look like this:

```python
import asyncio
import logging
from spider.config import config
from spider.spider import Spider
from spider.plugin import PluginManager
from spider.plugins.entity_extraction import EntityExtractionPlugin
from spider.plugins.real_time_metrics import RealTimeMetricsPlugin
from spider.plugins.dynamic_scraper import DynamicScraperPlugin
from spider.utils import init_logging
from spider.plugins.title_logger_plugin import TitleLoggerPlugin
from spider.plugins.web_scraper_plugin import WebScraperPlugin  # ← Add this line
```

## Step 2: Register the Plugin

In the `main()` function, add the plugin registration:

```python
def main() -> None:
    """
    Entry point for the crawler.
    """
    init_logging(logging.INFO)
    plugin_manager = PluginManager()

    # Register existing plugins
    plugin_manager.register(EntityExtractionPlugin())
    plugin_manager.register(RealTimeMetricsPlugin())
    plugin_manager.register(DynamicScraperPlugin())
    plugin_manager.register(TitleLoggerPlugin())

    # Register the Web Scraper Plugin
    plugin_manager.register(WebScraperPlugin())  # ← Add this line

    crawler = Spider(config['start_url'], config, plugin_manager)
    asyncio.run(crawler.crawl())
```

## Step 3: Run the Crawler

That's it! Now run your crawler:

```bash
poetry run python src/spider/main.py
```

The plugin will automatically:
- ✅ Extract all page metadata
- ✅ Analyze content structure
- ✅ Collect links and images
- ✅ Parse forms and inputs
- ✅ Extract structured data
- ✅ Store everything in PostgreSQL

## Verify It's Working

Check the logs for messages like:

```
INFO - Scraped https://example.com: 1250 words, 45 links, 12 images
INFO - Successfully saved scraped data for https://example.com
```

## Query Your Data

Create a simple script to query the scraped data:

```python
# test_scraper.py
from spider.plugins.scraper_utils import ScraperDataQuery

query = ScraperDataQuery()

# Get statistics
stats = query.get_page_statistics()
print(f"Total pages scraped: {stats['total_pages']}")
print(f"Average word count: {stats['average_word_count']}")

# Get a specific page
page = query.get_page_data("https://example.com")
if page:
    print(f"\nPage: {page['title']}")
    print(f"Word count: {page['word_count']}")
    print(f"Language: {page['language']}")
```

Run it:

```bash
poetry run python test_scraper.py
```

## Configuration (Optional)

You can customize the plugin behavior:

```python
plugin_manager.register(WebScraperPlugin(
    min_content_length=100,    # Only process pages with 100+ chars
    extract_full_text=False    # Set to True to extract full text content
))
```

## What Data Gets Collected?

For each page, the plugin extracts:

| Category | Data Points |
|----------|------------|
| **Metadata** | Title, description, keywords, author, canonical URL, language |
| **Content** | Word count, text length, headings (h1-h6), content blocks |
| **Links** | All links (internal/external) with anchor text |
| **Images** | Image URLs, alt text, dimensions |
| **Forms** | Form actions, methods, input fields |
| **Social** | OpenGraph and Twitter Card metadata |
| **Structured** | JSON-LD schema.org data |
| **Structure** | Semantic HTML5 elements analysis |

## Database Schema

The data is stored in the `scraped_data` table:

```sql
-- View your data
SELECT url, title, word_count, scraped_at
FROM scraped_data
ORDER BY scraped_at DESC
LIMIT 10;

-- Find pages with forms
SELECT url, title
FROM scraped_data
WHERE forms::text != '[]';

-- Search by keyword
SELECT url, title, description
FROM scraped_data
WHERE title ILIKE '%keyword%';
```

## Next Steps

1. **Read the full documentation**: See `WEB_SCRAPER_PLUGIN.md` for detailed usage
2. **Explore examples**: Check `examples/web_scraper_example.py` for code samples
3. **Query utilities**: Use the `ScraperDataQuery` class for easy data access

## Common Use Cases

### SEO Analysis
```python
from spider.plugins.scraper_utils import ScraperDataQuery
import json

query = ScraperDataQuery()
pages = query.get_all_pages()

for page in pages:
    headings = json.loads(page['headings'])
    if len(headings['h1']) == 0:
        print(f"⚠️ Missing H1: {page['url']}")
```

### Export Data
```python
query = ScraperDataQuery()
query.export_to_json("https://example.com", "data.json")
```

### Find Contact Forms
```python
pages_with_forms = query.get_pages_with_forms()
print(f"Found {len(pages_with_forms)} pages with forms")
```

## Troubleshooting

**Q: Plugin isn't scraping any data**

A: Check that:
- PostgreSQL is running and accessible
- Database URL is correct in `config.yaml`
- Pages have sufficient content (min 100 chars by default)

**Q: How do I see what was scraped?**

A: Check the logs or query the database:
```bash
poetry run python -c "from spider.plugins.scraper_utils import get_statistics; print(get_statistics())"
```

**Q: Can I scrape only specific pages?**

A: Yes! Override the `should_run()` method:
```python
class MyCustomScraper(WebScraperPlugin):
    async def should_run(self, url: str, content: str) -> bool:
        return '/blog/' in url  # Only scrape blog posts

plugin_manager.register(MyCustomScraper())
```

## Support

For more help:
- 📖 Full Documentation: `WEB_SCRAPER_PLUGIN.md`
- 💻 Code Examples: `examples/web_scraper_example.py`
- 🔧 Utility Functions: `src/spider/plugins/scraper_utils.py`

Happy scraping! 🚀
