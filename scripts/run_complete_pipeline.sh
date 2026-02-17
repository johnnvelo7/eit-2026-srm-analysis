#!/bin/bash
# ==============================================================================
# EiT 2026: Complete SRM Analysis Pipeline
# ==============================================================================
# This script runs the complete analysis pipeline from start to finish.
#
# Usage:
#   bash scripts/run_complete_pipeline.sh
#
# Steps:
#   1. Scrape companies from Brønnøysundregistrene
#   2. Prompt for research (manual step with Claude)
#   3. Generate HTML report
#   4. Open report in browser
# ==============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check prerequisites
print_header "Checking Prerequisites"

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found. Please install Python 3.8+"
    exit 1
fi
print_success "Python 3 found"

if ! python3 -c "import requests" &> /dev/null; then
    print_warning "requests library not found. Installing..."
    pip install requests pandas
fi
print_success "Python dependencies OK"

# Step 1: Scrape Companies
print_header "Step 1: Scraping Companies by NACE Code"

if [ -f "data/raw/companies_by_nace.json" ]; then
    read -p "companies_by_nace.json already exists. Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Skipping scraping, using existing data"
    else
        python3 scripts/1_scrape_companies.py
        print_success "Company scraping complete"
    fi
else
    python3 scripts/1_scrape_companies.py
    print_success "Company scraping complete"
fi

# Step 2: Research SRM Usage
print_header "Step 2: Researching SRM Usage (Manual Step)"

if [ ! -f "data/raw/srm_company_research.json" ]; then
    echo ""
    print_warning "Research data not found!"
    echo ""
    echo "You need to research SRM usage for companies using Claude Code."
    echo ""
    echo "Ask Claude:"
    echo "-----------------------------------------------------------"
    echo "Research SRM usage for companies in data/raw/companies_by_nace.json"
    echo ""
    echo "For each company, find:"
    echo "  - Annual report (2024/2023)"
    echo "  - Sustainability report"
    echo "  - SRM types used"
    echo "  - Quantitative data"
    echo "  - Sources"
    echo ""
    echo "Save to data/raw/srm_company_research.json"
    echo "-----------------------------------------------------------"
    echo ""
    read -p "Press Enter when research is complete and file is saved..."

    if [ ! -f "data/raw/srm_company_research.json" ]; then
        print_error "Research file still not found. Exiting."
        exit 1
    fi
fi

print_success "Research data found"

# Step 3: Generate Report
print_header "Step 3: Generating HTML Report"

python3 scripts/3_generate_report.py
print_success "Report generated"

# Step 4: Open Report
print_header "Step 4: Opening Report"

REPORT_PATH="outputs/reports/srm_analysis_report.html"

if [ -f "$REPORT_PATH" ]; then
    if command -v firefox &> /dev/null; then
        firefox "$REPORT_PATH" &
        print_success "Opened report in Firefox"
    elif command -v google-chrome &> /dev/null; then
        google-chrome "$REPORT_PATH" &
        print_success "Opened report in Chrome"
    else
        print_warning "No browser found. Open manually:"
        echo "  firefox $REPORT_PATH"
    fi
else
    print_error "Report file not found at $REPORT_PATH"
    exit 1
fi

# Summary
print_header "Pipeline Complete!"

echo ""
echo "Summary:"
echo "  Companies scraped:    $(jq '.companies_by_nace | to_entries | length' data/raw/companies_by_nace.json)"
echo "  Companies researched: $(jq '.companies | length' data/raw/srm_company_research.json)"
echo "  Report location:      $REPORT_PATH"
echo ""
echo "Next steps:"
echo "  - Review the report"
echo "  - Add more companies if needed"
echo "  - Refine research data"
echo "  - Export findings for Sirk Report"
echo ""
print_success "All done!"
