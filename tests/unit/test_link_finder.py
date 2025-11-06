"""Tests for link_finder module."""

import pytest
from spider.link_finder import LinkFinder


class TestLinkFinder:
    """Tests for LinkFinder class."""

    def test_find_links_simple_html(self):
        """Test finding links in simple HTML."""
        html = '<html><body><a href="http://example.com">Link</a></body></html>'
        finder = LinkFinder("http://base.com", "http://base.com")
        finder.feed(html)
        links = finder.page_links()
        assert "http://example.com" in links

    def test_find_links_relative_urls(self):
        """Test converting relative URLs to absolute."""
        html = '<html><body><a href="/path">Link</a></body></html>'
        finder = LinkFinder("http://example.com", "http://example.com")
        finder.feed(html)
        links = finder.page_links()
        assert "http://example.com/path" in links

    def test_find_links_multiple(self):
        """Test finding multiple links."""
        html = '''
        <html><body>
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
            <a href="http://external.com">External</a>
        </body></html>
        '''
        finder = LinkFinder("http://example.com", "http://example.com")
        finder.feed(html)
        links = finder.page_links()
        assert len(links) == 3
        assert "http://example.com/link1" in links
        assert "http://example.com/link2" in links
        assert "http://external.com" in links

    def test_find_links_ignores_fragments(self):
        """Test that fragments are included (not ignored)."""
        html = '<html><body><a href="#fragment">Fragment</a></body></html>'
        finder = LinkFinder("http://example.com", "http://example.com")
        finder.feed(html)
        links = finder.page_links()
        # Fragment links are included by urljoin
        assert len(links) > 0

    def test_find_links_empty_html(self):
        """Test with empty HTML."""
        finder = LinkFinder("http://example.com", "http://example.com")
        finder.feed("")
        links = finder.page_links()
        assert len(links) == 0

    def test_find_links_no_links(self):
        """Test HTML with no links."""
        html = '<html><body><p>No links here</p></body></html>'
        finder = LinkFinder("http://example.com", "http://example.com")
        finder.feed(html)
        links = finder.page_links()
        assert len(links) == 0

    def test_find_links_malformed_html(self):
        """Test with malformed HTML."""
        html = '<html><body><a href="/path">Link'
        finder = LinkFinder("http://example.com", "http://example.com")
        finder.feed(html)
        links = finder.page_links()
        # Should still extract the link
        assert "http://example.com/path" in links

    def test_find_links_with_query_params(self):
        """Test links with query parameters."""
        html = '<html><body><a href="/path?q=test">Link</a></body></html>'
        finder = LinkFinder("http://example.com", "http://example.com")
        finder.feed(html)
        links = finder.page_links()
        assert "http://example.com/path?q=test" in links

    def test_find_links_duplicate_removal(self):
        """Test that duplicate links are removed."""
        html = '''
        <html><body>
            <a href="/path">Link 1</a>
            <a href="/path">Link 2</a>
        </body></html>
        '''
        finder = LinkFinder("http://example.com", "http://example.com")
        finder.feed(html)
        links = finder.page_links()
        # Should only have one instance of the link
        assert len(links) == 1
        assert "http://example.com/path" in links

    def test_find_links_protocol_relative(self):
        """Test protocol-relative URLs."""
        html = '<html><body><a href="//example.com/path">Link</a></body></html>'
        finder = LinkFinder("http://base.com", "http://base.com")
        finder.feed(html)
        links = finder.page_links()
        # urljoin handles protocol-relative URLs
        assert len(links) > 0
