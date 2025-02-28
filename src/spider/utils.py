import logging
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from typing import Any

def init_logging(log_level: int = logging.INFO) -> None:
    """
    Initialize the root logger with a console handler.

    :param log_level: Logging level (e.g., logging.DEBUG, logging.INFO)
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def normalize_url(url: str) -> str:
    """
    Normalize a URL by removing trailing slashes and sorting query parameters.

    :param url: The URL to normalize.
    :return: Normalized URL.
    """
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    # Sort query parameters to ensure consistent ordering.
    query = urlencode(sorted(parse_qsl(parsed.query)))
    normalized = urlunparse((
        parsed.scheme, parsed.netloc, path, parsed.params, query, parsed.fragment
    ))
    return normalized
