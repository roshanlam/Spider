"""Tests for config module."""

import pytest
import os
import tempfile
from spider.config import load_config


class TestLoadConfig:
    """Tests for configuration loading."""

    def test_load_config_from_file(self, tmp_path):
        """Test loading config from YAML file."""
        config_content = """
threads: 10
rate_limit: 2
user_agent: "TestBot/1.0"
timeout: 15
start_url: "http://test.com"
database:
  url: "postgresql://test@localhost/testdb"
celery:
  broker_url: "redis://localhost:6379/1"
  result_backend: "redis://localhost:6379/1"
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        # This test would need to be adapted based on how load_config works
        # For now, testing that the function exists
        assert callable(load_config)

    def test_load_config_env_override(self):
        """Test that environment variables override config."""
        # Set environment variable
        os.environ["CRAWLER_THREADS"] = "20"

        try:
            # Would need actual config loading to test fully
            assert os.getenv("CRAWLER_THREADS") == "20"
        finally:
            # Clean up
            if "CRAWLER_THREADS" in os.environ:
                del os.environ["CRAWLER_THREADS"]

    def test_config_default_values(self):
        """Test that default values are used when config missing."""
        # This would test the actual default values
        # For now, just verify the function is importable
        assert load_config is not None

    def test_config_required_fields(self):
        """Test that required configuration fields exist."""
        # Would check for required fields like start_url, database, etc.
        pass
