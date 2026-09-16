"""
DAE Project: SQLite Relational Database & Storage Pipeline
==========================================================
Batch-4: Web Scraping and Product Price Analysis System
Technologies Demonstrated:
  - Python 3
  - SQLite3 (Relational Database Engine)
  - CSV Storage & Export
  - SQL Aggregations, Joins, Window Queries

Creates a normalized SQLite database (data/database/products.db), populates it
from scraped/preprocessed e-commerce datasets, executes analytical queries,
and exports clean CSV records for external reporting.
"""

import sqlite3
import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'data', 'database')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, 'products.db')
EXCEL_PATH = os.path.join(PROCESSED_DIR, 'DAE_Product_Data_Preprocessed.xlsx')
RAW_EXCEL_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'DAE Product Price Web Scraping Dataset 2000 Records final.xlsx')
CSV_EXPORT_PATH = os.path.join(PROCESSED_DIR, 'DAE_Product_Data_Preprocessed.csv')


def create_schema(conn: sqlite3.Connection):
    """Create normalized relational tables for DAE product intelligence."""
    cursor = conn.cursor()

    cursor.executescript("""
    PRAGMA foreign_keys = ON;

    DROP TABLE IF EXISTS price_records;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS websites;

    -- 1. Websites lookup table
    CREATE TABLE websites (
        website_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        platform_type TEXT DEFAULT 'E-Commerce Marketplace'
    );

    -- 2. Categories lookup table
    CREATE TABLE categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    );

    -- 3. Products table
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT UNIQUE NOT NULL,
        category_id INTEGER,
        mrp REAL NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );

    -- 4. Price Records (time-series and multi-store scrapes)
    CREATE TABLE price_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        website_id INTEGER NOT NULL,
        selling_price REAL NOT NULL,
        mrp REAL NOT NULL,
        discount REAL,
        rating REAL,
        review_count INTEGER,
        savings REAL,
        scrape_date TEXT,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (website_id) REFERENCES websites(website_id)
    );

    -- Create indexes for ultra-fast query execution
    CREATE INDEX idx_price_product ON price_records(product_id);
    CREATE INDEX idx_price_website ON price_records(website_id);
    CREATE INDEX idx_price_selling ON price_records(selling_price);
    """)
    conn.commit()
    print("  -> Created normalized SQLite relational schema.")


def populate_database(conn: sqlite3.Connection, df: pd.DataFrame):
    """Normalize and insert dataset records into SQLite tables."""
    cursor = conn.cursor()

    # 1. Insert Websites
    websites = sorted(df['Website'].dropna().unique().tolist())
    cursor.executemany("INSERT INTO websites (name) VALUES (?)", [(w,) for w in websites])
    conn.commit()

    website_map = {row[1]: row[0] for row in cursor.execute("SELECT website_id, name FROM websites").fetchall()}

    # 2. Insert Categories
    categories = sorted(df['Category'].dropna().unique().tolist())
    cursor.executemany("INSERT INTO categories (category_name) VALUES (?)", [(c,) for c in categories])
    conn.commit()

    category_map = {row[1]: row[0] for row in cursor.execute("SELECT category_id, category_name FROM categories").fetchall()}

    # 3. Insert Products
    prod_df = df.groupby('Product Name').agg({
        'Category': 'first',
        'MRP (₹)': 'first'
    }).reset_index()

    product_inserts = [
        (row['Product Name'], category_map.get(row['Category']), float(row['MRP (₹)']))
        for _, row in prod_df.iterrows()
    ]
    cursor.executemany("INSERT INTO products (product_name, category_id, mrp) VALUES (?, ?, ?)", product_inserts)
    conn.commit()

    product_map = {row[1]: row[0] for row in cursor.execute("SELECT product_id, product_name FROM products").fetchall()}

    # 4. Insert Price Records
    record_inserts = []
    for _, row in df.iterrows():
        p_id = product_map.get(row['Product Name'])
        w_id = website_map.get(row['Website'])
        if p_id and w_id:
            selling = float(row.get('Selling Price (₹)', 0))
            mrp = float(row.get('MRP (₹)', selling))
            disc = float(row.get('Discount (%)', 0))
            rating = float(row.get('Rating', 0))
            reviews = int(row.get('Review Count', 0))
            savings = mrp - selling
            s_date = str(row.get('Scrape Date', ''))
            record_inserts.append((p_id, w_id, selling, mrp, disc, rating, reviews, savings, s_date))

    cursor.executemany("""
    INSERT INTO price_records 
    (product_id, website_id, selling_price, mrp, discount, rating, review_count, savings, scrape_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, record_inserts)
    conn.commit()

    print(f"  -> Successfully inserted {len(websites)} websites, {len(categories)} categories, "
          f"{len(product_inserts)} products, and {len(record_inserts)} price records.")


def run_analytical_queries(conn: sqlite3.Connection) -> dict:
    """Execute SQL analytical queries demonstrating relational data analytics."""
    print("\n[Step 3] Executing Analytical SQL Queries...")
    results = {}

    # Query 1: Platform Price Competitiveness (Average price & discount per website)
    q1 = """
    SELECT 
        w.name AS Website,
        COUNT(pr.record_id) AS TotalListings,
        ROUND(AVG(pr.selling_price), 2) AS AvgSellingPrice,
        ROUND(AVG(pr.discount), 2) AS AvgDiscountPercent,
        ROUND(AVG(pr.rating), 2) AS AvgRating
    FROM websites w
    JOIN price_records pr ON w.website_id = pr.website_id
    GROUP BY w.website_id, w.name
    ORDER BY AvgSellingPrice ASC;
    """
    df_q1 = pd.read_sql_query(q1, conn)
    print("\n--- 1. Platform Competitiveness (SQL Query) ---")
    print(df_q1.to_string(index=False))
    results["platform_competitiveness"] = df_q1.to_dict(orient='records')

    # Query 2: Cross-Platform Price Arbitrage & Spread (Min vs Max per product)
    q2 = """
    SELECT 
        p.product_name AS Product,
        c.category_name AS Category,
        p.mrp AS MRP,
        MIN(pr.selling_price) AS LowestPrice,
        MAX(pr.selling_price) AS HighestPrice,
        ROUND(MAX(pr.selling_price) - MIN(pr.selling_price), 2) AS PriceDifference,
        ROUND(((MAX(pr.selling_price) - MIN(pr.selling_price)) / MIN(pr.selling_price)) * 100, 2) AS ArbitragePercent
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    JOIN price_records pr ON p.product_id = pr.product_id
    GROUP BY p.product_id, p.product_name, c.category_name, p.mrp
    ORDER BY PriceDifference DESC
    LIMIT 10;
    """
    df_q2 = pd.read_sql_query(q2, conn)
    print("\n--- 2. Top 10 Price Arbitrage Opportunities across Websites ---")
    print(df_q2.to_string(index=False))
    results["top_arbitrage_products"] = df_q2.to_dict(orient='records')

    # Query 3: Best Deal Store (Website with lowest price for each product)
    q3 = """
    WITH MinPrices AS (
        SELECT product_id, MIN(selling_price) AS min_price
        FROM price_records
        GROUP BY product_id
    )
    SELECT 
        w.name AS Website,
        COUNT(DISTINCT pr.product_id) AS CheapestProductsCount
    FROM price_records pr
    JOIN MinPrices mp ON pr.product_id = mp.product_id AND pr.selling_price = mp.min_price
    JOIN websites w ON pr.website_id = w.website_id
    GROUP BY w.name
    ORDER BY CheapestProductsCount DESC;
    """
    df_q3 = pd.read_sql_query(q3, conn)
    print("\n--- 3. Best Deal Leaderboard: Which Store Offers Lowest Price Most Often? ---")
    print(df_q3.to_string(index=False))
    results["cheapest_store_leaderboard"] = df_q3.to_dict(orient='records')

    return results


def main():
    print("=" * 65)
    print("  DAE SQLite Database & Storage Engine")
    print("=" * 65)

    # 1. Load data
    target_excel = EXCEL_PATH if os.path.exists(EXCEL_PATH) else RAW_EXCEL_PATH
    print(f"\n[Step 1] Loading data from: {target_excel}")
    df = pd.read_excel(target_excel)

    # 2. Export clean CSV (fulfilling CSV storage requirement)
    df.to_csv(CSV_EXPORT_PATH, index=False)
    print(f"  -> Exported clean CSV to: {CSV_EXPORT_PATH}")

    # 3. Initialize SQLite
    print(f"\n[Step 2] Initializing SQLite database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    try:
        create_schema(conn)
        populate_database(conn, df)
        query_results = run_analytical_queries(conn)

        # Save query results to report
        report_path = os.path.join(REPORTS_DIR, 'sqlite_analytics_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(query_results, f, indent=4)
        print(f"\n[Step 4] Saved SQL analytics summary to: {report_path}")

    finally:
        conn.close()

    print("\n" + "=" * 65)
    print("  SQLite & CSV Pipeline successfully executed!")
    print("=" * 65)


if __name__ == "__main__":
    main()
