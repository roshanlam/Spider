#!/usr/bin/env python3
"""
Simple script to query scraped data.

Usage:
    poetry run python query_data.py
"""

from spider.plugins.scraper_utils import ScraperDataQuery
import json
import sys


def main():
    query = ScraperDataQuery()

    print('=' * 70)
    print('📊 WEB SCRAPER DATA QUERY')
    print('=' * 70)

    # Get statistics
    stats = query.get_page_statistics()
    print(f'\n📈 Statistics:')
    print(f'   Total Pages: {stats["total_pages"]}')
    print(f'   Average Words: {stats["average_word_count"]:.0f}')
    print(f'   Pages with Forms: {stats["pages_with_forms"]}')
    print(f'   Pages with Structured Data: {stats["pages_with_structured_data"]}')

    if stats["total_pages"] == 0:
        print('\n⚠️  No data found. Run the crawler first:')
        print('   poetry run python run.py')
        return

    # Get all pages
    pages = query.get_all_pages(limit=10)
    print(f'\n📄 Recent Pages (showing up to 10):')
    print('-' * 70)

    for i, page in enumerate(pages, 1):
        print(f'\n{i}. {page["url"]}')
        print(f'   Title: {page["title"]}')
        print(f'   Words: {page["word_count"]} | Language: {page["language"]}')

        # Show links summary
        links = json.loads(page['links'])
        print(f'   Links: {links["count"]} total', end='')
        print(f' ({len(links["internal"])} internal, {len(links["external"])} external)')

        # Show images
        images = json.loads(page['images'])
        print(f'   Images: {len(images)}')

        # Show headings
        headings = json.loads(page['headings'])
        h1_count = len(headings.get('h1', []))
        if h1_count > 0:
            print(f'   H1: "{headings["h1"][0]}"')

    print('\n' + '=' * 70)
    print('💡 Tips:')
    print('   - Export data: q.export_to_json(url, "output.json")')
    print('   - Search pages: q.search_by_title("keyword")')
    print('   - Find forms: q.get_pages_with_forms()')
    print('=' * 70 + '\n')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n👋 Goodbye!')
        sys.exit(0)
    except Exception as e:
        print(f'\n❌ Error: {e}')
        sys.exit(1)
