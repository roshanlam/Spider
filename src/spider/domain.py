from urllib.parse import urlparse

def get_domain_name(url: str) -> str:
    """
    Extract the main domain name from a URL.

    :param url: The URL to process.
    :return: The domain name (e.g., example.com).
    """
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except Exception:
        return ''

def get_sub_domain_name(url: str) -> str:
    """
    Extract the sub-domain and domain from a URL.

    :param url: The URL to process.
    :return: The sub-domain and domain.
    """
    try:
        return urlparse(url).netloc
    except Exception:
        return ''
