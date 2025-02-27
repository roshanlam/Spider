# Plugin Development Guide for Spider

Plugins extend the functionality of the Spider crawler by processing or modifying the content of crawled pages.
They can extract metadata, filter or transform content, or integrate with external systems.

## Plugin Architecture Overview
The crawler uses a simple plugin system based on two classes:

**Plugin**: The base class for all plugins. It defines the interface (a single process method) that plugins must implement.
**PluginManager**: This class manages and executes registered plugins sequentially on the crawled content.

## How to Create a Custom Plugin
1. Create a New Module
Create a new Python file (e.g., my_custom_plugin.py) for your plugin. It's best to create in inside the plugins folder.
2. Import the Base Plugin Class
Import the Plugin class from the plugin module:
```python
from plugin import Plugin
```
3. Subclass the Plugin Class
Create a new class that inherits from Plugin. Implement the process method:
```python
class MyCustomPlugin(Plugin):
    def process(self, url: str, content: str) -> str:
        # Your custom processing logic here.
        return content
```

4. Implement the Process Method
The process method should:

Accept two parameters:
* **url**: The URL of the crawled page.
* **content**: The HTML content as a string.
Perform any custom operations (e.g., extracting metadata, filtering, modifying content).
Return the processed content (or the original content if no changes are made).

## Example: TitleLoggerPlugin
The following example extracts and logs the page title:

```python
import logging
from bs4 import BeautifulSoup
from plugin import Plugin

class TitleLoggerPlugin(Plugin):
    def process(self, url: str, content: str) -> str:
        try:
            soup = BeautifulSoup(content, 'lxml')
            title_tag = soup.find('title')
            if title_tag and title_tag.string:
                title = title_tag.string.strip()
                logging.info(f"Page Title for {url}: {title}")
            else:
                logging.info(f"No title found for {url}")
        except Exception as e:
            logging.error(f"Error processing title for {url}: {e}")
        return content
```

5. Register Your Plugin
In your main application (or during crawler setup), import and register your plugin with the `PluginManager`:
```python
from plugin import PluginManager
from title_logger_plugin import TitleLoggerPlugin

plugin_manager = PluginManager()
plugin_manager.register(TitleLoggerPlugin())
```

## Best Practices for Plugin Development

* Error Handling:
Wrap your processing logic in try-except blocks. Use logging to record errors without halting the crawler.

* Non-blocking Code:
Since the crawler operates asynchronously, avoid long-running synchronous tasks. Offload heavy processing if needed.

* Modularity:
Focus on a single responsibility per plugin. If your logic becomes too complex, split it into multiple plugins.

* Logging:
Use the built-in logging module to record useful information. This helps in debugging and monitoring plugin behavior.

* Testing:
Write unit tests for your plugins. Ensure that they handle both expected inputs and edge cases gracefully.

* Documentation:
Include clear docstrings in your plugin classes and methods. Explain what each plugin does and any configuration it may require.


Once your plugin is implemented and documented, register it within your main crawler configuration.
For example, in main.py:
```python
import asyncio
import logging
from config import config
from spider import Spider
from plugin import PluginManager
from utils import init_logging
from title_logger_plugin import TitleLoggerPlugin

def main() -> None:
    init_logging(logging.INFO)
    plugin_manager = PluginManager()
    # Register the custom TitleLoggerPlugin
    plugin_manager.register(TitleLoggerPlugin())
    crawler = Spider(config['start_url'], config, plugin_manager)
    asyncio.run(crawler.crawl())

if __name__ == '__main__':
    main()
```
