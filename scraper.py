import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import time
import math
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.62 Safari/537.36'
}


BASE = 'https://www.fragrantica.com'

MAX_PER_DESIGNER = 10
REQUEST_DELAY = 2.5

def get_designers(designer_index_url):
    response = requests.get(designer_index_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    elements = soup.find_all('div', class_="designerlist cell small-6 large-4")

    designers = {}

    for element in elements:
        

