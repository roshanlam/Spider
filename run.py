#!/usr/bin/env python3
"""
Simple script to run the Spider crawler with Web Scraper Plugin.

Usage:
    python run.py
"""

import sys
import subprocess

if __name__ == "__main__":
    # Run the spider main module
    sys.exit(subprocess.call([sys.executable, "-m", "spider.main"]))
