"""Pytest configuration and fixtures for Spider tests."""

import pytest
import asyncio
from unittest.mock import Mock, MagicMock


@pytest.fixture
def sample_html():
    """Provide sample HTML for testing."""
    return """
    <html>
        <head>
            <title>Test Page</title>
            <meta name="description" content="Test description">
        </head>
        <body>
            <h1>Main Heading</h1>
            <p>Test paragraph with <a href="http://example.com">a link</a>.</p>
            <img src="/image.jpg" alt="Test image">
        </body>
    </html>
    """


@pytest.fixture
def sample_url():
    """Provide sample URL for testing."""
    return "http://example.com"


@pytest.fixture
def mock_config():
    """Provide mock configuration."""
    return {
        'threads': 8,
        'rate_limit': 1,
        'timeout': 10,
        'user_agent': 'TestBot/1.0',
        'start_url': 'http://example.com',
        'database': {
            'url': 'postgresql://test@localhost/testdb'
        },
        'celery': {
            'broker_url': 'redis://localhost:6379/0',
            'result_backend': 'redis://localhost:6379/0'
        }
    }


@pytest.fixture
def mock_storage():
    """Provide mock Storage object."""
    storage = Mock()
    storage.save_page = Mock()
    storage.url_exists = Mock(return_value=False)
    return storage


@pytest.fixture
def mock_plugin_manager():
    """Provide mock PluginManager."""
    from spider.plugin import PluginManager
    return PluginManager()


@pytest.fixture
def mock_database_engine():
    """Provide mock database engine."""
    engine = MagicMock()
    conn = MagicMock()
    engine.connect.return_value.__enter__.return_value = conn
    return engine


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def complex_html():
    """Provide complex HTML for comprehensive testing."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="A comprehensive test page">
        <meta name="keywords" content="test, example, spider">
        <meta name="author" content="Test Author">
        <meta property="og:title" content="OG Title">
        <meta property="og:description" content="OG Description">
        <meta name="twitter:card" content="summary">
        <title>Complex Test Page</title>
        <link rel="canonical" href="http://example.com/canonical">
    </head>
    <body>
        <header>
            <nav>
                <a href="/home">Home</a>
                <a href="/about">About</a>
            </nav>
        </header>
        <main>
            <article>
                <h1>Main Article Heading</h1>
                <h2>Subheading 1</h2>
                <p>Paragraph with content.</p>
                <h2>Subheading 2</h2>
                <p>Another paragraph.</p>
            </article>
            <aside>
                <h3>Sidebar</h3>
                <ul>
                    <li><a href="/link1">Link 1</a></li>
                    <li><a href="/link2">Link 2</a></li>
                </ul>
            </aside>
        </main>
        <footer>
            <p>Footer content</p>
        </footer>
        <form action="/submit" method="POST">
            <input type="text" name="username" required>
            <input type="email" name="email" placeholder="Email">
            <textarea name="message"></textarea>
            <button type="submit">Submit</button>
        </form>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "Test Article"
        }
        </script>
    </body>
    </html>
    """


@pytest.fixture
def html_with_links():
    """HTML with various types of links."""
    return """
    <html>
    <body>
        <a href="http://external.com">External</a>
        <a href="/internal">Internal</a>
        <a href="relative/path">Relative</a>
        <a href="#fragment">Fragment</a>
        <a href="mailto:test@example.com">Email</a>
        <a href="javascript:void(0)">JavaScript</a>
    </body>
    </html>
    """


@pytest.fixture
def html_with_images():
    """HTML with various image tags."""
    return """
    <html>
    <body>
        <img src="http://example.com/absolute.jpg" alt="Absolute">
        <img src="/relative.jpg" alt="Relative">
        <img src="image.png" alt="Local" width="100" height="200">
        <img src="no-alt.jpg">
    </body>
    </html>
    """


@pytest.fixture
def html_with_forms():
    """HTML with form elements."""
    return """
    <html>
    <body>
        <form action="/submit" method="POST" id="form1">
            <input type="text" name="name" id="name" required>
            <input type="email" name="email" placeholder="Email">
            <input type="password" name="pass">
            <textarea name="message"></textarea>
            <select name="choice">
                <option value="1">Option 1</option>
                <option value="2">Option 2</option>
            </select>
            <button type="submit">Submit</button>
        </form>
        <form action="/search" method="GET">
            <input type="search" name="q">
        </form>
    </body>
    </html>
    """


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration between tests."""
    import logging
    logging.root.handlers = []
    yield
    logging.root.handlers = []


# Markers for test organization
pytest_plugins = []
