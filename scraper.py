import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import time
import math
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

BASE = 'https://www.fragrantica.com'

MAX_PER_DESIGNER = 10
REQUEST_DELAY = 2.5

def fetch(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url, wait_until="load", timeout=60000)

        # safe cookie handling
        try:
            page.locator("text=Accept").click(timeout=3000)
        except:
            pass

        page.wait_for_timeout(3000)

        # optional scroll (keep for now)
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(3000)

        html = page.content()

        browser.close()
        return html

        # print("=== HTML SNAPSHOT ===")
        # print(html[:1500])  # inspect what you're actually getting

def get_designers(designer_index_url):
    html = fetch(designer_index_url)
    soup = BeautifulSoup(html, "html.parser")

    elements = soup.select("div.h-full a[href^='/designers/']")

    designers = {}

    for a in elements:
        name = a.get_text(strip=True)
        href = a.get("href")

        if not href or not name:
            continue

        url = urljoin(BASE, href)

        designers[name] = url

    return designers
    
    #def get_perfumes(designer_name, designer_url):

url = "https://www.fragrantica.com/designers/"

designers = get_designers(url)

print(len(designers))
print(list(designers.items())[:10])






