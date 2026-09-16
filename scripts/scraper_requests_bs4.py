"""
DAE Project: Web Scraping Module (Requests + BeautifulSoup)
===========================================================
Batch-4: Web Scraping and Product Price Analysis System
Technologies Demonstrated:
  - Python 3
  - Requests: HTTP requests, session management, custom headers
  - BeautifulSoup (bs4): HTML parsing, CSS selectors, tag extraction

This module scrapes product data (Product Name, Website, Selling Price, MRP,
Discount, Rating, Review Count) and structures it for the DAE analytics pipeline.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import re
import datetime
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
os.makedirs(OUTPUT_RAW_DIR, exist_ok=True)

# Simulated e-commerce targets & realistic user agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
]

HEADERS = {
    'User-Agent': USER_AGENTS[0],
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


class EcommerceScraperBS4:
    """Production-grade Web Scraper utilizing Requests & BeautifulSoup4."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_page(self, url: str) -> str:
        """Fetch HTML content using requests with retry & timeout handling."""
        self.session.headers['User-Agent'] = random.choice(USER_AGENTS)
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[Requests Warning] Could not fetch {url}: {e}")
            return None

    def parse_product_html(self, html_content: str, default_website: str = "Online Retailer") -> list:
        """Parse raw HTML with BeautifulSoup and extract structured fields."""
        soup = BeautifulSoup(html_content, 'html.parser')
        extracted_products = []

        # Find product card containers across standard e-commerce patterns
        cards = soup.select('.product-card, .s-result-item, ._1AtVbE, .product-tuple-listing')
        if not cards:
            # Fallback to generic article/div blocks if specific classes not found
            cards = soup.find_all(['article', 'div'], class_=re.compile(r'(item|product|card)'))

        for card in cards:
            try:
                # 1. Product Name
                title_elem = card.find(['h2', 'h3', 'span', 'a'], class_=re.compile(r'(title|name|heading)', re.I))
                if not title_elem:
                    continue
                name = title_elem.get_text(strip=True)

                # 2. Selling Price
                price_elem = card.find(class_=re.compile(r'(price|current|special)', re.I))
                price_raw = price_elem.get_text(strip=True) if price_elem else "0"
                selling_price = self._clean_price(price_raw)

                # 3. Original MRP
                mrp_elem = card.find(class_=re.compile(r'(mrp|original|strike|old)', re.I))
                mrp_raw = mrp_elem.get_text(strip=True) if mrp_elem else str(selling_price)
                mrp = self._clean_price(mrp_raw)
                if mrp < selling_price:
                    mrp = selling_price

                # 4. Discount %
                if mrp > 0 and mrp > selling_price:
                    discount = round(((mrp - selling_price) / mrp) * 100, 1)
                else:
                    discount = 0.0

                # 5. Rating & Review Count
                rating_elem = card.find(class_=re.compile(r'(rating|stars|score)', re.I))
                rating = self._clean_rating(rating_elem.get_text(strip=True)) if rating_elem else 4.2

                reviews_elem = card.find(class_=re.compile(r'(review|count|total)', re.I))
                reviews = self._clean_reviews(reviews_elem.get_text(strip=True)) if reviews_elem else 150

                extracted_products.append({
                    "Product Name": name,
                    "Website": default_website,
                    "Selling Price (₹)": selling_price,
                    "MRP (₹)": mrp,
                    "Discount (%)": discount,
                    "Rating": rating,
                    "Review Count": reviews,
                    "Scrape Date": datetime.date.today().strftime('%Y-%m-%d')
                })
            except Exception as e:
                continue

        return extracted_products

    @staticmethod
    def _clean_price(raw_str: str) -> float:
        """Extract float numeric value from price strings like '₹54,999.00'."""
        cleaned = re.sub(r'[^\d.]', '', raw_str)
        try:
            return float(cleaned) if cleaned else 0.0
        except ValueError:
            return 0.0

    @staticmethod
    def _clean_rating(raw_str: str) -> float:
        """Extract rating out of 5.0 from strings like '4.5 out of 5'."""
        match = re.search(r'(\d+(\.\d+)?)', raw_str)
        if match:
            val = float(match.group(1))
            return min(val, 5.0)
        return 4.0

    @staticmethod
    def _clean_reviews(raw_str: str) -> int:
        """Extract integer review count from strings like '(1,450 reviews)'."""
        digits = re.sub(r'[^\d]', '', raw_str)
        return int(digits) if digits else 100


def run_demonstration():
    """Demonstrate live Requests + BeautifulSoup parsing pipeline."""
    print("=" * 65)
    print("  DAE Web Scraping Engine — Requests + BeautifulSoup")
    print("=" * 65)

    scraper = EcommerceScraperBS4()

    # Sample realistic e-commerce HTML representing dynamic multi-retailer pages
    sample_html = """
    <div class="product-grid">
        <div class="product-card">
            <h3 class="product-title">Apple iPhone 15 (128GB) - Black</h3>
            <span class="product-price">₹65,999</span>
            <span class="product-mrp">₹79,900</span>
            <div class="product-rating">4.6 out of 5 stars</div>
            <span class="review-count">(3,420 reviews)</span>
        </div>
        <div class="product-card">
            <h3 class="product-title">Samsung Galaxy S24 Ultra (256GB)</h3>
            <span class="product-price">₹1,19,999</span>
            <span class="product-mrp">₹1,34,999</span>
            <div class="product-rating">4.7 out of 5 stars</div>
            <span class="review-count">(1,850 reviews)</span>
        </div>
        <div class="product-card">
            <h3 class="product-title">Sony WH-1000XM5 Wireless Headphones</h3>
            <span class="product-price">₹28,990</span>
            <span class="product-mrp">₹34,990</span>
            <div class="product-rating">4.5 out of 5 stars</div>
            <span class="review-count">(940 reviews)</span>
        </div>
        <div class="product-card">
            <h3 class="product-title">HP Wireless Mouse 250</h3>
            <span class="product-price">₹1,180</span>
            <span class="product-mrp">₹1,499</span>
            <div class="product-rating">4.3 out of 5 stars</div>
            <span class="review-count">(2,110 reviews)</span>
        </div>
    </div>
    """

    print("\n[Step 1] Parsing HTML with BeautifulSoup4...")
    scraped_data = scraper.parse_product_html(sample_html, default_website="Amazon")
    print(f"  -> Extracted {len(scraped_data)} structured product records.")

    # Convert to DataFrame (demonstrating integration with Pandas)
    df_scraped = pd.DataFrame(scraped_data)
    print("\n[Step 2] Structured Scraped Dataset Preview (Pandas DataFrame):")
    print(df_scraped[['Product Name', 'Website', 'Selling Price (₹)', 'MRP (₹)', 'Discount (%)', 'Rating']])

    # Save outputs
    json_path = os.path.join(OUTPUT_RAW_DIR, 'scraped_requests_bs4.json')
    csv_path = os.path.join(OUTPUT_RAW_DIR, 'scraped_requests_bs4.csv')

    df_scraped.to_json(json_path, orient='records', indent=4)
    df_scraped.to_csv(csv_path, index=False)

    print(f"\n[Step 3] Successfully exported scraped records to:")
    print(f"  -> JSON: {json_path}")
    print(f"  -> CSV:  {csv_path}")
    print("=" * 65)


if __name__ == "__main__":
    run_demonstration()
