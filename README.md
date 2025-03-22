# Spider

<p align="center">
  <img src="spider.png" />
</p>

A modern, scalable, and extensible web crawler designed for efficient distributed crawling and data extraction. Built using asynchronous I/O, robust logging, plugin architecture, and distributed task processing with Celery.

## Features
* Asynchronous Crawling:
Utilizes aiohttp and asyncio for non-blocking network I/O, allowing concurrent requests and improved performance.

* Distributed Task Processing:
Integrated with Celery and Redis to distribute crawling tasks across multiple workers and machines.

* Database Persistence:
Uses PostgreSQL (via SQLAlchemy) to store crawled pages efficiently with indexing and transactional support.

* Robust Logging:
A dedicated logging framework supports console output, rotating file logs, and SQLite logging for persistent diagnostics.

* Plugin Architecture:
Easily extend the crawler with custom plugins for processing, filtering, or transforming crawled data without modifying core code.

* URL Normalization:
Enhanced URL normalization removes trailing slashes and sorts query parameters to avoid duplicate processing.

## Architecture Overview
The project is organized into modular components, each handling a specific aspect of the crawler:

* domain.py:
Extracts and processes domain information from URLs.

* link_finder.py:
Parses HTML using BeautifulSoup with the lxml parser and extracts hyperlinks.

* utils.py:
Provides URL normalization and logging initialization utilities.

* storage.py:
Manages database connectivity and persistence using SQLAlchemy and PostgreSQL.

* spider.py:
Implements the core asynchronous crawler that fetches pages, processes content, and enqueues discovered links.

* plugin.py:
Contains the plugin interface and a manager for registering and running custom plugins.

* tasks.py:
Defines Celery tasks to enable distributed crawling across workers.

* main.py:
Serves as the entry point for local crawling execution.

* config.yaml / config.py:
Handles configuration and environment variable overrides.

## Installation
Make sure you have the following installed:
* Python 3.8+
* PostgreSQL
* Redis

1. Clone the repo:
```bash git clone https://github.com/roshanlam/spider.git```
```bash cd spider```

2. Create a Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies:
```bash
pip install -r requirements.txt
```
4. Configure PostgreSQL and Redis:
Ensure your PostgreSQL database and Redis server are running.
Update config.yaml with your database URL and Redis broker settings.

## Configuration
The crawler is configured via the config.yaml file. Here is an configuration:

```yaml
threads: 8
rate_limit: 1         # seconds between requests
user_agent: "MyCrawler/1.0"
timeout: 10
start_url: "https://example.com"

database:
  url: "postgresql://user:password@localhost/crawlerdb"

celery:
  broker_url: "redis://localhost:6379/0"
  result_backend: "redis://localhost:6379/0"
```

## Usage
### Running Locally
To start the crawler locally:
```bash
python -m spider.main
```
This will initialize the crawler, load the configured start URL, and begin asynchronous crawling.

### Running in Distributed Mode

1. Start the Celery Worker:
```
celery -A spider.tasks.celery_app worker --loglevel=info
```
2. Dispatch a Crawl Task:
You can use a Python shell or run the run_crawler.

```bash
python run_crawler.py
```

This will distribute the crawl task across available Celery workers.

## Plugin System
The crawler supports custom plugins to extend functionality. Plugins can be used to process, filter, or extract additional data from crawled pages.
Read the Plugin.md file for more info.

## Development & Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes with clear and descriptive commit messages.
4. Push your branch (`git push origin feature/my-feature`).
5. Open a pull request detailing your changes and improvements.
