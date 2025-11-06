"""
Web Scraper Plugin - Complete Usage Example

This example demonstrates how to use the WebScraperPlugin to extract
comprehensive data from websites and analyze the results.
"""

import asyncio
import logging
from spider.spider import Spider
from spider.plugin import PluginManager
from spider.plugins.web_scraper_plugin import WebScraperPlugin
from spider.plugins.scraper_utils import ScraperDataQuery, get_page_data, search_pages, get_statistics
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def example_basic_scraping():
    """
    Example 1: Basic web scraping with the plugin
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Web Scraping")
    print("="*80 + "\n")

    # Create plugin manager
    plugin_manager = PluginManager()

    # Register the web scraper plugin
    plugin_manager.register(WebScraperPlugin(
        min_content_length=100,
        extract_full_text=False
    ))

    # Create spider with the plugin
    spider = Spider(
        start_url="https://example.com",
        max_depth=2,
        plugin_manager=plugin_manager
    )

    # Run the crawler
    print("Starting crawl...")
    await spider.crawl()
    print("Crawl completed!")


def example_query_data():
    """
    Example 2: Query and analyze scraped data
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Querying Scraped Data")
    print("="*80 + "\n")

    query = ScraperDataQuery()

    # Get data for a specific URL
    url = "https://example.com"
    page_data = query.get_page_data(url)

    if page_data:
        print(f"📄 Page: {page_data['url']}")
        print(f"📝 Title: {page_data['title']}")
        print(f"📊 Word Count: {page_data['word_count']}")
        print(f"🔗 Total Links: {json.loads(page_data['links'])['count']}")
        print(f"🖼️  Images: {len(json.loads(page_data['images']))}")
        print(f"📋 Forms: {len(json.loads(page_data['forms']))}")
        print(f"🌐 Language: {page_data['language']}")
        print(f"⏰ Scraped: {page_data['scraped_at']}")


def example_analyze_links():
    """
    Example 3: Analyze internal and external links
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Link Analysis")
    print("="*80 + "\n")

    query = ScraperDataQuery()
    url = "https://example.com"

    # Get internal links
    internal_links = query.get_internal_links(url)
    print(f"🔗 Internal Links ({len(internal_links)}):")
    for link in internal_links[:5]:  # Show first 5
        print(f"  • {link['url']}")
        print(f"    Text: {link['text']}")

    print()

    # Get external links
    external_links = query.get_external_links(url)
    print(f"🌐 External Links ({len(external_links)}):")
    for link in external_links[:5]:  # Show first 5
        print(f"  • {link['url']}")
        print(f"    Text: {link['text']}")


def example_analyze_seo():
    """
    Example 4: SEO Analysis
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: SEO Analysis")
    print("="*80 + "\n")

    query = ScraperDataQuery()
    pages = query.get_all_pages(limit=50)

    print("Running SEO checks...\n")

    issues = {
        'missing_title': [],
        'short_description': [],
        'no_h1': [],
        'multiple_h1': [],
        'missing_og': []
    }

    for page in pages:
        url = page['url']

        # Check title
        if not page['title']:
            issues['missing_title'].append(url)

        # Check description length
        if not page['description'] or len(page['description']) < 50:
            issues['short_description'].append(url)

        # Check H1 headings
        headings = json.loads(page['headings'])
        if len(headings['h1']) == 0:
            issues['no_h1'].append(url)
        elif len(headings['h1']) > 1:
            issues['multiple_h1'].append(url)

        # Check OpenGraph
        og = json.loads(page['opengraph'])
        if not og or 'title' not in og:
            issues['missing_og'].append(url)

    # Report issues
    print("🔍 SEO Issues Found:\n")
    print(f"❌ Missing Title: {len(issues['missing_title'])} pages")
    print(f"⚠️  Short/Missing Description: {len(issues['short_description'])} pages")
    print(f"❌ No H1 Heading: {len(issues['no_h1'])} pages")
    print(f"⚠️  Multiple H1 Headings: {len(issues['multiple_h1'])} pages")
    print(f"📱 Missing OpenGraph: {len(issues['missing_og'])} pages")

    # Show examples
    if issues['no_h1']:
        print(f"\nPages without H1 (first 3):")
        for url in issues['no_h1'][:3]:
            print(f"  • {url}")


def example_content_analysis():
    """
    Example 5: Content analysis by word count
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Content Analysis")
    print("="*80 + "\n")

    query = ScraperDataQuery()

    # Find short articles
    short_articles = query.find_pages_by_word_count(min_words=0, max_words=500)
    print(f"📄 Short Articles (< 500 words): {len(short_articles)}")

    # Find medium articles
    medium_articles = query.find_pages_by_word_count(min_words=500, max_words=1500)
    print(f"📄 Medium Articles (500-1500 words): {len(medium_articles)}")

    # Find long articles
    long_articles = query.find_pages_by_word_count(min_words=1500)
    print(f"📄 Long Articles (> 1500 words): {len(long_articles)}")

    # Show statistics
    stats = query.get_page_statistics()
    print(f"\n📊 Average Word Count: {stats['average_word_count']:.0f} words")


def example_structured_data():
    """
    Example 6: Extract structured data (JSON-LD)
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Structured Data Extraction")
    print("="*80 + "\n")

    query = ScraperDataQuery()
    url = "https://example.com"

    # Get structured data
    structured = query.get_structured_data(url)

    if structured:
        print(f"Found {len(structured)} structured data items:\n")
        for i, item in enumerate(structured, 1):
            print(f"Item {i}:")
            print(f"  Type: {item.get('@type', 'Unknown')}")
            print(f"  Context: {item.get('@context', 'N/A')}")

            # Show some fields
            for key, value in list(item.items())[:5]:
                if key not in ['@type', '@context']:
                    print(f"  {key}: {value}")
            print()
    else:
        print("No structured data found on this page.")


def example_image_analysis():
    """
    Example 7: Image extraction and analysis
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Image Analysis")
    print("="*80 + "\n")

    query = ScraperDataQuery()
    url = "https://example.com"

    images = query.get_images(url)

    print(f"🖼️  Found {len(images)} images:\n")

    # Analyze images
    images_with_alt = sum(1 for img in images if img['alt'])
    images_without_alt = len(images) - images_with_alt

    print(f"✅ Images with alt text: {images_with_alt}")
    print(f"❌ Images without alt text: {images_without_alt}")

    # Show first few images
    print(f"\nFirst 5 images:")
    for i, img in enumerate(images[:5], 1):
        print(f"\n{i}. {img['src']}")
        print(f"   Alt: {img['alt'] or '(missing)'}")
        if img['width'] or img['height']:
            print(f"   Size: {img['width']}x{img['height']}")


def example_forms_detection():
    """
    Example 8: Detect and analyze forms
    """
    print("\n" + "="*80)
    print("EXAMPLE 8: Form Detection")
    print("="*80 + "\n")

    query = ScraperDataQuery()

    # Find all pages with forms
    pages_with_forms = query.get_pages_with_forms()

    print(f"📋 Found {len(pages_with_forms)} pages with forms:\n")

    for page in pages_with_forms[:5]:  # Show first 5
        print(f"Page: {page['url']}")
        forms = json.loads(page['forms'])

        for i, form in enumerate(forms, 1):
            print(f"  Form {i}:")
            print(f"    Action: {form['action']}")
            print(f"    Method: {form['method']}")
            print(f"    Inputs: {len(form['inputs'])}")

            # Show input types
            input_types = [inp.get('input_type', inp['type']) for inp in form['inputs']]
            print(f"    Types: {', '.join(set(input_types))}")

        print()


def example_search_functionality():
    """
    Example 9: Search scraped pages
    """
    print("\n" + "="*80)
    print("EXAMPLE 9: Search Functionality")
    print("="*80 + "\n")

    # Search by keyword
    keyword = "example"
    results = search_pages(keyword)

    print(f"🔍 Search results for '{keyword}' ({len(results)} found):\n")

    for i, result in enumerate(results[:5], 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Description: {result['description'][:100]}..." if result['description'] else "   No description")
        print()


def example_export_data():
    """
    Example 10: Export data to JSON
    """
    print("\n" + "="*80)
    print("EXAMPLE 10: Export Data")
    print("="*80 + "\n")

    query = ScraperDataQuery()
    url = "https://example.com"
    output_file = "example_com_export.json"

    success = query.export_to_json(url, output_file)

    if success:
        print(f"✅ Data exported successfully to {output_file}")
        print(f"📄 You can now use this data in other applications")
    else:
        print(f"❌ Failed to export data")


def example_statistics():
    """
    Example 11: Overall statistics
    """
    print("\n" + "="*80)
    print("EXAMPLE 11: Overall Statistics")
    print("="*80 + "\n")

    stats = get_statistics()

    print("📊 Scraping Statistics:\n")
    print(f"📄 Total Pages Scraped: {stats['total_pages']}")
    print(f"📝 Average Word Count: {stats['average_word_count']:.0f} words")
    print(f"📋 Pages with Forms: {stats['pages_with_forms']}")
    print(f"🔗 Pages with Structured Data: {stats['pages_with_structured_data']}")

    print(f"\n🌐 Languages:")
    for lang_info in stats['languages'][:5]:
        print(f"  • {lang_info['language']}: {lang_info['count']} pages")


def example_headings_structure():
    """
    Example 12: Analyze heading structure
    """
    print("\n" + "="*80)
    print("EXAMPLE 12: Headings Structure Analysis")
    print("="*80 + "\n")

    query = ScraperDataQuery()
    url = "https://example.com"

    headings = query.get_headings_structure(url)

    print("📋 Headings Hierarchy:\n")

    for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        if headings.get(level):
            print(f"{level.upper()} ({len(headings[level])}):")
            for heading in headings[level][:3]:  # Show first 3
                print(f"  • {heading}")
            if len(headings[level]) > 3:
                print(f"  ... and {len(headings[level]) - 3} more")
            print()


def main():
    """
    Run all examples
    """
    print("\n" + "="*80)
    print("Web Scraper Plugin - Complete Examples")
    print("="*80)

    # Run the async example first (if needed)
    # asyncio.run(example_basic_scraping())

    # Run synchronous examples
    # Note: These assume you've already scraped some data

    try:
        example_query_data()
        example_analyze_links()
        example_analyze_seo()
        example_content_analysis()
        example_structured_data()
        example_image_analysis()
        example_forms_detection()
        example_search_functionality()
        example_export_data()
        example_statistics()
        example_headings_structure()

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have scraped some data first by running the crawler.")

    print("\n" + "="*80)
    print("Examples completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    # To run the scraping example:
    # asyncio.run(example_basic_scraping())

    # To run the analysis examples (after scraping):
    main()
