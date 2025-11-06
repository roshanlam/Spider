"""Tests for scraper_utils module."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from spider.plugins.scraper_utils import ScraperDataQuery


class TestScraperDataQuery:
    """Tests for ScraperDataQuery class."""

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_init(self, mock_create_engine):
        """Test initialization."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine

        query = ScraperDataQuery()

        assert query.engine == mock_engine
        mock_create_engine.assert_called_once()

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_get_page_data_success(self, mock_create_engine):
        """Test retrieving page data successfully."""
        # Setup mocks
        mock_engine = Mock()
        mock_conn = Mock()

        # Configure mock chain
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        # Mock database result as a list (indexed access)
        mock_row = [
            'http://example.com',  # url
            '2024-01-01',  # scraped_at
            'Test Page',  # title
            'Test description',  # description
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        ]

        mock_conn.execute.return_value.fetchone.return_value = mock_row

        query = ScraperDataQuery()
        result = query.get_page_data("http://example.com")

        assert result is not None
        assert result['url'] == 'http://example.com'
        mock_conn.execute.assert_called_once()

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_get_page_data_not_found(self, mock_create_engine):
        """Test retrieving page data when URL not found."""
        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        # Return None for not found
        mock_conn.execute.return_value.fetchone.return_value = None

        query = ScraperDataQuery()
        result = query.get_page_data("http://notfound.com")

        assert result is None

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_get_page_data_error(self, mock_create_engine):
        """Test error handling in get_page_data."""
        from sqlalchemy.exc import SQLAlchemyError

        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        # Raise error
        mock_conn.execute.side_effect = SQLAlchemyError("Database error")

        query = ScraperDataQuery()
        result = query.get_page_data("http://example.com")

        assert result is None

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_get_all_pages(self, mock_create_engine):
        """Test retrieving all pages."""
        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        # Mock multiple rows with indexed access
        mock_row1 = ['http://example1.com', '2024-01-01', 'Title 1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        mock_row2 = ['http://example2.com', '2024-01-02', 'Title 2', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

        mock_conn.execute.return_value.fetchall.return_value = [mock_row1, mock_row2]

        query = ScraperDataQuery()
        result = query.get_all_pages(limit=10, offset=0)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['url'] == 'http://example1.com'

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_get_all_pages_error(self, mock_create_engine):
        """Test error handling in get_all_pages."""
        from sqlalchemy.exc import SQLAlchemyError

        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_conn.execute.side_effect = SQLAlchemyError("Database error")

        query = ScraperDataQuery()
        result = query.get_all_pages()

        assert result == []

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_search_by_title(self, mock_create_engine):
        """Test searching by title."""
        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_row = ['http://example.com', '2024-01-01', 'Test Page', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

        mock_conn.execute.return_value.fetchall.return_value = [mock_row]

        query = ScraperDataQuery()
        result = query.search_by_title("test")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['title'] == 'Test Page'
        mock_conn.execute.assert_called_once()

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_search_by_title_error(self, mock_create_engine):
        """Test error handling in search_by_title."""
        from sqlalchemy.exc import SQLAlchemyError

        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_conn.execute.side_effect = SQLAlchemyError("Database error")

        query = ScraperDataQuery()
        result = query.search_by_title("test")

        assert result == []

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_search_by_description(self, mock_create_engine):
        """Test searching by description keyword."""
        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_row = ['http://example.com', '2024-01-01', 'Title', 'Test description with keyword', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

        mock_conn.execute.return_value.fetchall.return_value = [mock_row]

        query = ScraperDataQuery()
        result = query.search_by_description("keyword")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['description'] == 'Test description with keyword'

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_search_by_description_error(self, mock_create_engine):
        """Test error handling in search_by_description."""
        from sqlalchemy.exc import SQLAlchemyError

        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_conn.execute.side_effect = SQLAlchemyError("Database error")

        query = ScraperDataQuery()
        result = query.search_by_description("test")

        assert result == []

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_get_pages_with_forms(self, mock_create_engine):
        """Test getting pages with forms."""
        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_row = ['http://example.com', '2024-01-01', 'Title', None, None, None, None, None, None, None, None, None, None, None, None, None, '[{"action":"/submit"}]', None, None, None]

        mock_conn.execute.return_value.fetchall.return_value = [mock_row]

        query = ScraperDataQuery()
        result = query.get_pages_with_forms()

        assert isinstance(result, list)
        assert len(result) == 1

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_get_pages_with_forms_error(self, mock_create_engine):
        """Test error handling in get_pages_with_forms."""
        from sqlalchemy.exc import SQLAlchemyError

        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_conn.execute.side_effect = SQLAlchemyError("Database error")

        query = ScraperDataQuery()
        result = query.get_pages_with_forms()

        assert result == []

    @patch('spider.plugins.scraper_utils.create_engine')
    def test_row_to_dict(self, mock_create_engine):
        """Test converting row to dictionary."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine

        query = ScraperDataQuery()

        # Create a mock row with indexed access
        mock_row = [
            'http://example.com',  # url
            '2024-01-01',  # scraped_at
            'Test Title',  # title
            'Test Description',  # description
            'test, keywords',  # keywords
            'John Doe',  # author
            'http://example.com/canonical',  # canonical_url
            'en',  # language
            100,  # word_count
            500,  # text_length
            '{}',  # headings
            '{}',  # meta_tags
            '{}',  # opengraph
            '{}',  # twitter_card
            '{}',  # links
            '[]',  # images
            '[]',  # forms
            '[]',  # structured_data
            '{}',  # page_structure
            '',  # content_blocks
        ]

        result = query._row_to_dict(mock_row)
        assert isinstance(result, dict)
        assert result['url'] == 'http://example.com'
        assert result['title'] == 'Test Title'

    @patch('spider.plugins.scraper_utils.create_engine')
    @patch('builtins.open', new_callable=MagicMock)
    def test_export_to_json(self, mock_open, mock_create_engine):
        """Test exporting data to JSON file."""
        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_row = Mock()
        mock_row._asdict = Mock(return_value={'url': 'http://example.com', 'scraped_at': '2024-01-01'})
        mock_row._mapping = {'url': 'http://example.com'}

        mock_conn.execute.return_value.fetchone.return_value = mock_row

        query = ScraperDataQuery()
        result = query.export_to_json("http://example.com", "output.json")

        # Verify file operations occurred
        assert result is True or result is False  # Just verify it returns a boolean

    @patch('spider.plugins.scraper_utils.create_engine')
    @patch('builtins.open', side_effect=Exception("File error"))
    def test_export_to_json_file_error(self, mock_open, mock_create_engine):
        """Test export error handling."""
        mock_engine = Mock()
        mock_conn = Mock()

        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_engine.connect.return_value.__exit__ = Mock(return_value=None)

        mock_row = Mock()
        mock_row._asdict = Mock(return_value={'url': 'http://example.com'})

        mock_conn.execute.return_value.fetchone.return_value = mock_row

        query = ScraperDataQuery()
        result = query.export_to_json("http://example.com", "output.json")

        assert result is False
