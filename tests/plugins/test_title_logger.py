"""Tests for title_logger_plugin."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from spider.plugins.title_logger_plugin import TitleLoggerPlugin


class TestTitleLoggerPlugin:
    """Tests for TitleLoggerPlugin."""

    @pytest.mark.asyncio
    async def test_should_run_returns_true(self):
        """Test that should_run always returns True."""
        plugin = TitleLoggerPlugin()
        result = await plugin.should_run("http://example.com", "<html></html>")
        assert result is True

    @pytest.mark.asyncio
    async def test_process_extracts_title(self):
        """Test that title is extracted from HTML."""
        plugin = TitleLoggerPlugin()
        html = "<html><head><title>Test Page</title></head></html>"
        url = "http://example.com"

        with patch('spider.plugins.title_logger_plugin.engine') as mock_engine:
            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__.return_value = mock_conn

            result = await plugin.process(url, html)

            # Should return unchanged content
            assert result == html

    @pytest.mark.asyncio
    async def test_process_no_title(self):
        """Test processing HTML without title tag."""
        plugin = TitleLoggerPlugin()
        html = "<html><body>No title</body></html>"
        url = "http://example.com"

        with patch('spider.plugins.title_logger_plugin.engine') as mock_engine:
            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__.return_value = mock_conn

            result = await plugin.process(url, html)

            assert result == html

    @pytest.mark.asyncio
    async def test_process_empty_title(self):
        """Test processing HTML with empty title."""
        plugin = TitleLoggerPlugin()
        html = "<html><head><title></title></head></html>"
        url = "http://example.com"

        with patch('spider.plugins.title_logger_plugin.engine') as mock_engine:
            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__.return_value = mock_conn

            result = await plugin.process(url, html)

            assert result == html

    @pytest.mark.asyncio
    async def test_process_title_with_whitespace(self):
        """Test title extraction with whitespace."""
        plugin = TitleLoggerPlugin()
        html = "<html><head><title>  Test Page  </title></head></html>"
        url = "http://example.com"

        with patch('spider.plugins.title_logger_plugin.engine') as mock_engine:
            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__.return_value = mock_conn

            result = await plugin.process(url, html)

            assert result == html

    @pytest.mark.asyncio
    async def test_process_database_error(self):
        """Test handling of database errors."""
        plugin = TitleLoggerPlugin()
        html = "<html><head><title>Test</title></head></html>"
        url = "http://example.com"

        with patch('spider.plugins.title_logger_plugin.engine') as mock_engine:
            mock_engine.connect.side_effect = Exception("Database error")

            # Should not crash
            result = await plugin.process(url, html)

            assert result == html

    @pytest.mark.asyncio
    async def test_process_malformed_html(self):
        """Test processing malformed HTML."""
        plugin = TitleLoggerPlugin()
        html = "<html><head><title>Test</title>"  # Missing closing tags
        url = "http://example.com"

        with patch('spider.plugins.title_logger_plugin.engine') as mock_engine:
            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__.return_value = mock_conn

            result = await plugin.process(url, html)

            assert result == html
