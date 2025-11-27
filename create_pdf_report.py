#!/usr/bin/env python3
"""
Create a comprehensive PDF report with all NVIDIA visualizations
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
import os

print("=" * 80)
print("CREATING NVIDIA ANALYSIS PDF REPORT")
print("=" * 80)

# Create PDF document
pdf_filename = 'nvidia_analysis/NVIDIA_Financial_Analysis_Report.pdf'
doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#76B900'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#00A3E0'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=12
)

# Title Page
elements.append(Spacer(1, 1.5*inch))
title = Paragraph("NVIDIA Corporation", title_style)
elements.append(title)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Heading2'],
    fontSize=18,
    textColor=colors.HexColor('#333333'),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica'
)
subtitle = Paragraph("Financial Analysis Report - FY2024", subtitle_style)
elements.append(subtitle)

elements.append(Spacer(1, 0.5*inch))

# Executive Summary
exec_summary = Paragraph("<b>Executive Summary</b>", heading_style)
elements.append(exec_summary)

summary_text = """
NVIDIA Corporation delivered exceptional financial performance in FY2024, driven by unprecedented 
demand for AI computing infrastructure. The company's revenue more than doubled year-over-year, 
reaching $60.9 billion, representing a remarkable 126% growth rate. This extraordinary performance 
was primarily fueled by the Data Center segment, which grew 217% to $47.5 billion and now represents 
78% of total revenue.
<br/><br/>
Key highlights include significant margin expansion with gross margin improving to 72.7% from 56.9%, 
and operating margin surging to 54.1% from 15.7%. Net income reached $29.8 billion, an increase of 
581% year-over-year. The company's strategic focus on AI and accelerated computing has positioned 
it as the dominant player in the rapidly expanding AI infrastructure market.
"""
elements.append(Paragraph(summary_text, body_style))
elements.append(Spacer(1, 0.3*inch))

# Key Metrics Table
elements.append(Paragraph("<b>Key Financial Metrics</b>", heading_style))

data = [
    ['Metric', 'FY2024', 'FY2023', 'YoY Change'],
    ['Total Revenue', '$60.9B', '$27.0B', '+126.0%'],
    ['Data Center Revenue', '$47.5B', '$15.0B', '+216.6%'],
    ['Gross Margin', '72.7%', '56.9%', '+15.8pp'],
    ['Operating Margin', '54.1%', '15.7%', '+38.4pp'],
    ['Net Income', '$29.8B', '$4.4B', '+581.3%'],
    ['Gaming Revenue', '$10.4B', '$9.1B', '+15.0%'],
    ['Automotive Revenue', '$2.9B', '$0.9B', '+221.8%'],
]

table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#76B900')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

elements.append(table)
elements.append(PageBreak())

# Visualization 1: Revenue Trend
elements.append(Paragraph("<b>1. Financial Performance Trend</b>", heading_style))
insight1 = """
NVIDIA's financial trajectory shows explosive growth in FY2024 after a relatively flat FY2023. 
Revenue jumped from $27.0B to $60.9B, while net income surged from $4.4B to $29.8B. This represents 
one of the most dramatic financial turnarounds in technology sector history, driven by the AI revolution 
and NVIDIA's dominant position in GPU computing.
"""
elements.append(Paragraph(insight1, body_style))
img1 = Image('nvidia_analysis/01_revenue_trend.png', width=7*inch, height=4.67*inch)
elements.append(img1)
elements.append(PageBreak())

# Visualization 2: Segment Revenue
elements.append(Paragraph("<b>2. Business Segment Analysis</b>", heading_style))
insight2 = """
The Data Center segment has become NVIDIA's primary growth engine, accounting for 78% of total revenue 
in FY2024. This segment grew 217% year-over-year, driven by demand for AI training and inference 
infrastructure. Gaming remains the second-largest segment at $10.4B (17% of revenue), while Automotive 
showed strong growth, tripling to $2.9B as autonomous vehicle technology advances.
"""
elements.append(Paragraph(insight2, body_style))
img2 = Image('nvidia_analysis/02_segment_revenue.png', width=7*inch, height=3.83*inch)
elements.append(img2)
elements.append(PageBreak())

# Visualization 3: Geographic Distribution
elements.append(Paragraph("<b>3. Geographic Revenue Distribution</b>", heading_style))
insight3 = """
NVIDIA maintains strong geographic diversification with significant presence across key markets. 
The United States leads at $13.8B (23%), followed by Taiwan at $12.0B (20%), China at $10.3B (17%), 
and Singapore at $9.7B (16%). This diversification reduces regional risk while capturing growth 
opportunities across global AI infrastructure buildouts.
"""
elements.append(Paragraph(insight3, body_style))
img3 = Image('nvidia_analysis/03_geographic_revenue.png', width=7*inch, height=3.83*inch)
elements.append(img3)
elements.append(PageBreak())

# Visualization 4: Profitability Metrics
elements.append(Paragraph("<b>4. Profitability & Efficiency Metrics</b>", heading_style))
insight4 = """
NVIDIA's profitability metrics show remarkable improvement across all dimensions. Gross margin expanded 
to 72.7%, reflecting strong pricing power and favorable product mix. Operating margin surged to 54.1%, 
demonstrating exceptional operational leverage. The company maintained disciplined spending with R&D 
at 12.7% and SG&A at 5.9% of revenue, down significantly from prior years as revenue scaled dramatically.
"""
elements.append(Paragraph(insight4, body_style))
img4 = Image('nvidia_analysis/04_profitability_metrics.png', width=7*inch, height=4.67*inch)
elements.append(img4)
elements.append(PageBreak())

# Visualization 5: Product Mix
elements.append(Paragraph("<b>5. Product Mix Evolution</b>", heading_style))
insight5 = """
The product mix has shifted dramatically toward Compute & Networking, which now represents 84% of 
revenue ($51.3B) compared to just 41% in FY2022. This reflects the fundamental transformation of 
NVIDIA from a graphics-focused company to an AI computing infrastructure leader. Graphics products 
remain important at $9.6B but now represent only 16% of total revenue.
"""
elements.append(Paragraph(insight5, body_style))
img5 = Image('nvidia_analysis/05_product_mix.png', width=7*inch, height=3.83*inch)
elements.append(img5)
elements.append(PageBreak())

# Visualization 6: Growth Dashboard
elements.append(Paragraph("<b>6. Growth Rates Analysis</b>", heading_style))
insight6 = """
Growth metrics highlight NVIDIA's acceleration in FY2024. After minimal growth in FY2023 (0.2%), 
revenue exploded by 126% in FY2024. Data Center led with 217% growth, followed by Automotive at 222%. 
Margin expansion was equally impressive, with operating margin improving by 38.4 percentage points. 
The Data Center segment's share of total revenue increased from 39% in FY2022 to 78% in FY2024.
"""
elements.append(Paragraph(insight6, body_style))
img6 = Image('nvidia_analysis/06_growth_dashboard.png', width=7*inch, height=7*inch)
elements.append(img6)
elements.append(PageBreak())

# Visualization 7: Comprehensive Dashboard
elements.append(Paragraph("<b>7. Comprehensive Financial Dashboard</b>", heading_style))
insight7 = """
The comprehensive dashboard provides a holistic view of NVIDIA's financial performance. The upward 
trajectory in revenue and net income is unmistakable, with both metrics showing exponential growth 
in FY2024. The segment and geographic mix charts illustrate the company's diversified revenue base, 
while margin trends confirm sustained profitability improvements. The summary table captures the 
magnitude of year-over-year changes across all key metrics.
"""
elements.append(Paragraph(insight7, body_style))
img7 = Image('nvidia_analysis/07_comprehensive_dashboard.png', width=7*inch, height=7*inch)
elements.append(img7)
elements.append(PageBreak())

# Strategic Insights
elements.append(Paragraph("<b>Strategic Insights & Outlook</b>", heading_style))

insights_text = """
<b>1. AI Market Leadership:</b> NVIDIA has established itself as the dominant provider of AI computing 
infrastructure, with its GPUs becoming the de facto standard for AI training and inference workloads.
<br/><br/>
<b>2. Exceptional Operational Leverage:</b> The company demonstrated remarkable operational leverage, 
with revenue more than doubling while maintaining disciplined cost management, resulting in operating 
margin expansion of 38 percentage points.
<br/><br/>
<b>3. Data Center Transformation:</b> The Data Center segment's growth from $10.6B in FY2022 to $47.5B 
in FY2024 represents a fundamental business transformation, positioning NVIDIA at the center of the 
AI infrastructure buildout.
<br/><br/>
<b>4. Diversified Growth:</b> While Data Center dominates, other segments show healthy growth with 
Gaming up 15% and Automotive tripling, providing multiple growth vectors.
<br/><br/>
<b>5. Pricing Power:</b> Gross margin expansion to 72.7% demonstrates strong pricing power driven by 
limited competition in high-performance AI accelerators and strong demand exceeding supply.
<br/><br/>
<b>6. Geographic Reach:</b> Balanced geographic distribution across US, Asia, and other regions 
provides resilience and access to global AI infrastructure investments.
<br/><br/>
<b>7. Future Outlook:</b> With continued AI adoption across industries, cloud infrastructure expansion, 
and emerging applications in autonomous vehicles and robotics, NVIDIA is well-positioned for sustained 
growth, though at more normalized rates as the revenue base expands.
"""
elements.append(Paragraph(insights_text, body_style))

elements.append(Spacer(1, 0.5*inch))

# Footer
footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.grey,
    alignment=TA_CENTER
)
footer = Paragraph("NVIDIA Corporation Financial Analysis Report | FY2024 | Generated from Annual Report Data", footer_style)
elements.append(footer)

# Build PDF
doc.build(elements)

print("\n✅ PDF Report created successfully!")
print(f"📄 File: {pdf_filename}")
print(f"📊 Pages: Multiple pages with 7 visualizations")
print(f"💡 Includes: Executive summary, key metrics, insights, and comprehensive analysis")
print("=" * 80)
