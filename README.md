# DAE Project: Web Scraping & Multi-Platform Product Price Analysis

**Batch-4 | Data Analytics & Engineering (DAE) Project Review**

* **Team Members:**
  * 25B11CS195 : Chowdary Yashwanth
  * 25B11CS793 : Punnam Surya Sai
  * 25B11CS109 : B. Meghana
  * 25B11CS639 : N. Ramalakshmi

---

## 🚀 Technologies Used & Analytics Stack Mapping

The project strictly implements and demonstrates every technology specified in **Review Slide 7**:

| Technology | Role & Purpose | Implementation File / Artifact |
| :--- | :--- | :--- |
| **Python** | Main programming language for all backend & analytics pipelines | Python 3.13 Core Scripts |
| **Requests** | Fetch web pages with sessions, custom headers & timeout handling | [`scripts/scraper_requests_bs4.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/scripts/scraper_requests_bs4.py) |
| **BeautifulSoup** | Parse HTML DOM, CSS selector matching & structured record extraction | [`scripts/scraper_requests_bs4.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/scripts/scraper_requests_bs4.py) |
| **Selenium** | Dynamic browser automation, JS scrolling & lazy-loading element waits | [`scripts/scraper_selenium.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/scripts/scraper_selenium.py) |
| **Pandas** | Data cleaning, null handling, deduplication, aggregation & price comparison | [`scripts/preprocess_dataset.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/scripts/preprocess_dataset.py) |
| **NumPy** | Numerical operations, vector math, price difference and spread metrics | [`scripts/preprocess_dataset.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/scripts/preprocess_dataset.py) |
| **Matplotlib** | Scientific figure generation, dumbbell spreads, and time-series charts | [`scripts/preprocess_dataset.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/scripts/preprocess_dataset.py) |
| **Seaborn** | Advanced statistical charts (Box plots, Violin plots, Regplot, KDE, Heatmap) | [`scripts/generate_seaborn_charts.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/scripts/generate_seaborn_charts.py) |
| **CSV Storage** | Structured flat-file exports conforming to standardized schemas | [`data/processed/DAE_Product_Data_Preprocessed.csv`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/data/processed/DAE_Product_Data_Preprocessed.csv) |
| **SQLite3** | Normalized relational database (`products`, `websites`, `categories`, `price_records`) | [`data/database/products.db`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/data/database/products.db) & [`scripts/sqlite_pipeline.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/scripts/sqlite_pipeline.py) |
| **Streamlit** | Interactive multi-feature web dashboard for live exploration & SQL execution | [`streamlit_app.py`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/streamlit_app.py) |
| **Web Dashboard** | Premium interactive single-page analytics application (HTML5/CSS/JS) | [`dashboard/index.html`](file:///c:/Users/chowd/OneDrive/Desktop/DAE/dashboard/index.html) |

---

## 🏛️ Proposed System Architecture

```
┌─────────────────────────┐
│  User / Product Keyword │
└────────────┬────────────┘
             ▼
┌────────────────────────────────────────────────────────┐
│ Web Scraping: Requests + BS4 (Static) / Selenium (JS) │
└────────────┬───────────────────────────────────────────┘
             ▼
┌─────────────────────────┐
│ Raw Dataset (CSV/JSON)  │
└────────────┬────────────┘
             ▼
┌──────────────────────────────────────────────┐
│ Data Cleaning & Preprocessing (Pandas/NumPy) │
└────────────┬─────────────────────────────────┘
             ▼
┌──────────────────────────────────────────────────┐
│ Storage Pipeline: SQLite Relational DB & Clean CSV│
└────────────┬─────────────────────────────────────┘
             ▼
┌──────────────────────────────────────────────┐
│ Price Analysis: Cross-Platform Arbitrage/Spread│
└────────────┬─────────────────────────────────┘
             ▼
┌───────────────────────────────────────────────────┐
│ Visualization & Insights: Matplotlib/Seaborn/Streamlit│
└───────────────────────────────────────────────────┘
```

---

## 🛠️ Step-by-Step Execution Guide

### 1. Web Scraping Modules (Requests, BeautifulSoup, Selenium)
Run the Requests + BeautifulSoup static parser:
```bash
py scripts/scraper_requests_bs4.py
```
Run the dynamic browser scraper (Selenium WebDriver):
```bash
py scripts/scraper_selenium.py
```
*Outputs are saved to `data/raw/scraped_requests_bs4.csv` and `data/raw/scraped_selenium.csv`.*

---

### 2. Data Cleaning & Pipeline Preprocessing (Pandas & NumPy)
Inspect and clean the 2,000 product records:
```bash
py scripts/inspect_dataset.py
py scripts/preprocess_dataset.py
```
*Deduplicates, validates numerical price types, computes savings, and generates base Matplotlib figures.*

---

### 3. SQLite Relational Database & CSV Storage (SQLite3)
Build the relational SQLite database and execute analytical queries:
```bash
py scripts/sqlite_pipeline.py
```
*Creates normalized tables in `data/database/products.db`, runs competitive platform queries, and exports `DAE_Product_Data_Preprocessed.csv`.*

---

### 4. Advanced Statistical Visualizations (Seaborn & Matplotlib)
Generate publication-grade statistical charts:
```bash
py scripts/generate_seaborn_charts.py
```
*Produces 5 statistical graphics in `dashboard/charts/`:*
1. `price_distribution_boxplot.png` (Category IQR & Outlier Spread)
2. `rating_vs_price_scatter.png` (Linear Regression Trendline)
3. `category_violin_plot.png` (Multimodal Price Density)
4. `platform_discount_kde.png` (Retailer Discount KDE Curves)
5. `platform_price_heatmap.png` (Category × Retailer Annotated Heatmap)

---

### 5. Interactive Streamlit Dashboard
Launch the standalone Streamlit analytical dashboard:
```bash
py -m streamlit run streamlit_app.py
```
*Features interactive category filtering, live cross-platform price comparator, custom SQL query runner, and CSV exports.*

---

### 6. Interactive Web Dashboard (HTML5 / Vanilla CSS / Modern JS)
To view the full DAE Market Intelligence web dashboard:
```bash
cd dashboard
py -m http.server 8000
```
Then visit **`http://localhost:8000`** in your browser. Includes full Lightbox modal inspection for all 16 Matplotlib and Seaborn figures.

---

## 📊 Summary of Research Insights
* **Total Observations:** 2,000 scraped records across 5 retailers (Amazon, Flipkart, Croma, Reliance Digital, Vijay Sales).
* **Maximum Arbitrage Disparity:** **₹16,080** on the *LG 55-inch OLED TV* (Lowest: ₹1,08,000 vs Highest: ₹1,24,080).
* **Retailer Competitiveness Leaderboard:** Reliance Digital and Flipkart offer the lowest entry prices most frequently across consumer electronics.
