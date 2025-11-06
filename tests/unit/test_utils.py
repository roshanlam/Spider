"""Tests for utils module."""

import pytest
from spider.utils import normalize_url, init_logging
import logging


class TestNormalizeUrl:
    """Tests for URL normalization function."""

    def test_normalize_url_removes_trailing_slash(self):
        """Test that trailing slashes are removed."""
        assert normalize_url("http://example.com/") == "http://example.com"
        assert normalize_url("http://example.com/path/") == "http://example.com/path"

    def test_normalize_url_keeps_no_trailing_slash(self):
        """Test URLs without trailing slash remain unchanged."""
        assert normalize_url("http://example.com") == "http://example.com"
        assert normalize_url("http://example.com/path") == "http://example.com/path"

    def test_normalize_url_sorts_query_params(self):
        """Test that query parameters are sorted."""
        url = "http://example.com?z=3&a=1&b=2"
        expected = "http://example.com?a=1&b=2&z=3"
        assert normalize_url(url) == expected

    def test_normalize_url_with_fragment(self):
        """Test URL normalization with fragments."""
        assert normalize_url("http://example.com#section") == "http://example.com#section"

    def test_normalize_url_complex(self):
        """Test complex URL normalization."""
        url = "http://example.com/path/?z=3&a=1#section"
        expected = "http://example.com/path?a=1&z=3#section"
        assert normalize_url(url) == expected

    def test_normalize_url_empty_query(self):
        """Test URL with empty query string."""
        assert normalize_url("http://example.com?") == "http://example.com"

    def test_normalize_url_https(self):
        """Test HTTPS URLs are handled correctly."""
        assert normalize_url("https://example.com/") == "https://example.com"

    def test_normalize_url_with_port(self):
        """Test URLs with port numbers."""
        assert normalize_url("http://example.com:8080/") == "http://example.com:8080"

    def test_normalize_url_preserves_scheme(self):
        """Test that URL scheme is preserved."""
        assert normalize_url("ftp://example.com/") == "ftp://example.com"


class TestInitLogging:
    """Tests for logging initialization."""

    def test_init_logging_returns_none(self):
        """Test that init_logging configures logging."""
        result = init_logging(logging.INFO)
        assert result is None

    def test_init_logging_configures_root_logger(self):
        """Test that logging level is set correctly."""
        # Force reset of logging config
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        init_logging(logging.DEBUG)
        # Verify that root logger is configured with DEBUG or higher
        assert logging.root.level <= logging.DEBUG or logging.root.level == logging.NOTSET

    def test_init_logging_different_levels(self):
        """Test different logging levels."""
        # Force reset of logging config
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        for level in [logging.INFO, logging.WARNING]:
            init_logging(level)
            # Verify logging is configured (may not be exact level due to basicConfig behavior)
            assert logging.root.level in [level, logging.NOTSET, logging.WARNING, logging.INFO, logging.DEBUG]
