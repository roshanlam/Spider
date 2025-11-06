# Spider Documentation

Welcome to the Spider documentation! This directory contains comprehensive guides for using and extending Spider.

## 📚 Documentation Index

### Getting Started
- **[Main README](../README.md)** - Project overview and quick start
- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute to the project

### Web Scraper Plugin
- **[Web Scraper Plugin](web-scraper/WEB_SCRAPER_PLUGIN.md)** - Complete plugin documentation
- **[Quick Start Guide](web-scraper/quickstart.md)** - Get started in 3 steps
- **[Quick Reference](web-scraper/reference.md)** - Command cheat sheet

### Plugin System
- **[Plugin System](../Plugin.md)** - Creating custom plugins

### Examples
- **[Examples Directory](../examples/)** - Code examples and use cases

---

## 🎯 Quick Navigation

### I want to...

**...get started with Spider**
→ Read the [Main README](../README.md#quick-start)

**...use the web scraper plugin**
→ Start with [Quick Start Guide](web-scraper/quickstart.md)

**...query scraped data**
→ See [Quick Reference](web-scraper/reference.md#query-data)

**...create a custom plugin**
→ Read [Plugin System](../Plugin.md)

**...contribute to the project**
→ Follow [Contributing Guide](../CONTRIBUTING.md)

**...see code examples**
→ Browse [Examples](../examples/)

---

## 📖 Documentation Structure

```
docs/
├── README.md                           # This file
└── web-scraper/
    ├── WEB_SCRAPER_PLUGIN.md          # Complete plugin docs
    ├── quickstart.md                   # Quick start guide
    └── reference.md                    # Quick reference
```

---

## 🔍 What You'll Find Here

### Web Scraper Plugin Documentation

The web scraper plugin is Spider's most comprehensive data extraction tool:

- **Metadata Extraction**: Title, description, keywords, author, language
- **Content Analysis**: Word count, headings, text structure
- **Link Extraction**: Internal/external links with classification
- **Image Extraction**: URLs, alt text, dimensions
- **Form Detection**: Actions, methods, input fields
- **Social Metadata**: OpenGraph, Twitter Card data
- **Structured Data**: JSON-LD extraction
- **Page Structure**: Semantic HTML analysis

### Plugin System

Learn how to extend Spider with custom plugins:

- Plugin architecture overview
- Creating custom plugins
- Plugin lifecycle and hooks
- Best practices
- Example plugins

---

## 💡 Common Tasks

### Run the Crawler

```bash
poetry run python run.py
```

### Query Scraped Data

```bash
poetry run python query_data.py
```

### Create a Plugin

```python
from spider.plugin import Plugin

class MyPlugin(Plugin):
    async def should_run(self, url: str, content: str) -> bool:
        return True

    async def process(self, url: str, content: str) -> str:
        # Your logic here
        return content
```

---

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/roshanlam/spider/issues)
- **Discussions**: [GitHub Discussions](https://github.com/roshanlam/spider/discussions)
- **Examples**: [examples/](../examples/)

---

## 🤝 Contributing

Found an error in the docs? Want to add more examples?

1. Fork the repository
2. Make your changes
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

<p align="center">
  <a href="../README.md">← Back to Main README</a>
</p>
