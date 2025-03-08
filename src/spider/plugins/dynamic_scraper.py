import asyncio
import logging
from playwright.async_api import async_playwright
from spider.plugin import Plugin

class DynamicScraperPlugin(Plugin):
    async def should_run(self, url: str, content: str) -> bool:
        """
        Determine if this plugin should run. Here we assume that if the content length
        is below a threshold, it might be dynamically rendered.
        """
        return len(content.strip()) < 200

    async def process(self, url: str, content: str) -> str:
        """
        Uses Playwright to render the page and extract text and image URLs.
        Returns the fully rendered HTML content.
        """
        logging.info(f"DynamicScraperPlugin: Rendering {url} with Playwright")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("networkidle")
                rendered_html = await page.content()

                # Extract visible text content from the page.
                text = await page.evaluate("() => document.body.innerText")

                # Extract all image URLs using query selectors.
                image_elements = await page.query_selector_all("img")
                images = []
                for img in image_elements:
                    src = await img.get_attribute("src")
                    if src:
                        images.append(src)

                await browser.close()

                logging.info(
                    f"DynamicScraperPlugin: {url} - Rendered text length: {len(text)}; "
                    f"Found {len(images)} images: {images}"
                )
                return rendered_html
        except Exception as e:
            logging.error(f"DynamicScraperPlugin: Error processing {url}: {e}")
            return content
