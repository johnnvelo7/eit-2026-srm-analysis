#!/usr/bin/env python3
"""
Script 3: Generate SRM Analysis Report
=======================================
Creates interactive HTML report with matrix/heatmap visualization.

Usage:
    python scripts/3_generate_report.py

Inputs:
    - data/raw/srm_company_research.json
    - data/raw/srm_analysis.json

Output:
    - outputs/reports/srm_analysis_report.html

Dependencies:
    pip install jinja2
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Configuration
RESEARCH_FILE = Path("data/raw/srm_company_research.json")
SRM_CATEGORIES_FILE = Path("data/raw/srm_analysis.json")
OUTPUT_FILE = Path("outputs/reports/srm_analysis_report.html")

# SRM Category mapping to matrix columns
SRM_CATEGORY_MAP = {
    "Recycled aggregate": "construction",
    "Reclaimed asphalt pavement (RAP)": "construction",
    "Steel scrap": "metal",
    "Recycled steel scrap": "metal",
    "Aluminum scrap": "metal",
    "Copper scrap": "metal",
    "Nickel-bearing scrap": "metal",
    "Cobalt-bearing scrap": "metal",
    "Metal scrap": "metal",
    "Recycled polymer pellets": "plastic",
    "Sorted plastic waste": "plastic",
    "Recycled EPS": "plastic",
    "Wood chips / fiber": "wood",
    "Recovered timber": "wood",
    "Biomass fuel": "biomass",
    "Biomass pellets": "biomass",
    "Bio-oils": "biomass",
    "Biogas": "biogas",
    "Digestate": "digestate",
    "Digestate (biofertilizer)": "digestate"
}

def calculate_srm_intensity(srm_types: List[str], quantitative_data: str) -> Dict[str, int]:
    """
    Calculate SRM usage intensity for each category

    Returns dict with intensity levels (0=none, 1=low, 2=medium-high, 3=core)
    """
    intensity = {
        "construction": 0,
        "metal": 0,
        "plastic": 0,
        "wood": 0,
        "biomass": 0,
        "biogas": 0,
        "digestate": 0
    }

    for srm in srm_types:
        category = SRM_CATEGORY_MAP.get(srm)
        if category:
            # Simple heuristic: check quantitative data for intensity
            if "100%" in quantitative_data or "Core" in quantitative_data:
                intensity[category] = max(intensity[category], 3)
            elif any(x in quantitative_data for x in ["75%", "70%", "target", "high"]):
                intensity[category] = max(intensity[category], 2)
            elif srm in quantitative_data or category in quantitative_data:
                intensity[category] = max(intensity[category], 2)
            else:
                intensity[category] = max(intensity[category], 1)

    return intensity

def generate_html_report(companies: List[Dict]) -> str:
    """
    Generate HTML report with embedded JavaScript for visualizations

    Uses the template from srm_analysis_report.html
    """
    # Read the template HTML
    template_file = Path(__file__).parent.parent / "srm_analysis_report.html"

    if template_file.exists():
        with open(template_file, "r", encoding="utf-8") as f:
            html_template = f.read()

        # Replace company data in the JavaScript section
        companies_json = json.dumps(companies, indent=8, ensure_ascii=False)
        # This is a simple replacement - for production, use Jinja2 templating
        html_content = html_template.replace(
            "const companies = [",
            f"const companies = {companies_json.split('[', 1)[1]}"
        )

        return html_content
    else:
        # Fallback: generate basic HTML
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>SRM Analysis Report</title>
</head>
<body>
    <h1>SRM Analysis Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <p>Companies analyzed: {len(companies)}</p>
    <pre>{json.dumps(companies, indent=2)}</pre>
</body>
</html>"""

def main():
    """Main execution function"""
    print("=" * 60)
    print("EiT 2026: Generate SRM Analysis Report")
    print("=" * 60)
    print()

    # Load research data
    if not RESEARCH_FILE.exists():
        print(f"❌ Error: {RESEARCH_FILE} not found")
        print("   Run script 2 first to generate research data")
        return

    with open(RESEARCH_FILE, "r", encoding="utf-8") as f:
        research_data = json.load(f)

    companies = research_data["companies"]
    print(f"Loaded {len(companies)} companies from research data")

    # Calculate SRM intensity for each company
    for company in companies:
        srm_types = company.get("srm_types_used", [])
        quantitative = company.get("quantitative_data", "")
        company["srm_intensity"] = calculate_srm_intensity(srm_types, quantitative)

    print("Calculated SRM intensities for all companies")

    # Generate HTML report
    html_content = generate_html_report(companies)

    # Save report
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n✓ Report generated: {OUTPUT_FILE}")
    print(f"  File size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
    print(f"\nOpen report in browser:")
    print(f"  firefox {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
