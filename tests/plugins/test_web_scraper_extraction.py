"""Unit tests for WebScraperPlugin extraction methods."""

import pytest
from bs4 import BeautifulSoup
from spider.plugins.web_scraper_plugin import WebScraperPlugin


class TestWebScraperExtractionMethods:
    """Test individual extraction methods of WebScraperPlugin."""

    def setup_method(self):
        """Setup for each test method."""
        self.plugin = WebScraperPlugin()

    def test_extract_title(self):
        """Test title extraction."""
        html = "<html><head><title>Test Page Title</title></head></html>"
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_title(soup) == "Test Page Title"

    def test_extract_title_missing(self):
        """Test title extraction when missing."""
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_title(soup) is None

    def test_extract_description(self):
        """Test meta description extraction."""
        html = '<html><head><meta name="description" content="Test description"></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_description(soup) == "Test description"

    def test_extract_description_opengraph_fallback(self):
        """Test description fallback to OpenGraph."""
        html = '<html><head><meta property="og:description" content="OG description"></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_description(soup) == "OG description"

    def test_extract_description_missing(self):
        """Test description extraction when missing."""
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_description(soup) is None

    def test_extract_keywords(self):
        """Test keywords extraction."""
        html = '<html><head><meta name="keywords" content="test, keywords"></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_keywords(soup) == "test, keywords"

    def test_extract_keywords_missing(self):
        """Test keywords extraction when missing."""
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_keywords(soup) is None

    def test_extract_author(self):
        """Test author extraction."""
        html = '<html><head><meta name="author" content="John Doe"></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_author(soup) == "John Doe"

    def test_extract_author_article_fallback(self):
        """Test author fallback to article:author."""
        html = '<html><head><meta property="article:author" content="Jane Doe"></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_author(soup) == "Jane Doe"

    def test_extract_author_missing(self):
        """Test author extraction when missing."""
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_author(soup) is None

    def test_extract_canonical(self):
        """Test canonical URL extraction."""
        html = '<html><head><link rel="canonical" href="http://example.com/page"></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        result = self.plugin._extract_canonical(soup, "http://example.com")
        assert result == "http://example.com/page"

    def test_extract_canonical_relative(self):
        """Test canonical URL extraction with relative URL."""
        html = '<html><head><link rel="canonical" href="/page"></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        result = self.plugin._extract_canonical(soup, "http://example.com")
        assert result == "http://example.com/page"

    def test_extract_canonical_missing(self):
        """Test canonical extraction when missing."""
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_canonical(soup, "http://example.com") is None

    def test_extract_language(self):
        """Test language extraction."""
        html = '<html lang="en"><head></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_language(soup) == "en"

    def test_extract_language_xml_lang(self):
        """Test language extraction from xml:lang."""
        html = '<html xml:lang="fr"><head></head></html>'
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_language(soup) == "fr"

    def test_extract_language_missing(self):
        """Test language extraction when missing."""
        html = "<html><head></head></html>"
        soup = BeautifulSoup(html, 'lxml')
        assert self.plugin._extract_language(soup) is None

    def test_count_words(self):
        """Test word counting."""
        html = "<html><body><p>This is a test paragraph with words.</p></body></html>"
        soup = BeautifulSoup(html, 'lxml')
        count = self.plugin._count_words(soup)
        assert count > 0
        assert count == 7

    def test_count_words_empty(self):
        """Test word counting with empty content."""
        html = "<html><body></body></html>"
        soup = BeautifulSoup(html, 'lxml')
        count = self.plugin._count_words(soup)
        assert count == 0

    def test_extract_headings(self):
        """Test headings extraction."""
        html = """
        <html><body>
            <h1>Main Heading</h1>
            <h2>Subheading 1</h2>
            <h2>Subheading 2</h2>
            <h3>Sub-subheading</h3>
        </body></html>
        """
        soup = BeautifulSoup(html, 'lxml')
        headings = self.plugin._extract_headings(soup)
        assert 'h1' in headings
        assert len(headings['h1']) == 1
        assert headings['h1'][0] == 'Main Heading'
        assert 'h2' in headings
        assert len(headings['h2']) == 2

    def test_extract_headings_empty(self):
        """Test headings extraction with no headings."""
        html = "<html><body><p>No headings here</p></body></html>"
        soup = BeautifulSoup(html, 'lxml')
        headings = self.plugin._extract_headings(soup)
        assert isinstance(headings, dict)
        # Should have empty lists for h1-h6
        for i in range(1, 7):
            key = f'h{i}'
            assert key not in headings or len(headings[key]) == 0

    def test_extract_meta_tags(self):
        """Test meta tags extraction."""
        html = """
        <html><head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width">
            <meta property="og:title" content="Test">
        </head></html>
        """
        soup = BeautifulSoup(html, 'lxml')
        meta = self.plugin._extract_meta_tags(soup)
        assert isinstance(meta, dict)
        assert len(meta) > 0

    def test_extract_opengraph(self):
        """Test OpenGraph metadata extraction."""
        html = """
        <html><head>
            <meta property="og:title" content="OG Title">
            <meta property="og:description" content="OG Description">
            <meta property="og:image" content="http://example.com/image.jpg">
        </head></html>
        """
        soup = BeautifulSoup(html, 'lxml')
        og = self.plugin._extract_opengraph(soup)
        assert isinstance(og, dict)
        assert 'title' in og or 'og:title' in og
        # Check for either key format
        if 'og:title' in og:
            assert og['og:title'] == 'OG Title'
        elif 'title' in og:
            assert og['title'] == 'OG Title'

    def test_extract_twitter_card(self):
        """Test Twitter Card extraction."""
        html = """
        <html><head>
            <meta name="twitter:card" content="summary">
            <meta name="twitter:title" content="Twitter Title">
        </head></html>
        """
        soup = BeautifulSoup(html, 'lxml')
        twitter = self.plugin._extract_twitter_card(soup)
        assert isinstance(twitter, dict)
        # Check for either key format
        assert 'card' in twitter or 'twitter:card' in twitter
        if 'twitter:card' in twitter:
            assert twitter['twitter:card'] == 'summary'
        elif 'card' in twitter:
            assert twitter['card'] == 'summary'

    def test_extract_links(self):
        """Test link extraction."""
        html = """
        <html><body>
            <a href="http://example.com">External</a>
            <a href="/internal">Internal</a>
            <a href="http://example.com/page">Same domain</a>
        </body></html>
        """
        soup = BeautifulSoup(html, 'lxml')
        links = self.plugin._extract_links(soup, "http://example.com")
        # Method returns a dict with 'all', 'internal', 'external', 'count'
        assert isinstance(links, dict)
        assert 'all' in links or isinstance(links, list)
        if isinstance(links, dict):
            assert 'count' in links
            assert links['count'] > 0

    def test_extract_images(self):
        """Test image extraction."""
        html = """
        <html><body>
            <img src="http://example.com/image.jpg" alt="Test image" width="100">
            <img src="/relative.png" alt="Relative">
        </body></html>
        """
        soup = BeautifulSoup(html, 'lxml')
        images = self.plugin._extract_images(soup, "http://example.com")
        assert isinstance(images, list)
        assert len(images) == 2
        assert images[0]['alt'] == 'Test image'
        assert 'width' in images[0]

    def test_extract_forms(self):
        """Test form extraction."""
        html = """
        <html><body>
            <form action="/submit" method="POST">
                <input type="text" name="username">
                <input type="email" name="email">
                <button type="submit">Submit</button>
            </form>
        </body></html>
        """
        soup = BeautifulSoup(html, 'lxml')
        forms = self.plugin._extract_forms(soup)
        assert isinstance(forms, list)
        assert len(forms) == 1
        assert forms[0]['action'] == '/submit'
        assert forms[0]['method'] == 'POST'
        assert len(forms[0]['inputs']) == 2

    def test_extract_structured_data(self):
        """Test JSON-LD structured data extraction."""
        html = """
        <html><head>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": "Test Article"
            }
            </script>
        </head></html>
        """
        soup = BeautifulSoup(html, 'lxml')
        data = self.plugin._extract_structured_data(soup)
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]['@type'] == 'Article'

    @pytest.mark.asyncio
    async def test_should_run_valid_html(self):
        """Test should_run with valid HTML."""
        content = "<html><body>This is sufficient content for processing</body></html>" * 2
        result = await self.plugin.should_run("http://example.com", content)
        assert result is True

    @pytest.mark.asyncio
    async def test_should_run_too_short(self):
        """Test should_run with content too short."""
        content = "<html><body>Short</body></html>"
        result = await self.plugin.should_run("http://example.com", content)
        assert result is False

    @pytest.mark.asyncio
    async def test_should_run_not_html(self):
        """Test should_run with non-HTML content."""
        content = "This is plain text, not HTML" * 10
        result = await self.plugin.should_run("http://example.com", content)
        assert result is False
