#!/usr/bin/env python3
"""
Script 1: Scrape Companies by NACE Code
========================================
Scrapes Norwegian companies from Brønnøysundregistrene API by NACE codes.

Usage:
    python scripts/1_scrape_companies.py

Output:
    - data/raw/companies_by_nace.json
    - data/processed/companies_list.csv

Dependencies:
    pip install requests pandas
"""

import json
import requests
import time
from pathlib import Path
import pandas as pd
from typing import List, Dict

# Configuration
OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NACE codes to scrape (from mappings.csv)
NACE_CODES = [
    "23.51", "23.63", "23.61", "23.99",  # Construction materials
    "42.11", "42.99",  # Construction/Road building
    "24.10", "24.42", "24.45", "24.51", "24.52", "24.53", "24.54",  # Metals
    "22.22", "22.29", "38.32",  # Plastics & Recovery
    "16.21", "16.10",  # Wood
    "35.11", "35.30", "35.21",  # Energy
    "20.15", "01.11"  # Fertilizers & Agriculture
]

def scrape_companies_by_nace(nace_code: str, top_n: int = 5) -> List[Dict]:
    """
    Scrape companies from Brønnøysundregistrene API for a given NACE code

    Args:
        nace_code: NACE industry code (e.g., "23.51")
        top_n: Number of top companies to retrieve

    Returns:
        List of company dictionaries
    """
    # Convert NACE code format (23.51 -> 23.510)
    nace_formatted = nace_code.replace(".", "") + "0" if len(nace_code.split(".")[1]) == 2 else nace_code.replace(".", "")

    print(f"Scraping NACE {nace_code} ({nace_formatted})...")

    # Brønnøysundregistrene API endpoint
    url = "https://data.brreg.no/enhetsregisteret/api/enheter"

    params = {
        "naeringskode": nace_formatted,
        "size": top_n * 3  # Get more to account for filtering
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        companies = []

        for unit in data.get("_embedded", {}).get("enheter", [])[:top_n]:
            company = {
                "name": unit.get("navn"),
                "org_number": unit.get("organisasjonsnummer"),
                "nace_code": nace_code,
                "nace_description": unit.get("naeringskode1", {}).get("beskrivelse"),
                "revenue": None,  # Not available from API
                "employees": unit.get("antallAnsatte"),
                "location": unit.get("forretningsadresse", {}).get("poststed"),
                "description": unit.get("hjemmeside"),
                "municipality": unit.get("forretningsadresse", {}).get("kommune"),
                "postal_place": unit.get("forretningsadresse", {}).get("poststed"),
                "registration_date": unit.get("registreringsdatoEnhetsregisteret"),
                "organizational_form": unit.get("organisasjonsform", {}).get("beskrivelse")
            }
            companies.append(company)

        print(f"  Found {len(companies)} companies")
        time.sleep(0.5)  # Rate limiting
        return companies

    except requests.exceptions.RequestException as e:
        print(f"  Error scraping {nace_code}: {e}")
        return []

def main():
    """Main execution function"""
    print("=" * 60)
    print("EiT 2026: Company Scraping by NACE Code")
    print("=" * 60)
    print()

    all_companies = {}

    for nace_code in NACE_CODES:
        companies = scrape_companies_by_nace(nace_code)
        all_companies[nace_code] = companies

    # Save to JSON
    output_file = OUTPUT_DIR / "companies_by_nace.json"
    result = {
        "scrape_date": "2026-02-11",
        "source": "Brønnøysundregistrene API (data.brreg.no)",
        "note": "Revenue data not available from Brreg API. Employee count used as size proxy.",
        "companies_by_nace": all_companies
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Saved to {output_file}")

    # Create CSV for easy viewing
    csv_data = []
    for nace, companies in all_companies.items():
        for company in companies:
            row = company.copy()
            csv_data.append(row)

    df = pd.DataFrame(csv_data)
    csv_file = Path("data/processed/companies_list.csv")
    csv_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_file, index=False)

    print(f"✓ Saved CSV to {csv_file}")
    print(f"\nTotal companies scraped: {len(csv_data)}")
    print(f"NACE codes covered: {len(all_companies)}")

if __name__ == "__main__":
    main()
