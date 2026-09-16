"""
DAE Project: Statistical Visualization Suite (Matplotlib + Seaborn)
===================================================================
Batch-4: Web Scraping and Product Price Analysis System
Technologies Demonstrated:
  - Python 3
  - Seaborn (Advanced Statistical Data Visualization)
  - Matplotlib (Figure layout, formatting, and high-DPI export)
  - Pandas (Data slicing and grouping)

Generates 5 publication-ready statistical graphics:
  1. Category Price Distribution Box Plot (IQR & Outliers)
  2. Rating vs Price Scatter Plot with Linear Regression Trendline
  3. Category Price Density Violin Plot
  4. Retailer Discount Distribution KDE (Kernel Density Estimation)
  5. Retailer × Category Price Heatmap with Annotations
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_EXCEL = os.path.join(BASE_DIR, 'data', 'processed', 'DAE_Product_Data_Preprocessed.xlsx')
OUTPUT_CHARTS_DIR = os.path.join(BASE_DIR, 'dashboard', 'charts')
os.makedirs(OUTPUT_CHARTS_DIR, exist_ok=True)

# Define cohesive dark luxury aesthetic matching the dashboard
plt.style.use('dark_background')
DARK_BG = '#0a0a0f'
PANEL_BG = '#12121a'
GRID_COLOR = '#222233'
TEXT_COLOR = '#f1f5f9'
MUTED_TEXT = '#94a3b8'

custom_params = {
    'figure.facecolor': DARK_BG,
    'axes.facecolor': PANEL_BG,
    'axes.edgecolor': '#2a2a3e',
    'axes.labelcolor': TEXT_COLOR,
    'xtick.color': MUTED_TEXT,
    'ytick.color': MUTED_TEXT,
    'grid.color': GRID_COLOR,
    'grid.linestyle': '--',
    'grid.alpha': 0.5,
    'text.color': TEXT_COLOR,
    'font.family': 'sans-serif',
    'figure.dpi': 160
}
sns.set_theme(style="darkgrid", rc=custom_params)

PALETTE_VIBRANT = ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b', '#8b5cf6', '#06b6d4', '#10b981']


def main():
    print("=" * 65)
    print("  DAE Seaborn & Matplotlib Visualization Pipeline")
    print("=" * 65)

    if not os.path.exists(INPUT_EXCEL):
        print(f"Error: Dataset not found at {INPUT_EXCEL}")
        return

    df = pd.read_excel(INPUT_EXCEL)
    print(f"\n[Step 1] Loaded dataset with {len(df)} records.")

    # -------------------------------------------------------------
    # 1. BOX PLOT: Category Price Distribution (IQR, Median & Outliers)
    # -------------------------------------------------------------
    print("\n[Step 2] Generating Chart 1: Category Price Box Plot...")
    fig, ax = plt.subplots(figsize=(13, 7))
    sorted_cats = df.groupby('Category')['Selling Price (₹)'].median().sort_values(ascending=False).index

    sns.boxplot(
        data=df,
        x='Category',
        y='Selling Price (₹)',
        order=sorted_cats,
        palette=PALETTE_VIBRANT,
        ax=ax,
        fliersize=3.5,
        linewidth=1.4,
        boxprops=dict(alpha=0.85)
    )

    ax.set_title("Price Distribution & Outlier Spread by Category (Seaborn Boxplot)", fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel("Product Category", fontsize=12, fontweight='600')
    ax.set_ylabel("Selling Price (₹)", fontsize=12, fontweight='600')
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('₹{x:,.0f}'))
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    p1 = os.path.join(OUTPUT_CHARTS_DIR, 'price_distribution_boxplot.png')
    plt.savefig(p1)
    plt.close()
    print(f"  -> Saved: {p1}")

    # -------------------------------------------------------------
    # 2. SCATTER & REGRESSION: Rating vs. Selling Price
    # -------------------------------------------------------------
    print("\n[Step 3] Generating Chart 2: Rating vs Price Regression Scatter...")
    fig, ax = plt.subplots(figsize=(13, 7))

    sns.regplot(
        data=df,
        x='Selling Price (₹)',
        y='Rating',
        scatter_kws={'alpha': 0.45, 'color': '#06b6d4', 's': 30},
        line_kws={'color': '#f43f5e', 'linewidth': 2.5, 'label': 'Linear Fit Trendline'},
        ax=ax
    )

    ax.set_title("Relationship Between Product Price & Customer Rating (Seaborn Regplot)", fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel("Selling Price (₹)", fontsize=12, fontweight='600')
    ax.set_ylabel("Customer Rating (Stars)", fontsize=12, fontweight='600')
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('₹{x:,.0f}'))
    ax.set_ylim(3.8, 5.0)
    ax.legend(facecolor='#1e1e2e', edgecolor='#2a2a3e')
    plt.tight_layout()
    p2 = os.path.join(OUTPUT_CHARTS_DIR, 'rating_vs_price_scatter.png')
    plt.savefig(p2)
    plt.close()
    print(f"  -> Saved: {p2}")

    # -------------------------------------------------------------
    # 3. VIOLIN PLOT: Price Density & Distribution Shapes
    # -------------------------------------------------------------
    print("\n[Step 4] Generating Chart 3: Category Price Violin Plot...")
    fig, ax = plt.subplots(figsize=(13, 7))

    sns.violinplot(
        data=df,
        x='Category',
        y='Selling Price (₹)',
        order=sorted_cats,
        palette=PALETTE_VIBRANT,
        cut=0,
        inner="quartile",
        linewidth=1.2,
        ax=ax
    )

    ax.set_title("Probability Density of Product Prices Across Categories (Seaborn Violin Plot)", fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel("Product Category", fontsize=12, fontweight='600')
    ax.set_ylabel("Selling Price (₹)", fontsize=12, fontweight='600')
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('₹{x:,.0f}'))
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    p3 = os.path.join(OUTPUT_CHARTS_DIR, 'category_violin_plot.png')
    plt.savefig(p3)
    plt.close()
    print(f"  -> Saved: {p3}")

    # -------------------------------------------------------------
    # 4. KDE DISTRIBUTION: Retailer Discount Density Curves
    # -------------------------------------------------------------
    print("\n[Step 5] Generating Chart 4: Platform Discount KDE Curves...")
    fig, ax = plt.subplots(figsize=(13, 7))

    websites = df['Website'].unique()
    for i, w in enumerate(websites):
        subset = df[df['Website'] == w]
        sns.kdeplot(
            subset['Discount (%)'],
            ax=ax,
            label=w,
            fill=True,
            alpha=0.18,
            linewidth=2.2,
            color=PALETTE_VIBRANT[i % len(PALETTE_VIBRANT)]
        )

    ax.set_title("Retailer Discount Percentage Distribution (Seaborn Kernel Density Estimation)", fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel("Discount Percentage (%)", fontsize=12, fontweight='600')
    ax.set_ylabel("Density", fontsize=12, fontweight='600')
    ax.legend(title="Retail Platform", facecolor='#1e1e2e', edgecolor='#2a2a3e')
    plt.tight_layout()
    p4 = os.path.join(OUTPUT_CHARTS_DIR, 'platform_discount_kde.png')
    plt.savefig(p4)
    plt.close()
    print(f"  -> Saved: {p4}")

    # -------------------------------------------------------------
    # 5. HEATMAP: Category × Retailer Average Selling Price Matrix
    # -------------------------------------------------------------
    print("\n[Step 6] Generating Chart 5: Category × Website Price Heatmap...")
    fig, ax = plt.subplots(figsize=(12, 7))

    pivot_cat_site = df.pivot_table(index='Category', columns='Website', values='Selling Price (₹)', aggfunc='mean')

    sns.heatmap(
        pivot_cat_site,
        annot=True,
        fmt=",.0f",
        cmap="mako",
        cbar_kws={'label': 'Average Price (₹)'},
        linewidths=0.8,
        linecolor='#0a0a0f',
        ax=ax
    )

    ax.set_title("Average Selling Price Heatmap: Category vs. Retailer (Seaborn Heatmap)", fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel("Retail Platform", fontsize=12, fontweight='600')
    ax.set_ylabel("Product Category", fontsize=12, fontweight='600')
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    p5 = os.path.join(OUTPUT_CHARTS_DIR, 'platform_price_heatmap.png')
    plt.savefig(p5)
    plt.close()
    print(f"  -> Saved: {p5}")

    print("\n" + "=" * 65)
    print("  All 5 Seaborn Statistical Charts generated successfully!")
    print("=" * 65)


if __name__ == "__main__":
    main()
