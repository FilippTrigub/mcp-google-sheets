#!/usr/bin/env python3
"""
NVIDIA Annual Report Analysis Script
Extracts financial data and generates comprehensive visualizations
"""

import json
import re
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime

# Set style for professional visualizations
sns.set_style('whitegrid')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF"""
    print("📄 Extracting text from PDF...")
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(f"✓ Extracted {len(text)} characters from {len(reader.pages)} pages")
    return text

def analyze_nvidia_data(text):
    """Extract and analyze key financial metrics from NVIDIA report"""
    print("\n🔍 Analyzing NVIDIA financial data...")
    
    insights = {
        "company": "NVIDIA Corporation",
        "report_type": "Annual Report",
        "extraction_date": datetime.now().isoformat(),
        "key_metrics": {},
        "business_segments": {},
        "financial_highlights": {},
        "market_insights": {},
        "technology_focus": []
    }
    
    # Extract revenue data (looking for patterns like "$XX.X billion" or "$XX,XXX million")
    revenue_patterns = re.findall(r'\$(\d+[,.]?\d*)\s*(billion|million)', text, re.IGNORECASE)
    if revenue_patterns:
        revenues = []
        for amount, unit in revenue_patterns[:10]:  # Get first 10 mentions
            amount_clean = float(amount.replace(',', ''))
            if unit.lower() == 'billion':
                revenues.append(amount_clean * 1000)  # Convert to millions
            else:
                revenues.append(amount_clean)
        
        if revenues:
            insights["key_metrics"]["revenue_mentions"] = revenues
            insights["key_metrics"]["max_revenue_mentioned"] = max(revenues)
            insights["key_metrics"]["avg_revenue_mentioned"] = sum(revenues) / len(revenues)
    
    # Extract year mentions
    years = re.findall(r'\b(20\d{2})\b', text)
    year_counts = {}
    for year in years:
        year_counts[year] = year_counts.get(year, 0) + 1
    insights["key_metrics"]["year_mentions"] = dict(sorted(year_counts.items(), reverse=True)[:10])
    
    # Business segments analysis
    segments = {
        "Data Center": text.lower().count("data center"),
        "Gaming": text.lower().count("gaming"),
        "Professional Visualization": text.lower().count("professional visualization"),
        "Automotive": text.lower().count("automotive"),
        "AI": text.lower().count(" ai ") + text.lower().count("artificial intelligence"),
        "GPU": text.lower().count("gpu"),
        "Cloud": text.lower().count("cloud"),
        "Machine Learning": text.lower().count("machine learning"),
        "Deep Learning": text.lower().count("deep learning")
    }
    insights["business_segments"] = {k: v for k, v in sorted(segments.items(), key=lambda x: x[1], reverse=True)}
    
    # Technology keywords
    tech_keywords = ["CUDA", "RTX", "GeForce", "Tensor Core", "Hopper", "Ada Lovelace", 
                     "Omniverse", "DGX", "HGX", "Grace", "Jetson", "DRIVE"]
    tech_mentions = {}
    for keyword in tech_keywords:
        count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE))
        if count > 0:
            tech_mentions[keyword] = count
    insights["technology_focus"] = dict(sorted(tech_mentions.items(), key=lambda x: x[1], reverse=True))
    
    # Market and competitive keywords
    market_terms = {
        "Growth": text.lower().count("growth"),
        "Innovation": text.lower().count("innovation"),
        "Leadership": text.lower().count("leadership"),
        "Market Share": text.lower().count("market share"),
        "Competition": text.lower().count("competition"),
        "Investment": text.lower().count("investment"),
        "Research & Development": text.lower().count("research and development") + text.lower().count("r&d")
    }
    insights["market_insights"] = {k: v for k, v in sorted(market_terms.items(), key=lambda x: x[1], reverse=True)}
    
    # Extract percentage mentions (growth rates, margins, etc.)
    percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%', text)
    if percentages:
        pct_values = [float(p) for p in percentages if float(p) < 1000]  # Filter outliers
        insights["financial_highlights"]["percentage_mentions"] = {
            "count": len(pct_values),
            "average": round(sum(pct_values) / len(pct_values), 2) if pct_values else 0,
            "max": max(pct_values) if pct_values else 0,
            "min": min(pct_values) if pct_values else 0
        }
    
    print(f"✓ Extracted {len(insights['business_segments'])} business segments")
    print(f"✓ Found {len(insights['technology_focus'])} technology mentions")
    print(f"✓ Analyzed {len(insights['market_insights'])} market insights")
    
    return insights

def save_insights_json(insights, output_path):
    """Save insights to JSON file"""
    print(f"\n💾 Saving insights to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(insights, f, indent=2)
    print("✓ Insights saved successfully")

# Run Phase 1: Initial extraction
if __name__ == "__main__":
    pdf_path = "/vercel/sandbox/uploads/NVIDIAAn.pdf"
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    
    # Analyze data
    insights = analyze_nvidia_data(text)
    
    # Save to JSON
    save_insights_json(insights, "/vercel/sandbox/nvidia_insights.json")
    
    print("\n" + "="*60)
    print("📊 PHASE 1 COMPLETE: Data Extraction")
    print("="*60)
    print(f"Next: Run visualization generation")
