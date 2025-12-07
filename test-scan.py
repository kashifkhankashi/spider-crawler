#!/usr/bin/env python3
"""Test script to scan a website and show detailed errors"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.crawler.spider import WebsiteCrawler

async def test_scan():
    url = "https://longhorn-menu.us"
    print(f"Testing scan for: {url}")
    print("=" * 60)
    
    try:
        crawler = WebsiteCrawler(max_pages=5, include_external=False)
        results = await crawler.crawl(url)
        
        print(f"\n[SUCCESS] Scan completed successfully!")
        print(f"Pages found: {len(results.get('pages', []))}")
        print(f"Total links: {len(results.get('links', []))}")
        print(f"Total images: {len(results.get('images', []))}")
        
        if results.get('pages'):
            print("\nFirst page:")
            first_page = results['pages'][0]
            print(f"  URL: {first_page.get('url')}")
            print(f"  Title: {first_page.get('title', 'N/A')[:50]}")
            print(f"  Status: {first_page.get('status_code')}")
            print(f"  Word count: {first_page.get('word_count', 0)}")
        
        return results
        
    except Exception as e:
        print(f"\n[ERROR] ERROR occurred:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"Error repr: {repr(e)}")
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())
        raise

if __name__ == "__main__":
    try:
        results = asyncio.run(test_scan())
        print("\n" + "=" * 60)
        print("Test completed!")
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"Test failed with: {type(e).__name__}: {str(e)}")
        sys.exit(1)

