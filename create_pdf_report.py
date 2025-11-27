#!/usr/bin/env python3
"""
NVIDIA PDF Report Generator
Compiles all visualizations into a comprehensive PDF report
"""

import json
from fpdf import FPDF
from datetime import datetime
import os

class NVIDIAReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """Add header to each page"""
        self.set_font('Arial', 'B', 12)
        self.set_text_color(118, 185, 0)  # NVIDIA green
        self.cell(0, 10, 'NVIDIA Annual Report Analysis', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        """Add footer to each page"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title):
        """Add chapter title"""
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
        
    def chapter_body(self, body):
        """Add chapter body text"""
        self.set_font('Arial', '', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, body)
        self.ln()

def create_pdf_report(insights_path, chart_paths, output_path):
    """Create comprehensive PDF report with all visualizations"""
    print("\n📄 Creating PDF Report...")
    
    # Load insights
    with open(insights_path, 'r') as f:
        insights = json.load(f)
    
    # Initialize PDF
    pdf = NVIDIAReportPDF()
    pdf.set_title('NVIDIA Annual Report Analysis')
    pdf.set_author('Blackbox AI Analysis')
    
    # Cover Page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 28)
    pdf.set_text_color(118, 185, 0)
    pdf.ln(40)
    pdf.cell(0, 20, 'NVIDIA Corporation', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, 'Annual Report Analysis', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
    pdf.ln(20)
    
    # Executive Summary Box
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, 'Executive Summary', 0, 1, 'C', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    summary_text = """This comprehensive analysis examines NVIDIA's annual report, extracting key insights 
across business segments, technology focus areas, market positioning, and strategic themes. 
The report includes detailed visualizations and data-driven insights to understand NVIDIA's 
business priorities and market strategy."""
    pdf.multi_cell(0, 6, summary_text)
    
    # Key Statistics
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Key Statistics:', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    segments = insights.get('business_segments', {})
    tech = insights.get('technology_focus', {})
    market = insights.get('market_insights', {})
    
    if segments:
        top_segment = max(segments.items(), key=lambda x: x[1])
        pdf.cell(0, 6, f'  - Top Business Segment: {top_segment[0]} ({top_segment[1]} mentions)', 0, 1)
    
    if tech:
        top_tech = max(tech.items(), key=lambda x: x[1])
        pdf.cell(0, 6, f'  - Leading Technology: {top_tech[0]} ({top_tech[1]} mentions)', 0, 1)
    
    if market:
        top_market = max(market.items(), key=lambda x: x[1])
        pdf.cell(0, 6, f'  - Key Strategic Theme: {top_market[0]} ({top_market[1]} mentions)', 0, 1)
    
    pdf.cell(0, 6, f'  - Total Business Segments Analyzed: {len(segments)}', 0, 1)
    pdf.cell(0, 6, f'  - Technology Products Referenced: {len(tech)}', 0, 1)
    
    # Visualization Pages
    visualizations = [
        {
            'title': 'Business Segments Analysis',
            'description': 'This visualization shows the frequency of business segment mentions throughout the annual report. Higher mention counts indicate areas of strategic focus and operational emphasis for NVIDIA.',
            'path': chart_paths[0]
        },
        {
            'title': 'Technology & Product Focus',
            'description': 'Analysis of NVIDIA\'s key technologies and products referenced in the report. This highlights the company\'s technological priorities and product portfolio emphasis.',
            'path': chart_paths[1]
        },
        {
            'title': 'Market & Strategic Positioning',
            'description': 'Strategic themes and market positioning keywords reveal NVIDIA\'s competitive strategy, growth focus areas, and market approach.',
            'path': chart_paths[2]
        },
        {
            'title': 'Temporal Analysis',
            'description': 'Year reference timeline showing which time periods are most frequently discussed, indicating historical context and forward-looking statements.',
            'path': chart_paths[3]
        },
        {
            'title': 'Comprehensive Dashboard',
            'description': 'Multi-panel dashboard providing an integrated view of all key metrics, business segments, technologies, and strategic themes in a single comprehensive visualization.',
            'path': chart_paths[4]
        },
        {
            'title': 'Focus Intensity Heatmap',
            'description': 'Correlation heatmap showing the relative intensity and relationships between different focus areas, revealing interconnections in NVIDIA\'s business strategy.',
            'path': chart_paths[5]
        }
    ]
    
    for viz in visualizations:
        if viz['path'] and os.path.exists(viz['path']):
            pdf.add_page()
            pdf.chapter_title(viz['title'])
            pdf.chapter_body(viz['description'])
            pdf.ln(5)
            
            # Add image - full width
            pdf.image(viz['path'], x=10, w=190)
            print(f"  ✓ Added: {viz['title']}")
    
    # Detailed Insights Page
    pdf.add_page()
    pdf.chapter_title('Detailed Insights')
    
    # Business Segments Detail
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Business Segments Breakdown:', 0, 1)
    pdf.set_font('Arial', '', 9)
    
    for segment, count in sorted(segments.items(), key=lambda x: x[1], reverse=True):
        pdf.cell(0, 5, f'  - {segment}: {count} mentions', 0, 1)
    
    pdf.ln(5)
    
    # Technology Detail
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Technology & Products:', 0, 1)
    pdf.set_font('Arial', '', 9)
    
    for technology, count in sorted(tech.items(), key=lambda x: x[1], reverse=True):
        pdf.cell(0, 5, f'  - {technology}: {count} mentions', 0, 1)
    
    pdf.ln(5)
    
    # Market Insights Detail
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, 'Strategic Market Themes:', 0, 1)
    pdf.set_font('Arial', '', 9)
    
    for theme, count in sorted(market.items(), key=lambda x: x[1], reverse=True):
        pdf.cell(0, 5, f'  - {theme}: {count} mentions', 0, 1)
    
    # Conclusion Page
    pdf.add_page()
    pdf.chapter_title('Conclusion')
    
    conclusion = """This analysis provides a comprehensive view of NVIDIA's annual report through data-driven 
visualizations and quantitative insights. The findings reveal:

1. STRATEGIC FOCUS: NVIDIA's primary emphasis on AI, data center, and gaming segments reflects 
   the company's positioning in high-growth technology markets.

2. TECHNOLOGY LEADERSHIP: Strong references to proprietary technologies (CUDA, RTX, Tensor Cores) 
   demonstrate NVIDIA's commitment to maintaining technological differentiation.

3. MARKET POSITIONING: Frequent mentions of growth, innovation, and leadership indicate an 
   aggressive market strategy focused on expansion and market share gains.

4. FUTURE OUTLOOK: The temporal analysis and forward-looking statements suggest continued 
   investment in emerging technologies and market opportunities.

This report serves as a quantitative foundation for understanding NVIDIA's business strategy, 
operational priorities, and market positioning as communicated in their annual report."""
    
    pdf.chapter_body(conclusion)
    
    # Save PDF
    pdf.output(output_path)
    print(f"\n✅ PDF Report saved: {output_path}")
    print(f"   Total pages: {pdf.page_no()}")
    
    return output_path

if __name__ == "__main__":
    print("="*60)
    print("📊 NVIDIA PDF REPORT GENERATION")
    print("="*60)
    
    insights_path = '/vercel/sandbox/nvidia_insights.json'
    chart_paths = [
        '/vercel/sandbox/chart_1_business_segments.png',
        '/vercel/sandbox/chart_2_technology_focus.png',
        '/vercel/sandbox/chart_3_market_insights.png',
        '/vercel/sandbox/chart_4_year_mentions.png',
        '/vercel/sandbox/chart_5_comprehensive_dashboard.png',
        '/vercel/sandbox/chart_6_heatmap.png'
    ]
    output_path = '/vercel/sandbox/nvidia_analysis_report.pdf'
    
    create_pdf_report(insights_path, chart_paths, output_path)
    
    print("\n" + "="*60)
    print("✅ PHASE 3 COMPLETE: PDF Report Generation")
    print("="*60)
