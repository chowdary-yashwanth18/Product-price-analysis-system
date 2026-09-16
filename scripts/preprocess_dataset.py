"""
DAE Product Price Web Scraping - Data Cleaning & Visualization Pipeline
========================================================================
Generates charts that highlight ACTUAL variations in the dataset:
- Price ranges vary enormously (₹1,180 to ₹124,080)
- 20 unique products across 7 categories and 5 websites
- Ratings & discounts are uniformly distributed (same per product)
  → So we focus charts on price comparisons, website savings, and trends
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import json
import os

# ============================================================
# CONFIGURATION
# ============================================================
BASE_DIR = 'c:/Users/chowd/OneDrive/Desktop/DAE'
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'raw', 'DAE Product Price Web Scraping Dataset 2000 Records final.xlsx')
OUTPUT_DIR = os.path.join(BASE_DIR, 'dashboard')
CHARTS_DIR = os.path.join(OUTPUT_DIR, 'charts')
REPORT_FILE = os.path.join(BASE_DIR, 'reports', 'cleaning_report.json')

os.makedirs(CHARTS_DIR, exist_ok=True)

# Global chart style
plt.rcParams.update({
    'figure.facecolor': '#0a0a0f',
    'axes.facecolor': '#12121a',
    'axes.edgecolor': '#2a2a3a',
    'axes.labelcolor': '#c8d0db',
    'text.color': '#f8fafc',
    'xtick.color': '#94a3b8',
    'ytick.color': '#94a3b8',
    'grid.color': '#1e1e2e',
    'grid.alpha': 0.6,
    'font.family': 'sans-serif',
    'font.size': 11,
    'figure.dpi': 150,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.3,
})

report = []

# ============================================================
# STEP 1: LOAD DATA
# ============================================================
print("=" * 60)
print("  DAE Data Cleaning & Visualization Pipeline")
print("=" * 60)

print("\n[1/5] Loading dataset...")
df = pd.read_excel(INPUT_FILE)
report.append(f"Step 1 - Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns.")
print(f"  -> Loaded {df.shape[0]} rows and {df.shape[1]} columns.")

# ============================================================
# STEP 2: DATA CLEANING WITH PANDAS
# ============================================================
print("\n[2/5] Cleaning data with Pandas...")

# 2a. Null values
null_counts = df.isnull().sum()
total_nulls = null_counts.sum()
if total_nulls > 0:
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    report.append(f"Step 2a - Null values: Found {total_nulls}. Dropped rows. Remaining: {df.shape[0]}.")
else:
    report.append("Step 2a - Null values: None found. No action needed.")
    print(f"  -> No null values found.")

# 2b. Duplicates
dup_count = df.duplicated().sum()
if dup_count > 0:
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    report.append(f"Step 2b - Duplicates: Removed {dup_count}. Remaining: {df.shape[0]}.")
else:
    report.append("Step 2b - Duplicates: None found. No action needed.")
    print(f"  -> No duplicate records found.")

# 2c. Strip whitespace
str_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
for col in str_cols:
    df[col] = df[col].astype(str).str.strip()
report.append(f"Step 2c - Stripped whitespace from {len(str_cols)} text columns.")
print(f"  -> Stripped whitespace from: {str_cols}")

# 2d. Fix data types
if 'Scrape Date' in df.columns:
    df['Scrape Date'] = pd.to_datetime(df['Scrape Date'], errors='coerce')
    df['Scrape Date'] = df['Scrape Date'].dt.strftime('%Y-%m-%d')
    report.append("Step 2d - Converted 'Scrape Date' to YYYY-MM-DD.")
    print("  -> Converted 'Scrape Date' to YYYY-MM-DD.")

numeric_cols = ['MRP (₹)', 'Selling Price (₹)', 'Discount (%)', 'Rating', 'Review Count']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
report.append(f"Step 2d - Ensured numeric types for: {numeric_cols}")

# 2e. Post-coercion cleanup
post_nulls = df.isnull().sum().sum()
if post_nulls > 0:
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    report.append(f"Step 2e - Removed {post_nulls} NaN rows after type coercion.")

# Add computed column: Savings
df['Savings (₹)'] = df['MRP (₹)'] - df['Selling Price (₹)']

report.append(f"Cleaning complete. Final: {df.shape[0]} rows, {df.shape[1]} columns.")
print(f"  -> Cleaning complete. Final: {df.shape[0]} rows, {df.shape[1]} columns.")

# ============================================================
# STEP 3: COMPUTE ANALYTICS
# ============================================================
print("\n[3/5] Computing analytics...")

product_agg = df.groupby('Product Name').agg({
    'Selling Price (₹)': ['min', 'max', 'mean'],
    'MRP (₹)': 'first',
    'Discount (%)': 'mean',
    'Rating': 'mean',
    'Review Count': 'max',
    'Category': 'first',
    'Savings (₹)': 'mean'
}).reset_index()
product_agg.columns = ['Product Name', 'Best Price', 'Worst Price', 'Avg Price', 'MRP',
                         'Avg Discount', 'Avg Rating', 'Max Reviews', 'Category', 'Avg Savings']

website_product = df.groupby(['Website', 'Product Name']).agg({
    'Selling Price (₹)': 'mean'
}).reset_index()

print("  -> Aggregations complete.")

# ============================================================
# STEP 4: GENERATE MATPLOTLIB CHARTS
# ============================================================
print("\n[4/5] Generating Matplotlib charts...")

# COLOR PALETTES
COLORS_PRODUCTS = ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b', '#8b5cf6',
                   '#06b6d4', '#f43f5e', '#10b981', '#e879f9', '#fb923c',
                   '#2dd4bf', '#818cf8', '#a78bfa', '#fbbf24', '#34d399',
                   '#f472b6', '#22d3ee', '#c084fc', '#fb7185', '#4ade80']

COLORS_WEBSITES = ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b', '#8b5cf6']

# --- CHART 1: Product Price Range (Min to Max) - Dumbbell/Range Chart ---
prod_sorted = product_agg.sort_values('Avg Price', ascending=True)
fig, ax = plt.subplots(figsize=(14, 8))
y_pos = range(len(prod_sorted))

for i, (_, row) in enumerate(prod_sorted.iterrows()):
    ax.plot([row['Best Price'], row['Worst Price']], [i, i], 
            color='#334155', linewidth=6, solid_capstyle='round', zorder=1)
    ax.scatter(row['Best Price'], i, color='#10b981', s=100, zorder=3, edgecolors='#0a0a0f', linewidths=1.5)
    ax.scatter(row['Worst Price'], i, color='#ef4444', s=100, zorder=3, edgecolors='#0a0a0f', linewidths=1.5)
    ax.scatter(row['Avg Price'], i, color='#6366f1', s=80, zorder=4, marker='D', edgecolors='#0a0a0f', linewidths=1)

ax.set_yticks(list(y_pos))
ax.set_yticklabels(prod_sorted['Product Name'], fontsize=10)
ax.set_xlabel('Selling Price (₹)', fontsize=13)
ax.set_title('Product Price Range Across All Websites', fontsize=18, fontweight='bold', pad=20)
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('₹{x:,.0f}'))
ax.legend(['Range', 'Best Price', 'Worst Price', 'Avg Price'], loc='lower right',
          framealpha=0.8, facecolor='#1e1e2e', edgecolor='#2a2a3a', fontsize=10)
ax.grid(True, axis='x', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'product_price_range.png'))
plt.close()
print("  -> Chart 1: Product Price Range (product_price_range.png)")

# --- CHART 2: Website Price Comparison per Product (Grouped Bar) ---
# Pick the top 6 most expensive products for readability
top_products = product_agg.nlargest(6, 'Avg Price')['Product Name'].tolist()
wp_subset = website_product[website_product['Product Name'].isin(top_products)]
pivot = wp_subset.pivot(index='Product Name', columns='Website', values='Selling Price (₹)')
pivot = pivot.reindex(top_products)

fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(pivot))
width = 0.15
websites = pivot.columns.tolist()

for i, website in enumerate(websites):
    offset = (i - len(websites)/2 + 0.5) * width
    bars = ax.bar(x + offset, pivot[website], width, label=website, 
                  color=COLORS_WEBSITES[i % len(COLORS_WEBSITES)], edgecolor='none', zorder=3)

ax.set_xlabel('Product', fontsize=12)
ax.set_ylabel('Avg Selling Price (₹)', fontsize=12)
ax.set_title('Which Website Offers the Best Price? (Top 6 Products)', fontsize=16, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels([p[:20] for p in top_products], fontsize=9, rotation=15, ha='right')
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('₹{x:,.0f}'))
ax.legend(loc='upper right', framealpha=0.8, facecolor='#1e1e2e', edgecolor='#2a2a3a')
ax.grid(True, axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'website_comparison.png'))
plt.close()
print("  -> Chart 2: Website Price Comparison (website_comparison.png)")

# --- CHART 3: Price Trend Over Time for 4 Different Products ---
selected_products = ['Apple iPhone 15', 'HP Wireless Mouse 250', 'LG 55-inch OLED TV', 'Sony WH-1000XM5']
trend_colors = ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b']

fig, ax = plt.subplots(figsize=(14, 6))
for product, color in zip(selected_products, trend_colors):
    pdata = df[df['Product Name'] == product].groupby('Scrape Date')['Selling Price (₹)'].mean().reset_index()
    pdata = pdata.sort_values('Scrape Date')
    ax.plot(range(len(pdata)), pdata['Selling Price (₹)'], color=color, linewidth=2.5, 
            marker='o', markersize=3, label=product)

ax.set_xlabel('Time Period (Weekly Scrapes)', fontsize=12)
ax.set_ylabel('Avg Selling Price (₹)', fontsize=12)
ax.set_title('Price Trend Comparison: 4 Products Over Time', fontsize=16, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('₹{x:,.0f}'))
ax.legend(loc='upper right', framealpha=0.8, facecolor='#1e1e2e', edgecolor='#2a2a3a')
ax.grid(True, axis='y', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'price_trends_multi.png'))
plt.close()
print("  -> Chart 3: Multi-Product Price Trends (price_trends_multi.png)")

# --- CHART 4: Category-wise Avg Selling Price (Pie/Donut) ---
cat_price = df.groupby('Category')['Selling Price (₹)'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    cat_price, labels=cat_price.index, autopct='₹%1.0f',
    colors=COLORS_PRODUCTS[:len(cat_price)],
    pctdistance=0.75, startangle=140,
    wedgeprops=dict(width=0.45, edgecolor='#0a0a0f', linewidth=2)
)
for t in texts: t.set_fontsize(11); t.set_color('#f8fafc')
for t in autotexts: t.set_fontsize(9); t.set_color('#f8fafc'); t.set_fontweight('bold')
ax.set_title('Avg Selling Price by Category', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'category_avg_price.png'))
plt.close()
print("  -> Chart 4: Category Avg Price Donut (category_avg_price.png)")

# --- CHART 5: Savings Per Product (MRP vs Selling Price) ---
prod_savings = product_agg.sort_values('Avg Savings', ascending=True)
fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.barh(prod_savings['Product Name'], prod_savings['Avg Savings'], 
               color=COLORS_PRODUCTS[:len(prod_savings)], edgecolor='none', height=0.65, zorder=3)
for i, (val, name) in enumerate(zip(prod_savings['Avg Savings'], prod_savings['Product Name'])):
    ax.text(val + 100, i, f'₹{val:,.0f}', va='center', fontsize=9, color='#34d399', fontweight='bold')
ax.set_xlabel('Average Savings (MRP - Selling Price) in ₹', fontsize=12)
ax.set_title('Average Savings Per Product (MRP vs Actual Price)', fontsize=16, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('₹{x:,.0f}'))
ax.grid(True, axis='x', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'savings_per_product.png'))
plt.close()
print("  -> Chart 5: Savings Per Product (savings_per_product.png)")

# --- CHART 6: Price Heatmap - Product vs Website ---
heatmap_data = df.groupby(['Product Name', 'Website'])['Selling Price (₹)'].mean().unstack()
heatmap_data = heatmap_data.sort_values(by=heatmap_data.columns[0], ascending=False)

fig, ax = plt.subplots(figsize=(12, 10))
im = ax.imshow(heatmap_data.values, aspect='auto', cmap='RdYlGn_r')

ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels(heatmap_data.columns, fontsize=10, rotation=30, ha='right')
ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels(heatmap_data.index, fontsize=10)

# Add price text in cells
for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        val = heatmap_data.values[i, j]
        text_color = '#fff' if val > heatmap_data.values.mean() else '#111'
        ax.text(j, i, f'₹{val:,.0f}', ha='center', va='center', fontsize=7.5, 
                color=text_color, fontweight='bold')

cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
cbar.set_label('Avg Selling Price (₹)', fontsize=11, color='#94a3b8')
cbar.ax.yaxis.set_tick_params(color='#94a3b8')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#94a3b8')

ax.set_title('Price Heatmap: Product × Website', fontsize=16, fontweight='bold', pad=15, color='#f8fafc')
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'price_heatmap.png'))
plt.close()
print("  -> Chart 6: Price Heatmap (price_heatmap.png)")

# ============================================================
# STEP 5: EXPORT CLEANED DATA
# ============================================================
print("\n[5/5] Exporting cleaned data...")

cleaned_excel = os.path.join(BASE_DIR, 'data', 'processed', 'DAE_Product_Data_Preprocessed.xlsx')
df.to_excel(cleaned_excel, index=False)

json_path = os.path.join(OUTPUT_DIR, 'data.json')
df.to_json(json_path, orient='records', indent=4)

product_agg_json = product_agg.to_dict(orient='records')
with open(os.path.join(OUTPUT_DIR, 'product_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(product_agg_json, f, indent=4)

with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=4)

print(f"  -> Cleaned Excel: {cleaned_excel}")
print(f"  -> Dashboard JSON: {json_path}")
print(f"  -> Report: {REPORT_FILE}")
print("\n" + "=" * 60)
print("  Pipeline complete! 6 unique charts saved to dashboard/charts/")
print("=" * 60)
