"""
Test script for Web Scraper Plugin

This script verifies that the WebScraperPlugin is working correctly.
Run this after you've scraped some data to verify everything is functioning.
"""

import json
import sys
from typing import Dict, Any


def test_database_connection():
    """Test 1: Verify database connection"""
    print("\n" + "="*60)
    print("TEST 1: Database Connection")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import ScraperDataQuery
        query = ScraperDataQuery()

        # Try a simple query
        stats = query.get_page_statistics()

        print("✅ Database connection successful")
        print(f"   Total pages in database: {stats.get('total_pages', 0)}")
        return True

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure PostgreSQL is running and config.yaml is correct")
        return False


def test_plugin_installation():
    """Test 2: Verify plugin files exist"""
    print("\n" + "="*60)
    print("TEST 2: Plugin Installation")
    print("="*60)

    try:
        from spider.plugins.web_scraper_plugin import WebScraperPlugin
        from spider.plugins.scraper_utils import ScraperDataQuery

        print("✅ WebScraperPlugin imported successfully")
        print("✅ ScraperDataQuery imported successfully")

        # Try to instantiate
        plugin = WebScraperPlugin()
        print("✅ Plugin instantiation successful")

        return True

    except ImportError as e:
        print(f"❌ Plugin import failed: {e}")
        print("   Make sure the plugin files are in the correct location")
        return False


def test_data_extraction():
    """Test 3: Verify data was extracted"""
    print("\n" + "="*60)
    print("TEST 3: Data Extraction")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import ScraperDataQuery

        query = ScraperDataQuery()
        pages = query.get_all_pages(limit=1)

        if not pages:
            print("⚠️  No data found in database")
            print("   Run the crawler first to scrape some pages")
            return False

        page = pages[0]
        print("✅ Data extraction verified")
        print(f"   Sample page: {page['url']}")
        print(f"   Title: {page['title']}")
        print(f"   Word count: {page['word_count']}")

        return True

    except Exception as e:
        print(f"❌ Data extraction test failed: {e}")
        return False


def test_metadata_extraction():
    """Test 4: Verify metadata fields"""
    print("\n" + "="*60)
    print("TEST 4: Metadata Extraction")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import ScraperDataQuery

        query = ScraperDataQuery()
        pages = query.get_all_pages(limit=1)

        if not pages:
            print("⚠️  No data to test")
            return False

        page = pages[0]

        # Check key fields
        fields = {
            'url': page.get('url'),
            'title': page.get('title'),
            'description': page.get('description'),
            'language': page.get('language'),
            'word_count': page.get('word_count'),
        }

        print("Metadata fields:")
        for field, value in fields.items():
            status = "✅" if value is not None else "⚠️ "
            print(f"   {status} {field}: {value}")

        return True

    except Exception as e:
        print(f"❌ Metadata test failed: {e}")
        return False


def test_links_extraction():
    """Test 5: Verify links extraction"""
    print("\n" + "="*60)
    print("TEST 5: Links Extraction")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import ScraperDataQuery

        query = ScraperDataQuery()
        pages = query.get_all_pages(limit=1)

        if not pages:
            print("⚠️  No data to test")
            return False

        page = pages[0]
        links = json.loads(page['links'])

        print(f"✅ Links extracted successfully")
        print(f"   Total links: {links['count']}")
        print(f"   Internal links: {len(links['internal'])}")
        print(f"   External links: {len(links['external'])}")

        if links['all']:
            sample = links['all'][0]
            print(f"   Sample link: {sample['url']}")
            print(f"   Sample text: {sample['text']}")

        return True

    except Exception as e:
        print(f"❌ Links extraction test failed: {e}")
        return False


def test_images_extraction():
    """Test 6: Verify images extraction"""
    print("\n" + "="*60)
    print("TEST 6: Images Extraction")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import ScraperDataQuery

        query = ScraperDataQuery()
        pages = query.get_all_pages(limit=1)

        if not pages:
            print("⚠️  No data to test")
            return False

        page = pages[0]
        images = json.loads(page['images'])

        print(f"✅ Images extracted successfully")
        print(f"   Total images: {len(images)}")

        if images:
            sample = images[0]
            print(f"   Sample image: {sample['src']}")
            print(f"   Alt text: {sample['alt'] or '(none)'}")

        return True

    except Exception as e:
        print(f"❌ Images extraction test failed: {e}")
        return False


def test_headings_structure():
    """Test 7: Verify headings extraction"""
    print("\n" + "="*60)
    print("TEST 7: Headings Structure")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import ScraperDataQuery

        query = ScraperDataQuery()
        pages = query.get_all_pages(limit=1)

        if not pages:
            print("⚠️  No data to test")
            return False

        page = pages[0]
        headings = json.loads(page['headings'])

        print(f"✅ Headings extracted successfully")
        for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            count = len(headings.get(level, []))
            if count > 0:
                print(f"   {level.upper()}: {count} heading(s)")

        return True

    except Exception as e:
        print(f"❌ Headings test failed: {e}")
        return False


def test_query_functions():
    """Test 8: Verify query utility functions"""
    print("\n" + "="*60)
    print("TEST 8: Query Utility Functions")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import (
            ScraperDataQuery,
            get_page_data,
            get_statistics
        )

        query = ScraperDataQuery()

        # Test get_all_pages
        pages = query.get_all_pages(limit=5)
        print(f"✅ get_all_pages(): {len(pages)} pages returned")

        # Test get_page_statistics
        stats = get_statistics()
        print(f"✅ get_statistics(): {stats.get('total_pages', 0)} total pages")

        # Test search
        if pages:
            url = pages[0]['url']
            page_data = get_page_data(url)
            print(f"✅ get_page_data(): Retrieved {url}")

        return True

    except Exception as e:
        print(f"❌ Query functions test failed: {e}")
        return False


def test_structured_data():
    """Test 9: Verify structured data extraction"""
    print("\n" + "="*60)
    print("TEST 9: Structured Data")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import ScraperDataQuery

        query = ScraperDataQuery()
        pages = query.get_all_pages(limit=10)

        if not pages:
            print("⚠️  No data to test")
            return False

        pages_with_structured = 0
        for page in pages:
            structured = json.loads(page['structured_data'])
            if structured:
                pages_with_structured += 1

        print(f"✅ Structured data check complete")
        print(f"   Pages with JSON-LD: {pages_with_structured}/{len(pages)}")

        return True

    except Exception as e:
        print(f"❌ Structured data test failed: {e}")
        return False


def test_forms_detection():
    """Test 10: Verify forms detection"""
    print("\n" + "="*60)
    print("TEST 10: Forms Detection")
    print("="*60)

    try:
        from spider.plugins.scraper_utils import ScraperDataQuery

        query = ScraperDataQuery()
        pages_with_forms = query.get_pages_with_forms()

        print(f"✅ Forms detection working")
        print(f"   Pages with forms: {len(pages_with_forms)}")

        if pages_with_forms:
            sample = pages_with_forms[0]
            forms = json.loads(sample['forms'])
            print(f"   Sample page: {sample['url']}")
            print(f"   Forms on page: {len(forms)}")

        return True

    except Exception as e:
        print(f"❌ Forms detection test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*60)
    print("WEB SCRAPER PLUGIN TEST SUITE")
    print("="*60)

    tests = [
        test_plugin_installation,
        test_database_connection,
        test_data_extraction,
        test_metadata_extraction,
        test_links_extraction,
        test_images_extraction,
        test_headings_structure,
        test_query_functions,
        test_structured_data,
        test_forms_detection,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append(False)

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"\nTests passed: {passed}/{total} ({percentage:.0f}%)")

    if passed == total:
        print("\n🎉 All tests passed! The plugin is working correctly.")
        return 0
    elif passed > 0:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return 1
    else:
        print("\n❌ All tests failed. Check your installation and configuration.")
        return 2


def main():
    """Main entry point"""
    try:
        exit_code = run_all_tests()

        print("\n" + "="*60)
        if exit_code == 0:
            print("✅ PLUGIN IS READY TO USE")
            print("\nNext steps:")
            print("1. Run the crawler: poetry run python src/spider/main.py")
            print("2. Query your data: see examples/web_scraper_example.py")
            print("3. Read docs: WEB_SCRAPER_PLUGIN.md")
        elif exit_code == 1:
            print("⚠️  PARTIAL SUCCESS")
            print("\nSome features may not be working correctly.")
            print("Review the failed tests and check your configuration.")
        else:
            print("❌ SETUP INCOMPLETE")
            print("\nThe plugin is not properly installed or configured.")
            print("Check the installation instructions in QUICKSTART_WEB_SCRAPER.md")

        print("="*60 + "\n")

        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
