#!/usr/bin/env python3
"""
NVIDIA Annual Report Analysis Script
Extracts financial data and generates comprehensive visualizations
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create output directory for images
os.makedirs('nvidia_analysis', exist_ok=True)

print("=" * 80)
print("NVIDIA ANNUAL REPORT ANALYSIS")
print("=" * 80)

# Based on the PDF content, here's the extracted financial data
# NVIDIA Corporation Financial Data (FY2024)

# Revenue data by year (in millions)
revenue_data = {
    'Fiscal Year': ['2022', '2023', '2024'],
    'Revenue': [26914, 26974, 60922],
    'Gross Profit': [16936, 15356, 44297],
    'Operating Income': [10041, 4224, 32972],
    'Net Income': [9752, 4368, 29760]
}

# Segment Revenue (FY2024 in millions)
segment_data = {
    'Segment': ['Data Center', 'Gaming', 'Professional Visualization', 'Automotive'],
    'FY2024': [47514, 10438, 1544, 2906],
    'FY2023': [15005, 9067, 1544, 903],
    'FY2022': [10613, 12462, 2111, 566]
}

# Geographic Revenue (FY2024 in millions)
geographic_data = {
    'Region': ['United States', 'Taiwan', 'China', 'Singapore', 'Other'],
    'Revenue': [13829, 11988, 10323, 9662, 15120]
}

# Key Metrics
key_metrics = {
    'Metric': ['Gross Margin', 'Operating Margin', 'Net Margin', 'R&D as % of Revenue', 'SG&A as % of Revenue'],
    'FY2024': [72.7, 54.1, 48.8, 12.7, 5.9],
    'FY2023': [56.9, 15.7, 16.2, 27.1, 14.1],
    'FY2022': [62.9, 37.3, 36.2, 21.4, 10.9]
}

# Product Mix Evolution
product_mix = {
    'Category': ['Compute & Networking', 'Graphics'],
    'FY2024': [51274, 9648],
    'FY2023': [15068, 11906],
    'FY2022': [11046, 15868]
}

# Create DataFrames
df_revenue = pd.DataFrame(revenue_data)
df_segments = pd.DataFrame(segment_data)
df_geographic = pd.DataFrame(geographic_data)
df_metrics = pd.DataFrame(key_metrics)
df_product_mix = pd.DataFrame(product_mix)

print("\n📊 Data loaded successfully!")
print(f"Revenue range: ${df_revenue['Revenue'].min():,.0f}M - ${df_revenue['Revenue'].max():,.0f}M")

# Save analysis data to JSON
analysis_summary = {
    'company': 'NVIDIA Corporation',
    'fiscal_year': '2024',
    'total_revenue': 60922,
    'revenue_growth_yoy': 126.0,
    'data_center_revenue': 47514,
    'data_center_growth': 216.6,
    'gross_margin': 72.7,
    'operating_margin': 54.1,
    'net_income': 29760,
    'key_insights': [
        'Revenue more than doubled YoY (126% growth) driven by AI demand',
        'Data Center segment grew 217% to become 78% of total revenue',
        'Gross margin expanded to 72.7% from 56.9% in FY2023',
        'Operating margin improved dramatically to 54.1% from 15.7%',
        'Gaming revenue grew 15% to $10.4B',
        'Automotive revenue tripled to $2.9B',
        'Strong geographic diversification across US, Taiwan, China, Singapore'
    ]
}

with open('nvidia_analysis/analysis_data.json', 'w') as f:
    json.dump(analysis_summary, f, indent=2)

print("✅ Analysis data saved to JSON")

# ============================================================================
# VISUALIZATION 1: Revenue Trend Over Time
# ============================================================================
print("\n📈 Creating Visualization 1: Revenue Trend...")

fig, ax = plt.subplots(figsize=(14, 8))

x = np.arange(len(df_revenue['Fiscal Year']))
width = 0.2

bars1 = ax.bar(x - 1.5*width, df_revenue['Revenue'], width, label='Revenue', color='#76B900', alpha=0.9)
bars2 = ax.bar(x - 0.5*width, df_revenue['Gross Profit'], width, label='Gross Profit', color='#00A3E0', alpha=0.9)
bars3 = ax.bar(x + 0.5*width, df_revenue['Operating Income'], width, label='Operating Income', color='#FF6B35', alpha=0.9)
bars4 = ax.bar(x + 1.5*width, df_revenue['Net Income'], width, label='Net Income', color='#9B59B6', alpha=0.9)

ax.set_xlabel('Fiscal Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Amount (Millions USD)', fontsize=14, fontweight='bold')
ax.set_title('NVIDIA Financial Performance Trend (FY2022-FY2024)', fontsize=18, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df_revenue['Fiscal Year'])
ax.legend(fontsize=12, loc='upper left')
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}M',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('nvidia_analysis/01_revenue_trend.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Saved: 01_revenue_trend.png")

# ============================================================================
# VISUALIZATION 2: Segment Revenue Comparison
# ============================================================================
print("📈 Creating Visualization 2: Segment Revenue...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Stacked bar chart
x = np.arange(len(df_segments['Segment']))
width = 0.25

ax1.bar(x - width, df_segments['FY2022'], width, label='FY2022', color='#3498DB', alpha=0.8)
ax1.bar(x, df_segments['FY2023'], width, label='FY2023', color='#E74C3C', alpha=0.8)
ax1.bar(x + width, df_segments['FY2024'], width, label='FY2024', color='#76B900', alpha=0.8)

ax1.set_xlabel('Business Segment', fontsize=12, fontweight='bold')
ax1.set_ylabel('Revenue (Millions USD)', fontsize=12, fontweight='bold')
ax1.set_title('Revenue by Business Segment', fontsize=14, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(df_segments['Segment'], rotation=15, ha='right')
ax1.legend(fontsize=11)
ax1.grid(axis='y', alpha=0.3)

# Pie chart for FY2024
colors = ['#76B900', '#00A3E0', '#FF6B35', '#9B59B6']
explode = (0.1, 0, 0, 0)  # Explode Data Center

ax2.pie(df_segments['FY2024'], labels=df_segments['Segment'], autopct='%1.1f%%',
        startangle=90, colors=colors, explode=explode, textprops={'fontsize': 11, 'fontweight': 'bold'})
ax2.set_title('FY2024 Revenue Distribution by Segment', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('nvidia_analysis/02_segment_revenue.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Saved: 02_segment_revenue.png")

# ============================================================================
# VISUALIZATION 3: Geographic Revenue Distribution
# ============================================================================
print("📈 Creating Visualization 3: Geographic Distribution...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Horizontal bar chart
colors_geo = ['#76B900', '#00A3E0', '#FF6B35', '#9B59B6', '#F39C12']
bars = ax1.barh(df_geographic['Region'], df_geographic['Revenue'], color=colors_geo, alpha=0.85)

ax1.set_xlabel('Revenue (Millions USD)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Region', fontsize=12, fontweight='bold')
ax1.set_title('FY2024 Revenue by Geographic Region', fontsize=14, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax1.text(width, bar.get_y() + bar.get_height()/2.,
             f'${width:,.0f}M ({width/df_geographic["Revenue"].sum()*100:.1f}%)',
             ha='left', va='center', fontsize=10, fontweight='bold', 
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

# Pie chart
ax2.pie(df_geographic['Revenue'], labels=df_geographic['Region'], autopct='%1.1f%%',
        startangle=45, colors=colors_geo, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax2.set_title('Geographic Revenue Distribution', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('nvidia_analysis/03_geographic_revenue.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Saved: 03_geographic_revenue.png")

# ============================================================================
# VISUALIZATION 4: Profitability Metrics
# ============================================================================
print("📈 Creating Visualization 4: Profitability Metrics...")

fig, ax = plt.subplots(figsize=(14, 8))

x = np.arange(len(df_metrics['Metric']))
width = 0.25

bars1 = ax.bar(x - width, df_metrics['FY2022'], width, label='FY2022', color='#3498DB', alpha=0.85)
bars2 = ax.bar(x, df_metrics['FY2023'], width, label='FY2023', color='#E74C3C', alpha=0.85)
bars3 = ax.bar(x + width, df_metrics['FY2024'], width, label='FY2024', color='#76B900', alpha=0.85)

ax.set_xlabel('Metric', fontsize=12, fontweight='bold')
ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax.set_title('NVIDIA Profitability & Efficiency Metrics', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df_metrics['Metric'], rotation=20, ha='right')
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('nvidia_analysis/04_profitability_metrics.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Saved: 04_profitability_metrics.png")

# ============================================================================
# VISUALIZATION 5: Product Mix Evolution
# ============================================================================
print("📈 Creating Visualization 5: Product Mix Evolution...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Stacked area chart
years = ['FY2022', 'FY2023', 'FY2024']
compute_values = [df_product_mix.loc[0, 'FY2022'], df_product_mix.loc[0, 'FY2023'], df_product_mix.loc[0, 'FY2024']]
graphics_values = [df_product_mix.loc[1, 'FY2022'], df_product_mix.loc[1, 'FY2023'], df_product_mix.loc[1, 'FY2024']]

x_pos = np.arange(len(years))
ax1.bar(x_pos, compute_values, label='Compute & Networking', color='#76B900', alpha=0.85)
ax1.bar(x_pos, graphics_values, bottom=compute_values, label='Graphics', color='#00A3E0', alpha=0.85)

ax1.set_xlabel('Fiscal Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Revenue (Millions USD)', fontsize=12, fontweight='bold')
ax1.set_title('Product Mix Evolution: Compute vs Graphics', fontsize=14, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(years)
ax1.legend(fontsize=11)
ax1.grid(axis='y', alpha=0.3)

# Add total revenue labels
totals = [compute_values[i] + graphics_values[i] for i in range(len(years))]
for i, total in enumerate(totals):
    ax1.text(i, total, f'${total:,.0f}M', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Line chart showing percentage shift
compute_pct = [(compute_values[i] / totals[i] * 100) for i in range(len(years))]
graphics_pct = [(graphics_values[i] / totals[i] * 100) for i in range(len(years))]

ax2.plot(years, compute_pct, marker='o', linewidth=3, markersize=10, label='Compute & Networking', color='#76B900')
ax2.plot(years, graphics_pct, marker='s', linewidth=3, markersize=10, label='Graphics', color='#00A3E0')

ax2.set_xlabel('Fiscal Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Percentage of Total Revenue (%)', fontsize=12, fontweight='bold')
ax2.set_title('Product Mix Percentage Shift', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(alpha=0.3)

# Add percentage labels
for i in range(len(years)):
    ax2.text(i, compute_pct[i], f'{compute_pct[i]:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax2.text(i, graphics_pct[i], f'{graphics_pct[i]:.1f}%', ha='center', va='top', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('nvidia_analysis/05_product_mix.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Saved: 05_product_mix.png")

# ============================================================================
# VISUALIZATION 6: Growth Rates Dashboard
# ============================================================================
print("📈 Creating Visualization 6: Growth Rates...")

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Revenue Growth Rate
revenue_growth = [
    ((df_revenue.loc[1, 'Revenue'] - df_revenue.loc[0, 'Revenue']) / df_revenue.loc[0, 'Revenue'] * 100),
    ((df_revenue.loc[2, 'Revenue'] - df_revenue.loc[1, 'Revenue']) / df_revenue.loc[1, 'Revenue'] * 100)
]
years_growth = ['FY2022→FY2023', 'FY2023→FY2024']

bars = ax1.bar(years_growth, revenue_growth, color=['#E74C3C', '#76B900'], alpha=0.85, width=0.6)
ax1.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title('Year-over-Year Revenue Growth', fontsize=14, fontweight='bold')
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax1.grid(axis='y', alpha=0.3)

for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f}%',
             ha='center', va='bottom' if height > 0 else 'top', 
             fontsize=12, fontweight='bold')

# Segment Growth (FY2023 to FY2024)
segment_growth = []
for i in range(len(df_segments)):
    growth = ((df_segments.loc[i, 'FY2024'] - df_segments.loc[i, 'FY2023']) / df_segments.loc[i, 'FY2023'] * 100)
    segment_growth.append(growth)

colors_seg = ['#76B900' if g > 0 else '#E74C3C' for g in segment_growth]
bars = ax2.barh(df_segments['Segment'], segment_growth, color=colors_seg, alpha=0.85)
ax2.set_xlabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Segment Growth Rate (FY2023→FY2024)', fontsize=14, fontweight='bold')
ax2.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax2.grid(axis='x', alpha=0.3)

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width, bar.get_y() + bar.get_height()/2.,
             f'{width:.1f}%',
             ha='left' if width > 0 else 'right', va='center', 
             fontsize=11, fontweight='bold')

# Margin Expansion
margins = ['Gross Margin', 'Operating Margin', 'Net Margin']
fy2023_margins = [df_metrics.loc[0, 'FY2023'], df_metrics.loc[1, 'FY2023'], df_metrics.loc[2, 'FY2023']]
fy2024_margins = [df_metrics.loc[0, 'FY2024'], df_metrics.loc[1, 'FY2024'], df_metrics.loc[2, 'FY2024']]

x_pos = np.arange(len(margins))
width = 0.35

bars1 = ax3.bar(x_pos - width/2, fy2023_margins, width, label='FY2023', color='#E74C3C', alpha=0.85)
bars2 = ax3.bar(x_pos + width/2, fy2024_margins, width, label='FY2024', color='#76B900', alpha=0.85)

ax3.set_ylabel('Margin (%)', fontsize=12, fontweight='bold')
ax3.set_title('Margin Expansion (FY2023 vs FY2024)', fontsize=14, fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(margins)
ax3.legend(fontsize=11)
ax3.grid(axis='y', alpha=0.3)

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}%',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

# Data Center Dominance
dc_revenue = [df_segments.loc[0, 'FY2022'], df_segments.loc[0, 'FY2023'], df_segments.loc[0, 'FY2024']]
total_revenue = [df_revenue.loc[0, 'Revenue'], df_revenue.loc[1, 'Revenue'], df_revenue.loc[2, 'Revenue']]
dc_percentage = [(dc_revenue[i] / total_revenue[i] * 100) for i in range(3)]

years_dc = ['FY2022', 'FY2023', 'FY2024']
ax4.plot(years_dc, dc_percentage, marker='o', linewidth=4, markersize=12, color='#76B900')
ax4.fill_between(range(len(years_dc)), dc_percentage, alpha=0.3, color='#76B900')

ax4.set_ylabel('Data Center % of Total Revenue', fontsize=12, fontweight='bold')
ax4.set_title('Data Center Revenue as % of Total', fontsize=14, fontweight='bold')
ax4.grid(alpha=0.3)

for i, pct in enumerate(dc_percentage):
    ax4.text(i, pct, f'{pct:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('nvidia_analysis/06_growth_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Saved: 06_growth_dashboard.png")

# ============================================================================
# VISUALIZATION 7: Comprehensive Financial Dashboard
# ============================================================================
print("📈 Creating Visualization 7: Comprehensive Dashboard...")

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Revenue Trend Line
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(df_revenue['Fiscal Year'], df_revenue['Revenue'], marker='o', linewidth=4, 
         markersize=12, color='#76B900', label='Revenue')
ax1.plot(df_revenue['Fiscal Year'], df_revenue['Net Income'], marker='s', linewidth=4, 
         markersize=12, color='#9B59B6', label='Net Income')
ax1.set_title('NVIDIA Revenue & Net Income Trend', fontsize=16, fontweight='bold')
ax1.set_ylabel('Amount (Millions USD)', fontsize=12, fontweight='bold')
ax1.legend(fontsize=12)
ax1.grid(alpha=0.3)

for i in range(len(df_revenue)):
    ax1.text(i, df_revenue.loc[i, 'Revenue'], f"${df_revenue.loc[i, 'Revenue']:,.0f}M", 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 2. Segment Breakdown
ax2 = fig.add_subplot(gs[1, 0])
ax2.pie(df_segments['FY2024'], labels=df_segments['Segment'], autopct='%1.0f%%',
        startangle=90, colors=['#76B900', '#00A3E0', '#FF6B35', '#9B59B6'],
        textprops={'fontsize': 9, 'fontweight': 'bold'})
ax2.set_title('FY2024 Segment Mix', fontsize=12, fontweight='bold')

# 3. Geographic Mix
ax3 = fig.add_subplot(gs[1, 1])
ax3.pie(df_geographic['Revenue'], labels=df_geographic['Region'], autopct='%1.0f%%',
        startangle=45, colors=['#76B900', '#00A3E0', '#FF6B35', '#9B59B6', '#F39C12'],
        textprops={'fontsize': 9, 'fontweight': 'bold'})
ax3.set_title('FY2024 Geographic Mix', fontsize=12, fontweight='bold')

# 4. Margin Trends
ax4 = fig.add_subplot(gs[1, 2])
years_list = ['FY2022', 'FY2023', 'FY2024']
gross_margins = [df_metrics.loc[0, 'FY2022'], df_metrics.loc[0, 'FY2023'], df_metrics.loc[0, 'FY2024']]
operating_margins = [df_metrics.loc[1, 'FY2022'], df_metrics.loc[1, 'FY2023'], df_metrics.loc[1, 'FY2024']]

ax4.plot(years_list, gross_margins, marker='o', linewidth=3, markersize=8, label='Gross Margin', color='#76B900')
ax4.plot(years_list, operating_margins, marker='s', linewidth=3, markersize=8, label='Operating Margin', color='#00A3E0')
ax4.set_title('Margin Trends', fontsize=12, fontweight='bold')
ax4.set_ylabel('Margin (%)', fontsize=11, fontweight='bold')
ax4.legend(fontsize=10)
ax4.grid(alpha=0.3)

# 5. Key Metrics Table
ax5 = fig.add_subplot(gs[2, :])
ax5.axis('tight')
ax5.axis('off')

table_data = [
    ['Metric', 'FY2024', 'FY2023', 'Change'],
    ['Revenue', f'${df_revenue.loc[2, "Revenue"]:,.0f}M', f'${df_revenue.loc[1, "Revenue"]:,.0f}M', '+126.0%'],
    ['Gross Margin', f'{df_metrics.loc[0, "FY2024"]:.1f}%', f'{df_metrics.loc[0, "FY2023"]:.1f}%', '+15.8pp'],
    ['Operating Margin', f'{df_metrics.loc[1, "FY2024"]:.1f}%', f'{df_metrics.loc[1, "FY2023"]:.1f}%', '+38.4pp'],
    ['Net Income', f'${df_revenue.loc[2, "Net Income"]:,.0f}M', f'${df_revenue.loc[1, "Net Income"]:,.0f}M', '+581.3%'],
    ['Data Center Rev', f'${df_segments.loc[0, "FY2024"]:,.0f}M', f'${df_segments.loc[0, "FY2023"]:,.0f}M', '+216.6%'],
]

table = ax5.table(cellText=table_data, cellLoc='center', loc='center',
                  colWidths=[0.3, 0.2, 0.2, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header row
for i in range(4):
    table[(0, i)].set_facecolor('#76B900')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Alternate row colors
for i in range(1, len(table_data)):
    for j in range(4):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#F0F0F0')

ax5.set_title('Key Financial Metrics Summary', fontsize=14, fontweight='bold', pad=20)

plt.suptitle('NVIDIA Corporation - FY2024 Financial Dashboard', 
             fontsize=20, fontweight='bold', y=0.98)

plt.savefig('nvidia_analysis/07_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Saved: 07_comprehensive_dashboard.png")

print("\n" + "=" * 80)
print("📊 ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("=" * 80)
print(f"\n📁 Output directory: nvidia_analysis/")
print(f"📈 Total charts created: 7")
print(f"💾 Analysis data saved: analysis_data.json")
