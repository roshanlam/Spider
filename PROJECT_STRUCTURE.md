# Spider Project Structure

This document provides an overview of the Spider project organization.

## 📂 Directory Structure

```
spider/
├── .git/                       # Git repository
├── src/                        # Source code
│   └── spider/                 # Main package
│       ├── __init__.py
│       ├── spider.py           # Core async crawler
│       ├── plugin.py           # Plugin system
│       ├── storage.py          # Database persistence
│       ├── link_finder.py      # HTML parsing
│       ├── tasks.py            # Celery tasks
│       ├── config.py           # Configuration
│       ├── config.yaml         # Config file
│       ├── utils.py            # Utilities
│       ├── domain.py           # Domain handling
│       ├── main.py             # Entry point
│       └── plugins/            # Plugin modules
│           ├── web_scraper_plugin.py      # Comprehensive web scraper
│           ├── scraper_utils.py           # Query utilities
│           ├── title_logger_plugin.py     # Title extraction
│           ├── entity_extraction.py       # NLP extraction
│           ├── dynamic_scraper.py         # JavaScript rendering
│           └── real_time_metrics.py       # Live metrics
│
├── docs/                       # Documentation
│   ├── README.md               # Documentation index
│   └── web-scraper/            # Web scraper docs
│       ├── WEB_SCRAPER_PLUGIN.md    # Complete docs
│       ├── quickstart.md            # Quick start
│       └── reference.md             # Reference guide
│
├── examples/                   # Usage examples
│   └── web_scraper_example.py # Web scraper examples
│
├── tests/                      # Test suite
│   └── (test files)
│
├── client/                     # Client code (if applicable)
│
├── venv/                       # Virtual environment (gitignored)
│
├── run.py                      # Simple crawler runner
├── query_data.py               # Data query script
├── crawl.sh                    # Shell runner
├── query.sh                    # Shell query script
├── test_web_scraper_plugin.py # Plugin tests
├── run_crawler.py              # Celery task dispatcher
│
├── README.md                   # Main project README
├── CONTRIBUTING.md             # Contributing guide
├── LICENSE                     # MIT License
├── Plugin.md                   # Plugin system docs
├── TODO.md                     # Project TODOs (gitignored)
│
├── pyproject.toml              # Poetry dependencies
├── poetry.lock                 # Locked dependencies
├── requirements.txt            # Pip requirements
├── setup.cfg                   # Setup config
│
├── .gitignore                  # Git ignore rules
└── spider.png                  # Project logo
```

---

## 📁 Key Directories

### `/src/spider/`
Main package containing core crawler functionality.

**Core Modules:**
- `spider.py` - Asynchronous web crawler engine
- `plugin.py` - Plugin architecture and manager
- `storage.py` - PostgreSQL database operations
- `link_finder.py` - HTML parsing and link extraction
- `tasks.py` - Celery distributed task definitions
- `config.py` - Configuration loader
- `utils.py` - URL normalization and utilities

**Entry Points:**
- `main.py` - Local crawler execution
- `config.yaml` - Configuration settings

### `/src/spider/plugins/`
Extensible plugin modules for data processing.

**Included Plugins:**
- `web_scraper_plugin.py` (450+ lines) - Comprehensive data extraction
- `scraper_utils.py` (380+ lines) - Query and analysis utilities
- `title_logger_plugin.py` - Page title extraction
- `entity_extraction.py` - spaCy NLP entity recognition
- `dynamic_scraper.py` - Playwright-based JS rendering
- `real_time_metrics.py` - FastAPI WebSocket metrics

### `/docs/`
Project documentation organized by topic.

**Structure:**
- `README.md` - Documentation index and navigation
- `web-scraper/` - Web scraper plugin documentation
  - Complete plugin guide
  - Quick start tutorial
  - Command reference

### `/examples/`
Practical code examples and use cases.

**Includes:**
- `web_scraper_example.py` - 12 comprehensive examples
  - Basic scraping
  - SEO analysis
  - Link analysis
  - Form detection
  - Data export
  - And more...

### `/tests/`
Test suite for the project (pytest-based).

---

## 🎯 Entry Points

### For Users

| File | Purpose | Usage |
|------|---------|-------|
| **run.py** | Simple crawler runner | `poetry run python run.py` |
| **query_data.py** | Data query script | `poetry run python query_data.py` |
| **crawl.sh** | Shell script runner | `./crawl.sh` |
| **query.sh** | Shell query script | `./query.sh` |

### For Developers

| File | Purpose | Usage |
|------|---------|-------|
| **src/spider/main.py** | Main entry point | `poetry run python -m spider.main` |
| **run_crawler.py** | Celery task dispatcher | `python run_crawler.py` |
| **test_web_scraper_plugin.py** | Plugin test suite | `poetry run python test_web_scraper_plugin.py` |

---

## 🔌 Plugin System

### Creating a Plugin

1. Create new file in `src/spider/plugins/`
2. Inherit from `Plugin` class
3. Implement `should_run()` and `process()` methods
4. Register in `src/spider/main.py`

### Example Plugin Structure

```python
# src/spider/plugins/my_plugin.py
from spider.plugin import Plugin

class MyPlugin(Plugin):
    async def should_run(self, url: str, content: str) -> bool:
        return True  # Run on all pages

    async def process(self, url: str, content: str) -> str:
        # Processing logic
        return content
```

---

## 🗄️ Database Schema

### Core Tables

**`pages`** (from storage.py)
- URL storage and tracking
- Created by core crawler

**`titles`** (from title_logger_plugin.py)
- Page titles
- Created by TitleLoggerPlugin

**`scraped_data`** (from web_scraper_plugin.py)
- Comprehensive webpage data
- 20+ fields including metadata, links, images, forms, etc.
- Created by WebScraperPlugin

**`entities`** (from entity_extraction.py)
- Named entities (persons, organizations, locations)
- Created by EntityExtractionPlugin

---

## 📊 Configuration

### Main Config: `src/spider/config.yaml`

```yaml
start_url: "http://example.com"
rate_limit: 1
threads: 8
timeout: 10

database:
  url: "postgresql://user@localhost/crawlerdb"

celery:
  broker_url: "redis://localhost:6379/0"
  result_backend: "redis://localhost:6379/0"
```

### Environment Variables

Override config with environment variables:
- `CRAWLER_START_URL`
- `CRAWLER_THREADS`
- `CRAWLER_RATE_LIMIT`
- `CRAWLER_USER_AGENT`
- `CRAWLER_TIMEOUT`

---

## 🧪 Testing

### Test Files

- `test_web_scraper_plugin.py` - Web scraper tests (10 tests)
- Additional tests in `/tests/` directory

### Running Tests

```bash
# All tests
poetry run pytest

# Specific test file
poetry run python test_web_scraper_plugin.py

# With coverage
poetry run pytest --cov=spider
```

---

## 📝 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Main project documentation and quick start |
| **CONTRIBUTING.md** | Contribution guidelines and development setup |
| **Plugin.md** | Plugin system documentation |
| **docs/README.md** | Documentation index |
| **docs/web-scraper/*** | Web scraper plugin docs |

---

## 🔧 Development Tools

### Package Management
- **Poetry** - Dependency management (`pyproject.toml`)
- **pip** - Alternative package installer (`requirements.txt`)

### Code Quality
- **pytest** - Testing framework
- **coverage** - Code coverage analysis

### External Services
- **PostgreSQL** - Database
- **Redis** - Celery broker
- **Celery** - Distributed tasks

---

## 🚀 Deployment

### Local Development
```bash
poetry install
poetry run python run.py
```

### Distributed Mode
```bash
# Terminal 1: Start worker
celery -A spider.tasks.celery_app worker --loglevel=info

# Terminal 2: Queue tasks
python run_crawler.py
```

---

## 📦 Dependencies

See `pyproject.toml` for complete list. Key dependencies:

**Core:**
- aiohttp - Async HTTP
- BeautifulSoup4 - HTML parsing
- SQLAlchemy - Database ORM
- Celery - Task queue
- Redis - Message broker

**Plugins:**
- Playwright - Browser automation
- spaCy - NLP processing
- FastAPI - Web framework
- uvicorn - ASGI server

---

## 🔍 Finding Your Way

### I want to modify...

**...the crawler behavior**
→ Edit `src/spider/spider.py`

**...URL handling**
→ Edit `src/spider/utils.py`

**...database operations**
→ Edit `src/spider/storage.py`

**...plugin system**
→ Edit `src/spider/plugin.py`

**...data extraction**
→ Edit `src/spider/plugins/web_scraper_plugin.py`

**...configuration**
→ Edit `src/spider/config.yaml`

---

<p align="center">
  <a href="README.md">← Back to README</a> •
  <a href="CONTRIBUTING.md">Contributing →</a>
</p>
