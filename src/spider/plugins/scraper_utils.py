"""
Web Scraper Utility Module

Provides helper functions to query and analyze data collected by the WebScraperPlugin.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import SQLAlchemyError
from spider.config import config


class ScraperDataQuery:
    """
    Utility class for querying and analyzing scraped webpage data.
    """

    def __init__(self):
        """Initialize database connection."""
        self.engine = create_engine(config['database']['url'], echo=False)

    def get_page_data(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve all scraped data for a specific URL.

        Args:
            url: The URL to retrieve data for

        Returns:
            Dictionary containing all scraped data, or None if not found
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM scraped_data WHERE url = :url"),
                    {"url": url}
                ).fetchone()

                if result:
                    return self._row_to_dict(result)
                return None

        except SQLAlchemyError as e:
            logging.error(f"Error retrieving data for {url}: {e}")
            return None

    def get_all_pages(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieve all scraped pages with pagination.

        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            List of dictionaries containing scraped data
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM scraped_data ORDER BY scraped_at DESC LIMIT :limit OFFSET :offset"),
                    {"limit": limit, "offset": offset}
                ).fetchall()

                return [self._row_to_dict(row) for row in result]

        except SQLAlchemyError as e:
            logging.error(f"Error retrieving all pages: {e}")
            return []

    def search_by_title(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search for pages by title keyword.

        Args:
            keyword: Keyword to search for in titles

        Returns:
            List of matching pages
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM scraped_data WHERE title ILIKE :keyword ORDER BY scraped_at DESC"),
                    {"keyword": f"%{keyword}%"}
                ).fetchall()

                return [self._row_to_dict(row) for row in result]

        except SQLAlchemyError as e:
            logging.error(f"Error searching by title: {e}")
            return []

    def search_by_description(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search for pages by description keyword.

        Args:
            keyword: Keyword to search for in descriptions

        Returns:
            List of matching pages
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM scraped_data WHERE description ILIKE :keyword ORDER BY scraped_at DESC"),
                    {"keyword": f"%{keyword}%"}
                ).fetchall()

                return [self._row_to_dict(row) for row in result]

        except SQLAlchemyError as e:
            logging.error(f"Error searching by description: {e}")
            return []

    def get_pages_with_forms(self) -> List[Dict[str, Any]]:
        """
        Get all pages that contain forms.

        Returns:
            List of pages with forms
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM scraped_data WHERE forms::text != '[]' ORDER BY scraped_at DESC")
                ).fetchall()

                return [self._row_to_dict(row) for row in result]

        except SQLAlchemyError as e:
            logging.error(f"Error retrieving pages with forms: {e}")
            return []

    def get_external_links(self, url: str) -> List[Dict[str, str]]:
        """
        Get all external links from a specific page.

        Args:
            url: The URL to get external links from

        Returns:
            List of external links
        """
        page_data = self.get_page_data(url)
        if page_data and page_data.get('links'):
            links = json.loads(page_data['links'])
            return links.get('external', [])
        return []

    def get_internal_links(self, url: str) -> List[Dict[str, str]]:
        """
        Get all internal links from a specific page.

        Args:
            url: The URL to get internal links from

        Returns:
            List of internal links
        """
        page_data = self.get_page_data(url)
        if page_data and page_data.get('links'):
            links = json.loads(page_data['links'])
            return links.get('internal', [])
        return []

    def get_images(self, url: str) -> List[Dict[str, str]]:
        """
        Get all images from a specific page.

        Args:
            url: The URL to get images from

        Returns:
            List of images with metadata
        """
        page_data = self.get_page_data(url)
        if page_data and page_data.get('images'):
            return json.loads(page_data['images'])
        return []

    def get_structured_data(self, url: str) -> List[Dict[str, Any]]:
        """
        Get JSON-LD structured data from a specific page.

        Args:
            url: The URL to get structured data from

        Returns:
            List of structured data objects
        """
        page_data = self.get_page_data(url)
        if page_data and page_data.get('structured_data'):
            return json.loads(page_data['structured_data'])
        return []

    def get_page_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics about scraped pages.

        Returns:
            Dictionary containing various statistics
        """
        try:
            with self.engine.connect() as conn:
                # Total pages
                total = conn.execute(
                    text("SELECT COUNT(*) FROM scraped_data")
                ).scalar()

                # Average word count
                avg_words = conn.execute(
                    text("SELECT AVG(word_count) FROM scraped_data WHERE word_count IS NOT NULL")
                ).scalar()

                # Pages with forms
                pages_with_forms = conn.execute(
                    text("SELECT COUNT(*) FROM scraped_data WHERE forms::text != '[]'")
                ).scalar()

                # Pages with structured data
                pages_with_structured_data = conn.execute(
                    text("SELECT COUNT(*) FROM scraped_data WHERE structured_data::text != '[]'")
                ).scalar()

                # Most common languages
                languages = conn.execute(
                    text("SELECT language, COUNT(*) as count FROM scraped_data WHERE language IS NOT NULL GROUP BY language ORDER BY count DESC LIMIT 10")
                ).fetchall()

                return {
                    'total_pages': total,
                    'average_word_count': round(float(avg_words), 2) if avg_words else 0,
                    'pages_with_forms': pages_with_forms,
                    'pages_with_structured_data': pages_with_structured_data,
                    'languages': [{'language': lang[0], 'count': lang[1]} for lang in languages]
                }

        except SQLAlchemyError as e:
            logging.error(f"Error getting statistics: {e}")
            return {}

    def export_to_json(self, url: str, output_file: str) -> bool:
        """
        Export scraped data for a URL to a JSON file.

        Args:
            url: The URL to export
            output_file: Path to the output JSON file

        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.get_page_data(url)
            if data:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                logging.info(f"Exported data for {url} to {output_file}")
                return True
            else:
                logging.warning(f"No data found for {url}")
                return False

        except Exception as e:
            logging.error(f"Error exporting data: {e}")
            return False

    def get_headings_structure(self, url: str) -> Dict[str, List[str]]:
        """
        Get the headings structure for a specific page.

        Args:
            url: The URL to get headings from

        Returns:
            Dictionary with heading levels (h1-h6) and their text
        """
        page_data = self.get_page_data(url)
        if page_data and page_data.get('headings'):
            return json.loads(page_data['headings'])
        return {}

    def get_opengraph_data(self, url: str) -> Dict[str, str]:
        """
        Get OpenGraph metadata for a specific page.

        Args:
            url: The URL to get OpenGraph data from

        Returns:
            Dictionary with OpenGraph properties
        """
        page_data = self.get_page_data(url)
        if page_data and page_data.get('opengraph'):
            return json.loads(page_data['opengraph'])
        return {}

    def find_pages_by_word_count(self, min_words: int = 0, max_words: int = 999999) -> List[Dict[str, Any]]:
        """
        Find pages within a specific word count range.

        Args:
            min_words: Minimum word count
            max_words: Maximum word count

        Returns:
            List of matching pages
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM scraped_data WHERE word_count BETWEEN :min AND :max ORDER BY word_count DESC"),
                    {"min": min_words, "max": max_words}
                ).fetchall()

                return [self._row_to_dict(row) for row in result]

        except SQLAlchemyError as e:
            logging.error(f"Error finding pages by word count: {e}")
            return []

    def _row_to_dict(self, row) -> Dict[str, Any]:
        """
        Convert a database row to a dictionary.

        Args:
            row: Database row object

        Returns:
            Dictionary representation of the row
        """
        return {
            'url': row[0],
            'scraped_at': str(row[1]),
            'title': row[2],
            'description': row[3],
            'keywords': row[4],
            'author': row[5],
            'canonical_url': row[6],
            'language': row[7],
            'word_count': row[8],
            'text_length': row[9],
            'headings': row[10],
            'meta_tags': row[11],
            'opengraph': row[12],
            'twitter_card': row[13],
            'links': row[14],
            'images': row[15],
            'forms': row[16],
            'structured_data': row[17],
            'page_structure': row[18],
            'content_blocks': row[19],
        }


# Convenience functions for quick access
def get_page_data(url: str) -> Optional[Dict[str, Any]]:
    """Quick function to get page data."""
    query = ScraperDataQuery()
    return query.get_page_data(url)


def search_pages(keyword: str) -> List[Dict[str, Any]]:
    """Quick function to search pages by keyword."""
    query = ScraperDataQuery()
    title_results = query.search_by_title(keyword)
    desc_results = query.search_by_description(keyword)

    # Combine and deduplicate
    seen_urls = set()
    combined = []
    for result in title_results + desc_results:
        if result['url'] not in seen_urls:
            seen_urls.add(result['url'])
            combined.append(result)

    return combined


def get_statistics() -> Dict[str, Any]:
    """Quick function to get scraping statistics."""
    query = ScraperDataQuery()
    return query.get_page_statistics()
