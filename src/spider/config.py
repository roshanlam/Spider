import os
import yaml
from typing import Any, Dict

def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Load configuration from a YAML file with optional environment variable overrides.

    :param config_path: Path to the YAML configuration file.
    :return: Configuration dictionary.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, config_path)
    with open(full_path, 'r') as f:
        config = yaml.safe_load(f)
    # Environment variable overrides.
    config['threads'] = int(os.getenv("CRAWLER_THREADS", config.get('threads', 8)))
    config['rate_limit'] = float(os.getenv("CRAWLER_RATE_LIMIT", config.get('rate_limit', 1)))
    config['user_agent'] = os.getenv("CRAWLER_USER_AGENT", config.get('user_agent', "MyCrawler/1.0"))
    config['timeout'] = int(os.getenv("CRAWLER_TIMEOUT", config.get('timeout', 10)))
    config['start_url'] = os.getenv("CRAWLER_START_URL", config.get('start_url'))
    return config

config = load_config()
