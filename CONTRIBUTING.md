# Contributing to Spider

First off, thank you for considering contributing to Spider! It's people like you that make Spider such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Writing Tests](#writing-tests)
- [Documentation](#documentation)

---

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold these values.

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Poetry (package manager)
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/spider.git
   cd spider
   ```

3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/roshanlam/spider.git
   ```

---

## Development Setup

### 1. Install Dependencies

```bash
# Install with Poetry
poetry install

# Install Playwright browsers
poetry run playwright install chromium

# Download spaCy model
poetry run python -m spacy download en_core_web_sm
```

### 2. Setup Database

```bash
# Create database
createdb crawlerdb

# Verify connection
psql -d crawlerdb -c "SELECT 1;"
```

### 3. Configure Environment

Edit `src/spider/config.yaml`:

```yaml
start_url: "http://example.com"
database:
  url: "postgresql://YOUR_USERNAME@localhost/crawlerdb"
celery:
  broker_url: "redis://localhost:6379/0"
  result_backend: "redis://localhost:6379/0"
```

### 4. Run Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=spider

# Run specific test
poetry run python test_web_scraper_plugin.py
```

---

## How to Contribute

### Reporting Bugs

**Before submitting a bug report:**
- Check the issue tracker to see if the bug has already been reported
- Collect information about the bug (Python version, OS, error messages)

**Submitting a bug report:**
1. Use the issue tracker
2. Provide a clear title and description
3. Include steps to reproduce
4. Add relevant logs and screenshots
5. Mention the Python version and OS

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues:
1. Use a clear and descriptive title
2. Provide a detailed description of the suggested enhancement
3. Explain why this enhancement would be useful
4. Include examples if applicable

### Writing Plugins

Plugins are a great way to contribute! See [Plugin.md](Plugin.md) for details.

Example plugin:

```python
from spider.plugin import Plugin

class MyPlugin(Plugin):
    async def should_run(self, url: str, content: str) -> bool:
        """Determine if plugin should run for this URL/content."""
        return True

    async def process(self, url: str, content: str) -> str:
        """Process the content and return modified content."""
        # Your logic here
        return content
```

---

## Pull Request Process

### 1. Create a Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/amazing-feature
```

### 2. Make Changes

- Write clean, readable code
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Changes

Use clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "Add web scraper plugin for comprehensive data extraction"
git commit -m "Fix URL normalization bug for query parameters"
git commit -m "Update documentation for plugin system"

# Bad commit messages
git commit -m "fix bug"
git commit -m "update code"
git commit -m "changes"
```

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/amazing-feature

# Create pull request on GitHub
```

### 5. PR Checklist

- [ ] Code follows project style guidelines
- [ ] Added tests for new functionality
- [ ] All tests pass locally
- [ ] Updated documentation
- [ ] Added yourself to contributors (if first contribution)
- [ ] PR description clearly describes changes

---

## Coding Standards

### Python Style

We follow PEP 8 with some modifications:

```python
# Use type hints
def process_url(url: str, timeout: int = 10) -> dict:
    """Process a URL and return results."""
    pass

# Use descriptive variable names
page_content = fetch_page(url)  # Good
c = fetch_page(url)             # Bad

# Use docstrings for functions
def extract_links(html: str) -> List[str]:
    """
    Extract all links from HTML content.

    Args:
        html: HTML content as string

    Returns:
        List of absolute URLs found in the HTML
    """
    pass
```

### Async/Await

Use async/await properly:

```python
# Good
async def fetch_page(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Bad - mixing sync and async
def fetch_page(url: str) -> str:
    response = requests.get(url)  # Don't use sync in async project
    return response.text
```

### Error Handling

Always handle errors appropriately:

```python
# Good
try:
    page_data = await fetch_page(url)
except aiohttp.ClientError as e:
    logging.error(f"Failed to fetch {url}: {e}")
    return None

# Bad - catching generic exceptions
try:
    page_data = await fetch_page(url)
except:  # Too broad
    pass
```

---

## Writing Tests

### Test Structure

```python
import pytest
from spider.plugins.web_scraper_plugin import WebScraperPlugin

def test_plugin_initialization():
    """Test that plugin initializes correctly."""
    plugin = WebScraperPlugin()
    assert plugin is not None

@pytest.mark.asyncio
async def test_should_run():
    """Test should_run method."""
    plugin = WebScraperPlugin()
    result = await plugin.should_run("http://example.com", "<html></html>")
    assert result == True

@pytest.mark.asyncio
async def test_process_extracts_title():
    """Test that process extracts page title."""
    plugin = WebScraperPlugin()
    html = "<html><head><title>Test</title></head></html>"
    await plugin.process("http://example.com", html)
    # Verify title was extracted
```

### Running Tests

```bash
# All tests
poetry run pytest

# Specific file
poetry run pytest tests/test_plugin.py

# With coverage
poetry run pytest --cov=spider --cov-report=html

# Verbose output
poetry run pytest -v
```

---

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def extract_metadata(html: str, url: str) -> dict:
    """
    Extract metadata from HTML content.

    Args:
        html: HTML content as string
        url: URL of the page for context

    Returns:
        Dictionary containing extracted metadata with keys:
        - title: Page title
        - description: Meta description
        - keywords: Meta keywords

    Raises:
        ValueError: If html is empty or invalid

    Example:
        >>> metadata = extract_metadata(html, "http://example.com")
        >>> print(metadata['title'])
        'Example Domain'
    """
    pass
```

### Updating Documentation

When adding features:
1. Update relevant markdown files in `docs/`
2. Add examples to `examples/`
3. Update README.md if necessary
4. Add docstrings to all new functions/classes

---

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion on GitHub Discussions
- Reach out to maintainers

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Spider!** 🕷️
