"""Tests for spider module."""

import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from spider.spider import Spider
from spider.plugin import PluginManager


class TestSpider:
    """Tests for Spider class."""

    def test_spider_creation(self):
        """Test creating a Spider instance."""
        config = {
            'threads': 8,
            'rate_limit': 1,
            'timeout': 10,
            'user_agent': 'TestBot/1.0'
        }
        plugin_manager = PluginManager()

        spider = Spider("http://example.com", config, plugin_manager)

        assert spider is not None
        assert spider.start_url == "http://example.com"
        assert spider.config == config

    def test_spider_with_config(self):
        """Test Spider initialization with configuration."""
        config = {
            'threads': 10,
            'rate_limit': 2,
            'timeout': 15,
            'user_agent': 'CustomBot/2.0'
        }
        plugin_manager = PluginManager()

        spider = Spider("http://test.com", config, plugin_manager)

        # Verify configuration is stored
        assert spider.config == config
        assert spider.start_url == "http://test.com"

    def test_spider_plugin_manager(self):
        """Test that Spider uses plugin manager."""
        config = {
            'timeout': 10,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()

        spider = Spider("http://example.com", config, plugin_manager)

        # Verify plugin manager is stored
        assert spider.plugin_manager == plugin_manager

    @pytest.mark.asyncio
    async def test_spider_fetch_page(self):
        """Test fetching a page."""
        config = {
            'timeout': 10,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()

        spider = Spider("http://example.com", config, plugin_manager)

        # Mock aiohttp session
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_response.text = AsyncMock(return_value="<html>Test</html>")
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)

        # Test fetch method
        result = await spider.fetch(mock_session, "http://example.com")
        assert result == "<html>Test</html>"

    def test_spider_url_normalization(self):
        """Test that URLs are normalized."""
        config = {
            'timeout': 10,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()

        spider = Spider("http://example.com/", config, plugin_manager)

        # Should normalize URL
        assert spider.start_url == "http://example.com"

    def test_spider_rate_limiting(self):
        """Test rate limiting configuration."""
        config = {
            'rate_limit': 5,
            'timeout': 10,
            'user_agent': 'TestBot/1.0'
        }
        plugin_manager = PluginManager()

        spider = Spider("http://example.com", config, plugin_manager)

        # Verify rate limiting is configured
        assert spider.config['rate_limit'] == 5

    def test_spider_visited_tracking(self):
        """Test that visited URLs are tracked."""
        config = {
            'timeout': 10,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()

        spider = Spider("http://example.com", config, plugin_manager)

        # Should initialize visited set
        assert isinstance(spider.visited, set)
        assert len(spider.visited) == 0

    @pytest.mark.asyncio
    async def test_spider_process_url_already_visited(self):
        """Test that already visited URLs are skipped."""
        config = {
            'timeout': 10,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()
        spider = Spider("http://example.com", config, plugin_manager)

        # Mark URL as visited
        spider.visited.add("http://example.com")

        # Process should skip this URL
        mock_session = AsyncMock()
        await spider.process_url(mock_session, "http://example.com")

        # Session should not be called
        mock_session.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_spider_process_url_saves_content(self):
        """Test that processed content is saved."""
        config = {
            'timeout': 10,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()
        spider = Spider("http://example.com", config, plugin_manager)

        # Mock session and response
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_response.text = AsyncMock(return_value="<html><body><a href='/test'>Link</a></body></html>")
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)

        # Mock save_page
        with patch('spider.spider.save_page') as mock_save:
            await spider.process_url(mock_session, "http://example.com/page")

            # Verify page was fetched and saved
            assert "http://example.com/page" in spider.visited
            mock_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_spider_fetch_non_html(self):
        """Test that non-HTML content is skipped."""
        config = {
            'timeout': 10,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()
        spider = Spider("http://example.com", config, plugin_manager)

        # Mock session returning JSON
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await spider.fetch(mock_session, "http://example.com/api")
        assert result is None

    @pytest.mark.asyncio
    async def test_spider_fetch_non_200_status(self):
        """Test that non-200 responses are skipped."""
        config = {
            'timeout': 10,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()
        spider = Spider("http://example.com", config, plugin_manager)

        # Mock session returning 404
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_session.get = MagicMock(return_value=mock_response)
        mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
        mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)

        result = await spider.fetch(mock_session, "http://example.com/missing")
        assert result is None

    @pytest.mark.asyncio
    async def test_spider_fetch_timeout(self):
        """Test that timeouts are handled."""
        config = {
            'timeout': 1,
            'user_agent': 'TestBot/1.0',
            'rate_limit': 1
        }
        plugin_manager = PluginManager()
        spider = Spider("http://example.com", config, plugin_manager)

        # Mock session that times out
        mock_session = AsyncMock()
        mock_session.get.side_effect = Exception("Timeout")

        result = await spider.fetch(mock_session, "http://example.com")
        assert result is None
