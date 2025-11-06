# 🕷️ Spider

<p align="center">
  <img src="spider.png" />
</p>

<p align="center">
  <strong>A modern, scalable, and extensible web crawler for efficient distributed crawling and data extraction</strong>
</p>

<p align="center">
  Built with asynchronous I/O, plugin architecture, and distributed task processing
</p>

---

## ✨ Features

### Core Capabilities
- **🚀 Asynchronous Crawling** - Non-blocking I/O with `aiohttp` and `asyncio` for high performance
- **🌐 Distributed Processing** - Scale across multiple workers using Celery and Redis
- **💾 Database Persistence** - PostgreSQL storage with SQLAlchemy ORM
- **🔌 Plugin Architecture** - Extensible system for custom data processing
- **📊 Robust Logging** - Console, file, and database logging for diagnostics
- **🔗 URL Normalization** - Smart deduplication and link management

### Included Plugins
- **🕸️ Web Scraper** - Comprehensive webpage data extraction
- **📝 Title Logger** - Extract and store page titles
- **🤖 Entity Extraction** - NLP-based named entity recognition (spaCy)
- **🎭 Dynamic Scraper** - JavaScript-rendered pages (Playwright)
- **📈 Real-time Metrics** - Live crawl statistics via WebSocket

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis

### Installation

```bash
# Clone repository
git clone https://github.com/roshanlam/spider.git
cd spider

# Install with Poetry (recommended)
poetry install

# Install Playwright browsers
poetry run playwright install chromium

# Download spaCy model
poetry run python -m spacy download en_core_web_sm
```

### Configuration

Edit `src/spider/config.yaml`:

```yaml
start_url: "http://example.com"
rate_limit: 1  # seconds between requests
threads: 8
timeout: 10

database:
  url: "postgresql://username@localhost/crawlerdb"

celery:
  broker_url: "redis://localhost:6379/0"
  result_backend: "redis://localhost:6379/0"
```

### Run the Crawler

**Simple way:**
```bash
poetry run python run.py
```

**Or using module:**
```bash
poetry run python -m spider.main
```

### Query Scraped Data

```bash
# View all scraped data
poetry run python query_data.py

# Or programmatically
poetry run python
>>> from spider.plugins.scraper_utils import ScraperDataQuery
>>> query = ScraperDataQuery()
>>> page = query.get_page_data("http://example.com")
>>> print(page['title'])
```

---

## 📦 Project Structure

```
spider/
├── src/spider/
│   ├── spider.py           # Core async crawler
│   ├── plugin.py           # Plugin system
│   ├── storage.py          # Database persistence
│   ├── link_finder.py      # HTML parsing and link extraction
│   ├── tasks.py            # Celery distributed tasks
│   ├── config.py           # Configuration loader
│   ├── utils.py            # URL normalization and utilities
│   └── plugins/
│       ├── web_scraper_plugin.py      # Comprehensive web scraper
│       ├── scraper_utils.py           # Query utilities
│       ├── title_logger_plugin.py     # Title extraction
│       ├── entity_extraction.py       # NLP entity extraction
│       ├── dynamic_scraper.py         # JavaScript rendering
│       └── real_time_metrics.py       # Live metrics
├── docs/                   # Documentation
├── examples/               # Usage examples
├── tests/                  # Test suite
├── run.py                  # Simple runner script
├── query_data.py           # Data query script
└── pyproject.toml          # Poetry dependencies
```

---

## 🔌 Plugin System

Spider uses a powerful plugin architecture for extensibility.

### Using the Web Scraper Plugin

The comprehensive web scraper extracts structured data from every page:

```python
from spider.plugins.scraper_utils import ScraperDataQuery

query = ScraperDataQuery()

# Get page data
page = query.get_page_data("http://example.com")
print(f"Title: {page['title']}")
print(f"Words: {page['word_count']}")
print(f"Links: {len(page['links'])}")

# Search pages
results = query.search_by_title("python")

# Get statistics
stats = query.get_page_statistics()
print(f"Total pages: {stats['total_pages']}")
```

**What gets extracted:**
- Metadata (title, description, keywords, author, language)
- Content structure (headings, word count, text analysis)
- Links (internal/external with anchor text)
- Images (URLs, alt text, dimensions)
- Forms (actions, methods, input fields)
- Social metadata (OpenGraph, Twitter Card)
- Structured data (JSON-LD)
- Page structure (semantic HTML)

📚 **Full documentation:** [docs/web-scraper/](docs/web-scraper/)

### Creating Custom Plugins

```python
from spider.plugin import Plugin

class MyPlugin(Plugin):
    async def should_run(self, url: str, content: str) -> bool:
        return True  # Run on all pages

    async def process(self, url: str, content: str) -> str:
        # Your processing logic here
        print(f"Processing {url}")
        return content

# Register in main.py
plugin_manager.register(MyPlugin())
```

📚 **Plugin documentation:** [Plugin.md](Plugin.md)

---

## 🌐 Distributed Mode

Run Spider across multiple workers for large-scale crawling.

### Start Celery Worker

```bash
celery -A spider.tasks.celery_app worker --loglevel=info
```

### Queue Tasks

```python
from spider.tasks import crawl_task

result = crawl_task.delay("https://example.com")
print(f"Task ID: {result.id}")
```

---

## 📊 Usage Examples

### Basic Crawling

```python
import asyncio
from spider.spider import Spider
from spider.config import config
from spider.plugin import PluginManager
from spider.plugins.web_scraper_plugin import WebScraperPlugin

# Setup
plugin_manager = PluginManager()
plugin_manager.register(WebScraperPlugin())

# Create and run crawler
crawler = Spider(config['start_url'], config, plugin_manager)
asyncio.run(crawler.crawl())
```

### Query Data

```python
from spider.plugins.scraper_utils import ScraperDataQuery

query = ScraperDataQuery()

# Get all pages
pages = query.get_all_pages(limit=10)
for page in pages:
    print(f"{page['url']}: {page['title']}")

# Find pages with forms
pages_with_forms = query.get_pages_with_forms()

# Export data
query.export_to_json("http://example.com", "output.json")
```

### SEO Analysis

```python
import json

pages = query.get_all_pages()
for page in pages:
    # Check for SEO issues
    if not page['description']:
        print(f"⚠️ Missing description: {page['url']}")

    headings = json.loads(page['headings'])
    if len(headings['h1']) == 0:
        print(f"⚠️ No H1 heading: {page['url']}")
```

---

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# Run web scraper plugin tests
poetry run python test_web_scraper_plugin.py

# Check coverage
poetry run pytest --cov=spider
```

---

## 📚 Documentation

- **[Web Scraper Plugin](docs/web-scraper/WEB_SCRAPER_PLUGIN.md)** - Complete plugin documentation
- **[Quick Start Guide](docs/web-scraper/quickstart.md)** - Get started in 3 steps
- **[Quick Reference](docs/web-scraper/reference.md)** - Command cheat sheet
- **[Plugin System](Plugin.md)** - Creating custom plugins
- **[Examples](examples/)** - Code examples and use cases

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📋 Requirements

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Poetry (package manager)

See [pyproject.toml](pyproject.toml) for complete dependencies.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built with:
- [aiohttp](https://docs.aiohttp.org/) - Async HTTP client/server
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Celery](https://docs.celeryproject.org/) - Distributed task queue
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Playwright](https://playwright.dev/) - Browser automation
- [spaCy](https://spacy.io/) - NLP library

---

## 🐛 Issues & Support

- **Bug Reports:** [GitHub Issues](https://github.com/roshanlam/spider/issues)
- **Questions:** [GitHub Discussions](https://github.com/roshanlam/spider/discussions)
- **Documentation:** [docs/](docs/)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/roshanlam">Roshan Lamichhaner</a>
</p>

<p align="center">
  <a href="https://github.com/roshanlam/spider/stargazers">⭐ Star us on GitHub!</a>
</p>
