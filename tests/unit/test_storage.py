"""Tests for storage module."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from spider.storage import save_page, engine, pages_table


class TestSavePage:
    """Tests for save_page function."""

    @patch('spider.storage.SessionLocal')
    def test_save_page_success(self, mock_session_local):
        """Test saving a page successfully."""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        url = "http://example.com"
        content = "<html>Test</html>"

        save_page(url, content)

        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch('spider.storage.SessionLocal')
    def test_save_page_integrity_error(self, mock_session_local):
        """Test handling duplicate page insertion."""
        from sqlalchemy.exc import IntegrityError
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.execute.side_effect = IntegrityError("", "", "")

        url = "http://example.com"
        content = "<html>Test</html>"

        # Should not raise exception
        save_page(url, content)

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()

    @patch('spider.storage.SessionLocal')
    def test_save_page_sqlalchemy_error(self, mock_session_local):
        """Test handling general database errors."""
        from sqlalchemy.exc import SQLAlchemyError
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.execute.side_effect = SQLAlchemyError("Database error")

        url = "http://example.com"
        content = "<html>Test</html>"

        # Should not raise exception
        save_page(url, content)

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()

    def test_pages_table_exists(self):
        """Test that pages table is defined."""
        assert pages_table is not None
        assert pages_table.name == 'pages'

    def test_engine_exists(self):
        """Test that engine is created."""
        assert engine is not None
