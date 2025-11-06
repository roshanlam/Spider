# Web Scraper Plugin Documentation

## Overview

The **WebScraperPlugin** is a comprehensive web scraping plugin for the Spider crawler that extracts and structures all important data from webpages. It automatically collects metadata, content, links, images, forms, and structured data, storing everything in a PostgreSQL database for easy querying and analysis.

## Features

### Data Extraction Capabilities

The plugin extracts the following data from each webpage:

#### 1. **Metadata**
- Page title
- Meta description
- Meta keywords
- Author information
- Canonical URL
- Language code
- Word count and text length

#### 2. **OpenGraph & Social Media**
- OpenGraph metadata (og:title, og:description, og:image, etc.)
- Twitter Card metadata
- Social sharing information

#### 3. **Content Structure**
- Headings hierarchy (h1-h6)
- Content blocks (articles, sections, main content)
- Paragraph analysis
- Word count per section

#### 4. **Links**
- All hyperlinks with anchor text
- Internal vs external link classification
- Link titles and attributes
- Absolute URLs resolved

#### 5. **Images**
- Image sources (absolute URLs)
- Alt text and titles
- Width and height attributes
- Image count and metadata

#### 6. **Forms**
- Form actions and methods
- Input fields with types
- Field names, IDs, and attributes
- Required field detection
- Textarea and select elements

#### 7. **Structured Data**
- JSON-LD schema.org data
- Microdata extraction
- Rich snippets information

#### 8. **Page Structure**
- Semantic HTML5 elements (header, footer, nav, aside, main)
- Article and section counts
- Table and list detection
- Overall page architecture

## Installation & Setup

### 1. Register the Plugin

Add the plugin to your Spider crawler in `main.py`:

```python
from spider.plugins.web_scraper_plugin import WebScraperPlugin

# Create plugin manager
plugin_manager = PluginManager()

# Register the web scraper plugin
plugin_manager.register(WebScraperPlugin(
    min_content_length=100,  # Minimum content length to process
    extract_full_text=False   # Whether to extract full text
))

# Pass the plugin manager to your Spider instance
spider = Spider(
    start_url="https://example.com",
    max_depth=3,
    plugin_manager=plugin_manager
)
```

### 2. Database Setup

The plugin automatically creates a `scraped_data` table in your PostgreSQL database with all necessary columns. Ensure your database configuration is set up correctly in `config.yaml`:

```yaml
database:
  url: postgresql://user:password@localhost:5432/spider_db
```

### 3. Run the Crawler

```bash
# Run with Poetry
poetry run python src/spider/main.py

# Or activate virtual environment first
poetry shell
python src/spider/main.py
```

## Usage Examples

### Basic Usage

```python
from spider import Spider
from spider.plugin import PluginManager
from spider.plugins.web_scraper_plugin import WebScraperPlugin

# Initialize plugin
scraper_plugin = WebScraperPlugin()

# Create plugin manager and register
plugin_manager = PluginManager()
plugin_manager.register(scraper_plugin)

# Create and run spider
spider = Spider(
    start_url="https://example.com",
    max_depth=2,
    plugin_manager=plugin_manager
)

await spider.crawl()
```

### Query Scraped Data

```python
from spider.plugins.scraper_utils import ScraperDataQuery

# Create query instance
query = ScraperDataQuery()

# Get data for a specific URL
page_data = query.get_page_data("https://example.com")
print(f"Title: {page_data['title']}")
print(f"Word Count: {page_data['word_count']}")
print(f"Links: {page_data['links']}")

# Search by title keyword
results = query.search_by_title("python")
for result in results:
    print(f"{result['url']}: {result['title']}")

# Get all external links from a page
external_links = query.get_external_links("https://example.com")
for link in external_links:
    print(f"{link['url']} - {link['text']}")

# Get images from a page
images = query.get_images("https://example.com")
for img in images:
    print(f"Image: {img['src']} (alt: {img['alt']})")

# Get OpenGraph metadata
og_data = query.get_opengraph_data("https://example.com")
print(f"OG Title: {og_data.get('title')}")
print(f"OG Description: {og_data.get('description')}")

# Get pages with forms
pages_with_forms = query.get_pages_with_forms()
print(f"Found {len(pages_with_forms)} pages with forms")

# Get statistics
stats = query.get_page_statistics()
print(f"Total Pages: {stats['total_pages']}")
print(f"Average Word Count: {stats['average_word_count']}")
```

### Convenience Functions

```python
from spider.plugins.scraper_utils import get_page_data, search_pages, get_statistics

# Quick page data retrieval
data = get_page_data("https://example.com")

# Quick search
results = search_pages("machine learning")

# Quick statistics
stats = get_statistics()
print(stats)
```

### Export Data to JSON

```python
from spider.plugins.scraper_utils import ScraperDataQuery

query = ScraperDataQuery()

# Export a single page's data to JSON
query.export_to_json(
    url="https://example.com",
    output_file="example_com_data.json"
)
```

### Advanced Queries

```python
from spider.plugins.scraper_utils import ScraperDataQuery

query = ScraperDataQuery()

# Find pages by word count range
long_articles = query.find_pages_by_word_count(min_words=1000, max_words=5000)
print(f"Found {len(long_articles)} articles between 1000-5000 words")

# Get all pages (with pagination)
all_pages = query.get_all_pages(limit=50, offset=0)

# Get headings structure
headings = query.get_headings_structure("https://example.com")
print(f"H1 headings: {headings['h1']}")
print(f"H2 headings: {headings['h2']}")

# Get JSON-LD structured data
structured = query.get_structured_data("https://example.com")
for item in structured:
    print(f"Type: {item.get('@type')}")
    print(f"Data: {item}")
```

### Analyze Page Structure

```python
from spider.plugins.scraper_utils import ScraperDataQuery
import json

query = ScraperDataQuery()
page_data = query.get_page_data("https://example.com")

# Analyze page structure
structure = json.loads(page_data['page_structure'])
print(f"Has header: {structure['has_header']}")
print(f"Has footer: {structure['has_footer']}")
print(f"Has navigation: {structure['has_nav']}")
print(f"Article count: {structure['article_count']}")
print(f"Section count: {structure['section_count']}")

# Analyze content blocks
content_blocks = json.loads(page_data['content_blocks'])
for block in content_blocks:
    print(f"Block type: {block['type']}")
    print(f"Word count: {block['word_count']}")
    print(f"Preview: {block['text'][:100]}...")
```

## Database Schema

The `scraped_data` table has the following structure:

```sql
CREATE TABLE scraped_data (
    url VARCHAR PRIMARY KEY,
    scraped_at TIMESTAMP NOT NULL,
    title TEXT,
    description TEXT,
    keywords TEXT,
    author VARCHAR,
    canonical_url VARCHAR,
    language VARCHAR,
    word_count INTEGER,
    text_length INTEGER,
    headings JSON,
    meta_tags JSON,
    opengraph JSON,
    twitter_card JSON,
    links JSON,
    images JSON,
    forms JSON,
    structured_data JSON,
    page_structure JSON,
    content_blocks JSON
);
```

## Use Cases

### 1. SEO Analysis
```python
# Analyze SEO metadata across multiple pages
query = ScraperDataQuery()
pages = query.get_all_pages(limit=100)

for page in pages:
    if not page['description'] or len(page['description']) < 50:
        print(f"⚠️ Short/missing description: {page['url']}")

    headings = json.loads(page['headings'])
    if len(headings['h1']) == 0:
        print(f"⚠️ No H1 heading: {page['url']}")
    elif len(headings['h1']) > 1:
        print(f"⚠️ Multiple H1 headings: {page['url']}")
```

### 2. Competitive Analysis
```python
# Analyze competitor websites
query = ScraperDataQuery()

competitor_url = "https://competitor.com"
page_data = query.get_page_data(competitor_url)

print(f"Content length: {page_data['word_count']} words")
print(f"Internal links: {len(json.loads(page_data['links'])['internal'])}")
print(f"External links: {len(json.loads(page_data['links'])['external'])}")
print(f"Images: {len(json.loads(page_data['images']))}")

# Get their OpenGraph strategy
og = json.loads(page_data['opengraph'])
print(f"Social media title: {og.get('title')}")
print(f"Social media image: {og.get('image')}")
```

### 3. Content Inventory
```python
# Build a content inventory
query = ScraperDataQuery()
pages = query.get_all_pages(limit=1000)

inventory = []
for page in pages:
    inventory.append({
        'url': page['url'],
        'title': page['title'],
        'word_count': page['word_count'],
        'has_forms': len(json.loads(page['forms'])) > 0,
        'language': page['language'],
        'last_scraped': page['scraped_at']
    })

# Export to CSV or analyze further
import csv
with open('content_inventory.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=inventory[0].keys())
    writer.writeheader()
    writer.writerows(inventory)
```

### 4. Link Graph Analysis
```python
# Build a link graph
query = ScraperDataQuery()
pages = query.get_all_pages(limit=500)

link_graph = {}
for page in pages:
    internal_links = json.loads(page['links'])['internal']
    link_graph[page['url']] = [link['url'] for link in internal_links]

# Find most linked-to pages
from collections import Counter
all_links = [link for links in link_graph.values() for link in links]
most_linked = Counter(all_links).most_common(10)

print("Top 10 most linked-to pages:")
for url, count in most_linked:
    print(f"{count} links -> {url}")
```

### 5. Form Detection for Lead Generation
```python
# Find pages with contact forms
query = ScraperDataQuery()
pages_with_forms = query.get_pages_with_forms()

contact_pages = []
for page in pages_with_forms:
    forms = json.loads(page['forms'])
    for form in forms:
        # Look for email or contact-related fields
        field_names = [inp['name'] for inp in form['inputs']]
        if any('email' in name.lower() or 'contact' in name.lower() for name in field_names):
            contact_pages.append({
                'url': page['url'],
                'title': page['title'],
                'form_action': form['action'],
                'fields': field_names
            })

print(f"Found {len(contact_pages)} pages with contact forms")
```

## Configuration Options

### Plugin Initialization Options

```python
WebScraperPlugin(
    min_content_length=100,    # Minimum HTML content length to process
    extract_full_text=False    # Extract complete page text (increases storage)
)
```

### Conditional Scraping

Override `should_run()` to control which pages to scrape:

```python
class SelectiveWebScraper(WebScraperPlugin):
    async def should_run(self, url: str, content: str) -> bool:
        # Only scrape blog posts
        if '/blog/' not in url:
            return False

        # Only scrape pages with sufficient content
        if len(content) < self.min_content_length:
            return False

        return True

# Use the selective scraper
plugin_manager.register(SelectiveWebScraper())
```

## Performance Considerations

- **Storage**: Each page typically requires 10-50 KB of database storage depending on content
- **Processing**: Plugin adds ~50-200ms of processing time per page
- **Memory**: Minimal memory overhead, processes one page at a time
- **Concurrency**: Fully async-compatible, works with concurrent crawling

## Troubleshooting

### Plugin Not Extracting Data

Check the logs for errors:
```bash
tail -f logs/spider.log | grep "WebScraperPlugin"
```

### Database Connection Issues

Verify your database configuration:
```python
from spider.config import config
print(config['database']['url'])
```

### Missing Data Fields

Some websites may not have all fields. Check for None values:
```python
page_data = query.get_page_data(url)
if page_data['description'] is None:
    print("No meta description found")
```

## Best Practices

1. **Filter URLs**: Use `should_run()` to only scrape relevant pages
2. **Monitor Storage**: Regularly check database size as data accumulates
3. **Export Important Data**: Use `export_to_json()` for backup and portability
4. **Respect Robots.txt**: Configure Spider to honor robots.txt rules
5. **Rate Limiting**: Use Spider's built-in rate limiting to avoid overloading servers

## API Reference

See `scraper_utils.py` for complete API documentation of the `ScraperDataQuery` class.

## License

This plugin is part of the Spider web crawler project.

## Support

For issues or questions, please refer to the main Spider project documentation.
