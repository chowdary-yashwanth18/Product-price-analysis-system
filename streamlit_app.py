"""
DAE Market Intelligence — Interactive Streamlit Dashboard
==========================================================
Batch-4: Web Scraping and Product Price Analysis System
Technologies Demonstrated:
  - Streamlit (Interactive Reactive Web Framework)
  - Pandas & NumPy (Data Processing & Calculations)
  - SQLite3 (Relational Database Querying)
  - Seaborn & Matplotlib (Statistical Visualization Display)
  - Requests, BeautifulSoup, Selenium (Scraper Diagnostics)
"""

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os
import glob

# Set Streamlit page configuration
st.set_page_config(
    page_title="DAE Market Intelligence | Product Price Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_EXCEL = os.path.join(BASE_DIR, 'data', 'processed', 'DAE_Product_Data_Preprocessed.xlsx')
DATA_CSV = os.path.join(BASE_DIR, 'data', 'processed', 'DAE_Product_Data_Preprocessed.csv')
DB_PATH = os.path.join(BASE_DIR, 'data', 'database', 'products.db')
CHARTS_DIR = os.path.join(BASE_DIR, 'dashboard', 'charts')
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')

# Inject custom modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.8rem;
    }
    .kpi-card {
        background: linear-gradient(145deg, #12121a, #1a1a26);
        border: 1px solid #2a2a3e;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    .kpi-title {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.3rem;
    }
    .best-deal-badge {
        background-color: #065f46;
        color: #34d399;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load preprocessed product dataset."""
    if os.path.exists(DATA_EXCEL):
        df = pd.read_excel(DATA_EXCEL)
    elif os.path.exists(DATA_CSV):
        df = pd.read_csv(DATA_CSV)
    else:
        raw_files = glob.glob(os.path.join(RAW_DIR, '*.xlsx'))
        if raw_files:
            df = pd.read_excel(raw_files[0])
        else:
            return pd.DataFrame()
    return df


df_master = load_data()

# -------------------------------------------------------------
# SIDEBAR CONTROLS & FILTERS
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/lightning-bolt.png", width=50)
    st.title("DAE Analytics")
    st.caption("Batch-4 Project Review | Market Intelligence")
    st.markdown("---")

    st.subheader("Global Filters")
    if not df_master.empty:
        categories = ["All Categories"] + sorted(df_master['Category'].dropna().unique().tolist())
        sel_cat = st.selectbox("Product Category", categories)

        websites = sorted(df_master['Website'].dropna().unique().tolist())
        sel_websites = st.multiselect("Retailer Websites", websites, default=websites)

        min_price = float(df_master['Selling Price (₹)'].min())
        max_price = float(df_master['Selling Price (₹)'].max())
        price_range = st.slider("Price Range (₹)", min_value=min_price, max_value=max_price, value=(min_price, max_price), step=1000.0)

        search_query = st.text_input("Search Product", placeholder="e.g. iPhone, OLED TV...")
    else:
        sel_cat = "All Categories"
        sel_websites = []
        price_range = (0, 100000)
        search_query = ""

    st.markdown("---")
    st.markdown("### Technologies Stack")
    st.markdown("""
    - **Language:** Python 3.13
    - **Scraping:** Requests, BS4, Selenium
    - **Analytics:** Pandas, NumPy
    - **Visuals:** Matplotlib, Seaborn
    - **Storage:** SQLite3, CSV
    - **Dashboard:** Streamlit + HTML5
    """)


# -------------------------------------------------------------
# MAIN HEADER & OVERVIEW
# -------------------------------------------------------------
st.markdown('<div class="main-header">⚡ DAE Market Intelligence & Price Comparison Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Retailer Analytics comparing 2,000 product pricing records across Amazon, Flipkart, Croma, Reliance Digital, and Vijay Sales</div>', unsafe_allow_html=True)

if df_master.empty:
    st.error("No dataset available. Please ensure data preprocessing has been run.")
    st.stop()

# Filter dataset according to sidebar selections
df_filtered = df_master.copy()
if sel_cat != "All Categories":
    df_filtered = df_filtered[df_filtered['Category'] == sel_cat]
if sel_websites:
    df_filtered = df_filtered[df_filtered['Website'].isin(sel_websites)]
df_filtered = df_filtered[
    (df_filtered['Selling Price (₹)'] >= price_range[0]) &
    (df_filtered['Selling Price (₹)'] <= price_range[1])
]
if search_query:
    df_filtered = df_filtered[df_filtered['Product Name'].str.contains(search_query, case=False, na=False)]

# -------------------------------------------------------------
# TOP EXECUTIVE KPI CARDS
# -------------------------------------------------------------
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

total_records = len(df_filtered)
unique_prods = df_filtered['Product Name'].nunique()
avg_discount = df_filtered['Discount (%)'].mean() if not df_filtered.empty else 0
avg_price = df_filtered['Selling Price (₹)'].mean() if not df_filtered.empty else 0
lowest_price = df_filtered['Selling Price (₹)'].min() if not df_filtered.empty else 0

with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Listings Filtered</div>
        <div class="kpi-value">{total_records:,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Unique Products</div>
        <div class="kpi-value">{unique_prods}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Avg Market Discount</div>
        <div class="kpi-value">{avg_discount:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Price</div>
        <div class="kpi-value">₹{avg_price:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Lowest Offer Price</div>
        <div class="kpi-value">₹{lowest_price:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# INTERACTIVE APPLICATION TABS
# -------------------------------------------------------------
tab_compare, tab_charts, tab_sql, tab_scrapers, tab_data = st.tabs([
    "🔍 Product Price Comparator",
    "📊 Statistical Charts (Seaborn & Matplotlib)",
    "🗄️ SQLite Database Engine",
    "🕷️ Web Scrapers (Requests / BS4 / Selenium)",
    "📋 Data Explorer & Export"
])

# -------------------------------------------------------------
# TAB 1: PRODUCT PRICE COMPARATOR
# -------------------------------------------------------------
with tab_compare:
    st.subheader("Cross-Platform Product Price Comparator")
    st.caption("Select any product to compare real-time prices across all 5 e-commerce retailers")

    all_products = sorted(df_master['Product Name'].unique().tolist())
    selected_product = st.selectbox("Select Product to Compare", all_products)

    p_subset = df_master[df_master['Product Name'] == selected_product]
    if not p_subset.empty:
        site_agg = p_subset.groupby('Website').agg({
            'Selling Price (₹)': 'mean',
            'MRP (₹)': 'first',
            'Discount (%)': 'mean',
            'Rating': 'mean',
            'Review Count': 'max'
        }).reset_index().sort_values('Selling Price (₹)')

        mrp_val = site_agg['MRP (₹)'].iloc[0]
        cheapest_site = site_agg.iloc[0]['Website']
        cheapest_price = site_agg.iloc[0]['Selling Price (₹)']
        highest_price = site_agg.iloc[-1]['Selling Price (₹)']
        spread = highest_price - cheapest_price
        spread_pct = (spread / cheapest_price) * 100

        col_left, col_right = st.columns([1, 1.2])

        with col_left:
            st.markdown(f"### {selected_product}")
            st.write(f"**Original MRP:** ₹{mrp_val:,.0f}")
            st.success(f"🏆 **Best Deal Available:** ₹{cheapest_price:,.0f} at **{cheapest_site}**")
            st.info(f"💡 **Max Savings Across Stores:** ₹{spread:,.0f} ({spread_pct:.1f}% price difference)")

            st.write("#### Retailer Breakdown")
            for _, r in site_agg.iterrows():
                is_best = r['Website'] == cheapest_site
                badge = " 🥇 CHEAPEST" if is_best else ""
                st.write(f"- **{r['Website']}:** ₹{r['Selling Price (₹)']:,.0f} ({r['Discount (%)']:.1f}% off | ⭐ {r['Rating']:.1f}){badge}")

        with col_right:
            st.write("#### Price Comparison Bar Chart")
            chart_df = site_agg.set_index('Website')[['Selling Price (₹)']]
            st.bar_chart(chart_df)

# -------------------------------------------------------------
# TAB 2: STATISTICAL CHARTS (SEABORN & MATPLOTLIB)
# -------------------------------------------------------------
with tab_charts:
    st.subheader("Statistical Visualizations (Matplotlib & Seaborn Suite)")
    st.caption("Visualizing price distributions, kernel density estimations, category spreads, and linear regression")

    chart_options = {
        "Category Price Box Plot (IQR & Outliers)": "price_distribution_boxplot.png",
        "Rating vs Selling Price Regression Scatter": "rating_vs_price_scatter.png",
        "Category Price Density Violin Plot": "category_violin_plot.png",
        "Retailer Discount KDE Curves": "platform_discount_kde.png",
        "Retailer × Category Price Heatmap": "platform_price_heatmap.png",
        "Product Price Range Dumbbell Chart": "product_price_range.png",
        "Which Website Offers the Best Price?": "website_comparison.png",
        "4-Product Price Trends Over Time": "price_trends_multi.png"
    }

    sel_chart_name = st.selectbox("Select Visualized Chart", list(chart_options.keys()))
    chart_filename = chart_options[sel_chart_name]
    chart_filepath = os.path.join(CHARTS_DIR, chart_filename)

    if os.path.exists(chart_filepath):
        st.image(chart_filepath, caption=sel_chart_name, use_container_width=True)
    else:
        st.warning(f"Chart '{chart_filename}' is being generated. Run `py scripts/generate_seaborn_charts.py` to compile.")

# -------------------------------------------------------------
# TAB 3: SQLITE DATABASE ENGINE
# -------------------------------------------------------------
with tab_sql:
    st.subheader("SQLite Relational Database & Analytics Engine")
    st.caption(f"Database File: `{DB_PATH}`")

    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)

        preset_queries = {
            "1. Platform Price Competitiveness & Averages": """
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
            """,
            "2. Top 10 Cross-Platform Arbitrage Opportunities": """
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
            """,
            "3. Best Deal Leaderboard (Stores with Lowest Price)": """
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
        }

        sel_preset = st.selectbox("Select Preset Analytical SQL Query", list(preset_queries.keys()))
        sql_input = st.text_area("SQL Query Editor", preset_queries[sel_preset], height=180)

        if st.button("Execute SQL Query", type="primary"):
            try:
                res_df = pd.read_sql_query(sql_input, conn)
                st.success(f"Query returned {len(res_df)} rows.")
                st.dataframe(res_df, use_container_width=True)
            except Exception as e:
                st.error(f"SQL Error: {e}")

        conn.close()
    else:
        st.warning("SQLite database not found. Please run `py scripts/sqlite_pipeline.py` first.")

# -------------------------------------------------------------
# TAB 4: WEB SCRAPERS DIAGNOSTICS
# -------------------------------------------------------------
with tab_scrapers:
    st.subheader("Web Scraping Infrastructure")
    st.caption("Demonstrating dual-engine scraping: Requests + BeautifulSoup (Static HTML) and Selenium WebDriver (Dynamic DOM)")

    c_s1, c_s2 = st.columns(2)

    with c_s1:
        st.markdown("### 1. Requests + BeautifulSoup Module")
        st.write("""
        - **Target:** Static & REST e-commerce HTML pages.
        - **Method:** `requests.Session` with custom User-Agent headers, timeout handling, and `bs4.BeautifulSoup` CSS selector parsing.
        - **Script:** `scripts/scraper_requests_bs4.py`
        """)
        bs4_csv = os.path.join(RAW_DIR, 'scraped_requests_bs4.csv')
        if os.path.exists(bs4_csv):
            st.write("**Latest Scraped Records (BS4):**")
            st.dataframe(pd.read_csv(bs4_csv), use_container_width=True)
        else:
            st.info("Run `py scripts/scraper_requests_bs4.py` to view live output.")

    with c_s2:
        st.markdown("### 2. Selenium WebDriver Module")
        st.write("""
        - **Target:** Client-side JavaScript hydrated pages (React, Next.js).
        - **Method:** Headless Chrome WebDriver, scroll-down trigger for dynamic lazy-loading, explicit waits (`WebDriverWait`).
        - **Script:** `scripts/scraper_selenium.py`
        """)
        sel_csv = os.path.join(RAW_DIR, 'scraped_selenium.csv')
        if os.path.exists(sel_csv):
            st.write("**Latest Scraped Records (Selenium):**")
            st.dataframe(pd.read_csv(sel_csv), use_container_width=True)
        else:
            st.info("Run `py scripts/scraper_selenium.py` to view live output.")

# -------------------------------------------------------------
# TAB 5: DATA EXPLORER & EXPORT
# -------------------------------------------------------------
with tab_data:
    st.subheader("Cleaned Dataset Explorer")
    st.write(f"Displaying **{len(df_filtered)}** records matching active filters.")
    st.dataframe(df_filtered, use_container_width=True, height=450)

    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="DAE_Filtered_Product_Data.csv",
        mime="text/csv",
        type="primary"
    )

st.markdown("---")
st.markdown("<center style='color:#64748b;'>DAE Analytics — Batch-4 Team: Chowdary Yashwanth | Punnam Surya Sai | B. Meghana | N. Ramalakshmi</center>", unsafe_allow_html=True)
