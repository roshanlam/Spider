"""Tests for domain module."""

import pytest
from spider.domain import get_domain_name, get_sub_domain_name


class TestGetDomainName:
    """Tests for get_domain_name function."""

    def test_get_domain_name_simple(self):
        """Test getting domain from simple URL."""
        assert get_domain_name("http://example.com") == "example.com"
        assert get_domain_name("https://example.com") == "example.com"

    def test_get_domain_name_with_path(self):
        """Test getting domain from URL with path."""
        assert get_domain_name("http://example.com/path/to/page") == "example.com"

    def test_get_domain_name_with_subdomain(self):
        """Test getting domain from URL with subdomain."""
        domain = get_domain_name("http://sub.example.com")
        assert domain == "example.com"

    def test_get_domain_name_with_port(self):
        """Test getting domain from URL with port."""
        domain = get_domain_name("http://example.com:8080")
        assert "example.com" in domain

    def test_get_domain_name_with_query(self):
        """Test getting domain from URL with query string."""
        assert get_domain_name("http://example.com?query=value") == "example.com"

    def test_get_domain_name_complex_url(self):
        """Test getting domain from complex URL."""
        url = "https://sub.example.com:8080/path?query=value#fragment"
        domain = get_domain_name(url)
        # Port is included in domain extraction
        assert domain == "example.com:8080"

    def test_get_domain_name_error_handling(self):
        """Test error handling with invalid URL."""
        result = get_domain_name("")
        assert result == ""


class TestGetSubDomainName:
    """Tests for get_sub_domain_name function."""

    def test_get_sub_domain_name_simple(self):
        """Test getting subdomain from simple URL."""
        result = get_sub_domain_name("http://example.com")
        assert result == "example.com"

    def test_get_sub_domain_name_with_subdomain(self):
        """Test getting subdomain with subdomain."""
        result = get_sub_domain_name("http://sub.example.com")
        assert result == "sub.example.com"

    def test_get_sub_domain_name_with_www(self):
        """Test getting subdomain with www."""
        result = get_sub_domain_name("http://www.example.com")
        assert result == "www.example.com"

    def test_get_sub_domain_name_with_port(self):
        """Test getting subdomain with port."""
        result = get_sub_domain_name("http://example.com:8080")
        assert "example.com" in result

    def test_get_sub_domain_name_error(self):
        """Test error handling."""
        result = get_sub_domain_name("")
        assert result == ""
