"""
Comprehensive Web Scraper Plugin

This plugin extracts structured data from webpages including:
- Metadata (title, description, keywords, author, canonical URL)
- OpenGraph and Twitter Card data
- Headings structure (h1-h6)
- Content analysis (paragraphs, word count, text length)
- Links (internal, external, with anchor text)
- Images (src, alt text, dimensions)
- Forms and input fields
- JSON-LD structured data
- Page structure and semantic analysis
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Text, JSON, Integer, DateTime, MetaData, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from spider.config import config
from spider.plugin import Plugin

# Configure the database
engine = create_engine(config['database']['url'], echo=False)
metadata = MetaData()

# Define the scraped_data table with comprehensive fields
scraped_data_table = Table(
    'scraped_data', metadata,
    Column('url', String, primary_key=True),
    Column('scraped_at', DateTime, nullable=False),
    Column('title', Text, nullable=True),
    Column('description', Text, nullable=True),
    Column('keywords', Text, nullable=True),
    Column('author', String, nullable=True),
    Column('canonical_url', String, nullable=True),
    Column('language', String, nullable=True),
    Column('word_count', Integer, nullable=True),
    Column('text_length', Integer, nullable=True),
    Column('headings', JSON, nullable=True),  # Structure of h1-h6
    Column('meta_tags', JSON, nullable=True),  # All meta tags
    Column('opengraph', JSON, nullable=True),  # OpenGraph metadata
    Column('twitter_card', JSON, nullable=True),  # Twitter Card metadata
    Column('links', JSON, nullable=True),  # Internal and external links
    Column('images', JSON, nullable=True),  # Images with details
    Column('forms', JSON, nullable=True),  # Form elements
    Column('structured_data', JSON, nullable=True),  # JSON-LD data
    Column('page_structure', JSON, nullable=True),  # Overall structure analysis
    Column('content_blocks', JSON, nullable=True),  # Main content blocks
)

# Create the table if it doesn't exist
metadata.create_all(engine)


class WebScraperPlugin(Plugin):
    """
    A comprehensive web scraping plugin that extracts and structures
    all important data from webpages for analysis and reuse.
    """

    def __init__(self, min_content_length: int = 100, extract_full_text: bool = False):
        """
        Initialize the plugin with configuration options.

        Args:
            min_content_length: Minimum content length to process (default: 100)
            extract_full_text: Whether to extract full text content (default: False)
        """
        self.min_content_length = min_content_length
        self.extract_full_text = extract_full_text

    async def should_run(self, url: str, content: str) -> bool:
        """
        Determine if the plugin should run based on content length and type.
        """
        # Only process HTML content with sufficient length
        if len(content) < self.min_content_length:
            return False

        # Check if content appears to be HTML
        if not content.strip().startswith('<'):
            return False

        return True

    async def process(self, url: str, content: str) -> str:
        """
        Extract comprehensive structured data from the webpage.
        """
        try:
            soup = BeautifulSoup(content, 'lxml')

            # Extract all data components
            scraped_data = {
                'url': url,
                'scraped_at': datetime.utcnow().isoformat(),
                'title': self._extract_title(soup),
                'description': self._extract_description(soup),
                'keywords': self._extract_keywords(soup),
                'author': self._extract_author(soup),
                'canonical_url': self._extract_canonical(soup, url),
                'language': self._extract_language(soup),
                'word_count': self._count_words(soup),
                'text_length': len(soup.get_text()),
                'headings': self._extract_headings(soup),
                'meta_tags': self._extract_meta_tags(soup),
                'opengraph': self._extract_opengraph(soup),
                'twitter_card': self._extract_twitter_card(soup),
                'links': self._extract_links(soup, url),
                'images': self._extract_images(soup, url),
                'forms': self._extract_forms(soup),
                'structured_data': self._extract_structured_data(soup),
                'page_structure': self._analyze_page_structure(soup),
                'content_blocks': self._extract_content_blocks(soup),
            }

            # Log summary
            logging.info(
                f"Scraped {url}: "
                f"{scraped_data['word_count']} words, "
                f"{len(scraped_data['links']['all'])} links, "
                f"{len(scraped_data['images'])} images"
            )

            # Save to database
            self._save_to_database(scraped_data)

        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")

        return content

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page title."""
        title_tag = soup.find('title')
        return title_tag.string.strip() if title_tag and title_tag.string else None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta description."""
        desc = soup.find('meta', attrs={'name': 'description'})
        if not desc:
            desc = soup.find('meta', attrs={'property': 'og:description'})
        return desc.get('content', '').strip() if desc else None

    def _extract_keywords(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta keywords."""
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        return keywords.get('content', '').strip() if keywords else None

    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract author information."""
        author = soup.find('meta', attrs={'name': 'author'})
        if not author:
            author = soup.find('meta', attrs={'property': 'article:author'})
        return author.get('content', '').strip() if author else None

    def _extract_canonical(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract canonical URL."""
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical and canonical.get('href'):
            return urljoin(base_url, canonical['href'])
        return None

    def _extract_language(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page language."""
        html_tag = soup.find('html')
        if html_tag:
            return html_tag.get('lang') or html_tag.get('xml:lang')
        return None

    def _count_words(self, soup: BeautifulSoup) -> int:
        """Count words in the page text content."""
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def _extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract all headings (h1-h6) with hierarchy."""
        headings = {
            'h1': [h.get_text().strip() for h in soup.find_all('h1')],
            'h2': [h.get_text().strip() for h in soup.find_all('h2')],
            'h3': [h.get_text().strip() for h in soup.find_all('h3')],
            'h4': [h.get_text().strip() for h in soup.find_all('h4')],
            'h5': [h.get_text().strip() for h in soup.find_all('h5')],
            'h6': [h.get_text().strip() for h in soup.find_all('h6')],
        }
        return headings

    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract all meta tags."""
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
            content = meta.get('content')
            if name and content:
                meta_tags[name] = content
        return meta_tags

    def _extract_opengraph(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract OpenGraph metadata."""
        og_data = {}
        for meta in soup.find_all('meta', attrs={'property': re.compile(r'^og:')}):
            prop = meta.get('property', '').replace('og:', '')
            content = meta.get('content', '')
            if prop and content:
                og_data[prop] = content
        return og_data

    def _extract_twitter_card(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract Twitter Card metadata."""
        twitter_data = {}
        for meta in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
            name = meta.get('name', '').replace('twitter:', '')
            content = meta.get('content', '')
            if name and content:
                twitter_data[name] = content
        return twitter_data

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """Extract all links with classification (internal/external)."""
        base_domain = urlparse(base_url).netloc
        links = {
            'all': [],
            'internal': [],
            'external': [],
            'count': 0
        }

        for link in soup.find_all('a', href=True):
            href = link.get('href', '').strip()
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue

            absolute_url = urljoin(base_url, href)
            link_domain = urlparse(absolute_url).netloc
            anchor_text = link.get_text().strip()

            link_data = {
                'url': absolute_url,
                'text': anchor_text,
                'title': link.get('title', ''),
            }

            links['all'].append(link_data)

            if link_domain == base_domain:
                links['internal'].append(link_data)
            else:
                links['external'].append(link_data)

        links['count'] = len(links['all'])
        return links

    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract all images with metadata."""
        images = []

        for img in soup.find_all('img'):
            src = img.get('src', '').strip()
            if not src:
                continue

            absolute_url = urljoin(base_url, src)

            image_data = {
                'src': absolute_url,
                'alt': img.get('alt', '').strip(),
                'title': img.get('title', '').strip(),
                'width': img.get('width', ''),
                'height': img.get('height', ''),
            }
            images.append(image_data)

        return images

    def _extract_forms(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract form elements and their inputs."""
        forms = []

        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get').upper(),
                'id': form.get('id', ''),
                'name': form.get('name', ''),
                'inputs': []
            }

            # Extract input fields
            for input_field in form.find_all(['input', 'textarea', 'select']):
                input_data = {
                    'type': input_field.name,
                    'name': input_field.get('name', ''),
                    'id': input_field.get('id', ''),
                    'value': input_field.get('value', ''),
                    'placeholder': input_field.get('placeholder', ''),
                    'required': input_field.has_attr('required'),
                }

                if input_field.name == 'input':
                    input_data['input_type'] = input_field.get('type', 'text')

                form_data['inputs'].append(input_data)

            forms.append(form_data)

        return forms

    def _extract_structured_data(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract JSON-LD structured data."""
        structured_data = []

        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                structured_data.append(data)
            except (json.JSONDecodeError, TypeError, AttributeError):
                continue

        return structured_data

    def _analyze_page_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze overall page structure and semantic elements."""
        structure = {
            'has_header': bool(soup.find('header')),
            'has_footer': bool(soup.find('footer')),
            'has_nav': bool(soup.find('nav')),
            'has_aside': bool(soup.find('aside')),
            'has_main': bool(soup.find('main')),
            'article_count': len(soup.find_all('article')),
            'section_count': len(soup.find_all('section')),
            'div_count': len(soup.find_all('div')),
            'table_count': len(soup.find_all('table')),
            'list_count': len(soup.find_all(['ul', 'ol'])),
        }
        return structure

    def _extract_content_blocks(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract main content blocks (articles, sections, main content)."""
        blocks = []

        # Extract article content
        for article in soup.find_all('article'):
            blocks.append({
                'type': 'article',
                'id': article.get('id', ''),
                'class': ' '.join(article.get('class', [])),
                'text': article.get_text().strip()[:500],  # First 500 chars
                'word_count': len(re.findall(r'\b\w+\b', article.get_text())),
            })

        # Extract main content
        main = soup.find('main')
        if main:
            blocks.append({
                'type': 'main',
                'id': main.get('id', ''),
                'class': ' '.join(main.get('class', [])),
                'text': main.get_text().strip()[:500],
                'word_count': len(re.findall(r'\b\w+\b', main.get_text())),
            })

        # Extract section content
        for i, section in enumerate(soup.find_all('section')[:5]):  # Limit to first 5
            blocks.append({
                'type': 'section',
                'index': i,
                'id': section.get('id', ''),
                'class': ' '.join(section.get('class', [])),
                'text': section.get_text().strip()[:500],
                'word_count': len(re.findall(r'\b\w+\b', section.get_text())),
            })

        return blocks

    def _save_to_database(self, data: Dict[str, Any]) -> None:
        """Save scraped data to PostgreSQL database."""
        try:
            stmt = pg_insert(scraped_data_table).values(
                url=data['url'],
                scraped_at=datetime.fromisoformat(data['scraped_at']),
                title=data['title'],
                description=data['description'],
                keywords=data['keywords'],
                author=data['author'],
                canonical_url=data['canonical_url'],
                language=data['language'],
                word_count=data['word_count'],
                text_length=data['text_length'],
                headings=json.dumps(data['headings']),
                meta_tags=json.dumps(data['meta_tags']),
                opengraph=json.dumps(data['opengraph']),
                twitter_card=json.dumps(data['twitter_card']),
                links=json.dumps(data['links']),
                images=json.dumps(data['images']),
                forms=json.dumps(data['forms']),
                structured_data=json.dumps(data['structured_data']),
                page_structure=json.dumps(data['page_structure']),
                content_blocks=json.dumps(data['content_blocks']),
            )

            # Update on conflict
            stmt = stmt.on_conflict_do_update(
                index_elements=['url'],
                set_={
                    'scraped_at': datetime.fromisoformat(data['scraped_at']),
                    'title': data['title'],
                    'description': data['description'],
                    'keywords': data['keywords'],
                    'author': data['author'],
                    'canonical_url': data['canonical_url'],
                    'language': data['language'],
                    'word_count': data['word_count'],
                    'text_length': data['text_length'],
                    'headings': json.dumps(data['headings']),
                    'meta_tags': json.dumps(data['meta_tags']),
                    'opengraph': json.dumps(data['opengraph']),
                    'twitter_card': json.dumps(data['twitter_card']),
                    'links': json.dumps(data['links']),
                    'images': json.dumps(data['images']),
                    'forms': json.dumps(data['forms']),
                    'structured_data': json.dumps(data['structured_data']),
                    'page_structure': json.dumps(data['page_structure']),
                    'content_blocks': json.dumps(data['content_blocks']),
                }
            )

            with engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()

            logging.info(f"Successfully saved scraped data for {data['url']}")

        except SQLAlchemyError as e:
            logging.error(f"Database error saving scraped data for {data['url']}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error saving scraped data for {data['url']}: {e}")
