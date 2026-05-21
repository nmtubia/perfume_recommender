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

# ----------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------

def compute_score(rating, votes):
    if rating is None or votes is None:
        return None
    return rating * math.log1p(votes)

# ----------------------------------------------------------------------------------
    
def get_perfumes(designer_url, designer_name):
    html = fetch(designer_url)
    soup = BeautifulSoup(html, "html.parser")

    elements = soup.select("a.prefumeHbox")
    
    perfumes = []

    for element in elements:
        name_tag = element.select_one('h3.tw-perfume-title')
        year_tag = element.select_one('span.tw-year-badge')
        gender_tag = element.select_one("span.text-pink-700, span.text-teal-700, span.text-blue-700")
        designer_tag = element.select_one('p.tw-perfume-designer')

        perfumes.append({
            'designer': designer_name,
            'perfume_name': name_tag.get_text(strip=True) if name_tag else None,
            'year': year_tag.get_text(strip=True) if year_tag else None,
            'gender': gender_tag.get_text(strip=True) if gender_tag else None,
            'url': urljoin(BASE, element.get("href"))
        })
    
    return perfumes

# ----------------------------------------------------------------------------------

def get_fragrance_details(perfume_url):
    html = fetch(perfume_url)
    soup = BeautifulSoup(html, "html.parser")

    perfume_details = []

     # -------------------------
    # 1. ACCORDS
    # -------------------------
    main_accords = [
    s.get_text(strip=True)
    for s in soup.select("span.truncate")
    if s.get_text(strip=True) != "Search perfumes, articles, designers..."]

     # -------------------------
    # 2. NOTES
    # -------------------------
    notes = {
        "top_notes": [],
        "middle_notes": [],
        "base_notes": []
    }

    elements = soup.select("div.pyramid-level-container")

    notes["top_notes"] = [
        n.get_text(strip=True)
        for n in elements[0].select("span.pyramid-note-label")
    ]

    notes["middle_notes"] = [
        n.get_text(strip=True)
        for n in elements[1].select("span.pyramid-note-label")
    ]

    notes["base_notes"] = [
        n.get_text(strip=True)
        for n in elements[2].select("span.pyramid-note-label")
    ]

    perfume_details.append({
        'main_accords' : main_accords,
        'notes': notes
    })
    return perfume_details

details = get_fragrance_details('https://www.fragrantica.com/perfume/d-Annam/Da-Lat-89237.html')
print(details)





