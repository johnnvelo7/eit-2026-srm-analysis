# 🔄 Secondary Raw Materials in Norwegian Industry

**EiT 2026 Project | Sirk Norge | NTNU Experts in Teams**

[![View Report](https://img.shields.io/badge/View-Interactive_Report-blue?style=for-the-badge)](https://johnnvelo7.github.io/eit-2026-srm-analysis/)
[![Data](https://img.shields.io/badge/Companies-105-green?style=flat-square)](data/raw/companies_by_nace.json)
[![NACE Codes](https://img.shields.io/badge/NACE_Codes-23-orange?style=flat-square)](data/processed/companies_list.csv)

---

## 📊 Project Overview

This project maps **secondary raw materials (SRM)** usage across Norwegian industrial companies to understand circular economy practices and identify opportunities for increased recycling and material recovery.

**Key Findings:**
- 🏭 **105 companies** analyzed across 23 NACE industry codes
- ♻️ **7 SRM categories** identified and mapped
- 📈 **770,000 tonnes/year** steel scrap recycling (7 Steel Nordic)
- 🔋 **451,000 tonnes/year** aluminum scrap (Hydro Aluminium, target 1.2M by 2030)
- ⚡ **350,000 tonnes/year** waste-to-energy conversion (Hafslund Celsio)

---

## 🌐 Interactive Report

**[View the Interactive Report →](https://johnnvelo7.github.io/eit-2026-srm-analysis/)**

The report includes:
- 📊 Company-to-SRM Matrix/Heatmap
- 🏢 Detailed Company Profiles with SRM Usage
- 📈 Data Visualizations & Charts
- 🔗 Source Links to Annual Reports

---

## 🗂️ Data Structure

### Secondary Raw Material Categories

1. **Recycled Construction Materials**
   - Recycled aggregate, Reclaimed asphalt pavement (RAP)

2. **Metal Scrap**
   - Steel, aluminum, copper, nickel/cobalt scrap

3. **Recycled Plastics**
   - Polymer pellets, EPS (Expanded Polystyrene)

4. **Wood-based Materials**
   - Wood chips, recovered timber

5. **Biomass Fuel**
   - Pellets, bio-oils, biogenic waste

6. **Biogas**
   - From organic waste, manure, food waste

7. **Digestate & Bio-fertilizers**
   - Biogas production residue

### Industries Covered (NACE Codes)

| Sector | NACE Codes | Companies |
|--------|-----------|-----------|
| Construction Materials | 23.51, 23.63, 23.61, 23.99 | 19 |
| Road Construction | 42.11, 42.99 | 10 |
| Metals | 24.10, 24.42, 24.45, 24.51-54 | 30 |
| Plastics & Recovery | 22.22, 22.29, 38.32 | 10 |
| Wood | 16.21, 16.10 | 7 |
| Energy | 35.11, 35.30, 35.21 | 18 |
| Fertilizers & Agriculture | 20.15, 01.11 | 11 |

---

## 🚀 Quick Start

### View the Report Locally

```bash
# Clone the repository
git clone https://github.com/johnnvelo7/eit-2026-srm-analysis.git
cd eit-2026-srm-analysis

# Open the report in your browser
firefox index.html
# or
open index.html  # macOS
```

### Run the Analysis Pipeline

```bash
# Install dependencies
pip install -r requirements.txt

# Run complete pipeline
bash scripts/run_complete_pipeline.sh
```

Or step-by-step:

```bash
# 1. Scrape companies from Brønnøysundregistrene
python scripts/1_scrape_companies.py

# 2. Research SRM usage (requires AI/manual research)
python scripts/2_research_srm_usage.py

# 3. Generate HTML report
python scripts/3_generate_report.py
```

---

## 📁 Repository Structure

```
eit-2026-srm-analysis/
├── index.html                  # Main interactive report
├── data/
│   ├── raw/                    # JSON data files
│   │   ├── companies_by_nace.json
│   │   └── srm_company_research.json
│   └── processed/              # CSV exports
│       └── companies_list.csv
├── scripts/                    # Python automation
│   ├── 1_scrape_companies.py
│   ├── 2_research_srm_usage.py
│   ├── 3_generate_report.py
│   └── run_complete_pipeline.sh
├── docs/                       # Documentation
│   └── methodology.md
└── README.md                   # This file
```

---

## 🔬 Methodology

### Phase 1: Data Collection
- **Source:** [Brønnøysundregistrene API](https://data.brreg.no)
- **Method:** Automated scraping by NACE code
- **Coverage:** Top 3-5 companies per sector by employee count

### Phase 2: SRM Research
- **Sources:** Annual reports, sustainability reports (CSRD/ESRS compliant)
- **Method:** AI-assisted analysis with manual verification
- **Focus:** Quantitative data on recycled material usage

### Phase 3: Visualization
- **Technology:** Interactive HTML with Chart.js
- **Features:** Matrix heatmap, company profiles, data charts

---

## 🏆 Top SRM Users

| Company | Sector | SRM Volume/Year | Type |
|---------|--------|-----------------|------|
| **7 Steel Nordic** | Steel | 770,000 tonnes | Steel scrap |
| **Hydro Aluminium** | Aluminum | 451,000 tonnes | Aluminum scrap |
| **Hafslund Celsio** | Energy | 350,000 tonnes | Waste-to-energy |
| **Alcoa Norway** | Aluminum | 20,000 tonnes | Aluminum scrap |
| **Glencore Nikkelverk** | Nickel/Cobalt | 20,000 tonnes | Battery materials |

---

## 📊 Key Statistics

- **Construction Sector:** 30-100% recycled aggregate content
- **Aluminum Sector:** 75-100% recycled content in premium products, 95% energy savings
- **Steel Sector:** 100% EAF production with renewable energy
- **Biogas Sector:** >100% emissions reduction potential
- **Plastics (EPS):** Closed-loop 100% recyclable systems

---

## 🔄 Recreating the Analysis

### Add More Companies

Edit `scripts/1_scrape_companies.py`:

```python
NACE_CODES = [
    "23.51",  # Existing codes
    "25.50",  # Add new NACE codes here
]
```

### Expand Research

```bash
# Research new sectors
# Use AI/manual research to populate srm_company_research.json

# Regenerate report
python scripts/3_generate_report.py
```

---

## 📚 Data Sources

- [Brønnøysundregistrene](https://data.brreg.no) - Company registry
- [Proff.no](https://www.proff.no) - Company information
- [Norske Utslipp](https://www.norskeutslipp.no) - Emission permits
- [SSB NACE Codes](https://www.ssb.no/klass/klassifikasjoner/6) - Industry classification
- Company annual reports (2023-2024)
- Company sustainability reports (CSRD/ESRS compliant)

---

## 🤝 Contributing

This is an academic project for EiT 2026. Contributions for data accuracy and additional companies are welcome!

1. Fork the repository
2. Add data to `data/raw/srm_company_research.json`
3. Regenerate report with `python scripts/3_generate_report.py`
4. Submit a pull request

---

## 📄 License

This project is for academic use (EiT 2026 - NTNU). Data sources are publicly available.

**Attribution:**
- Data: Brønnøysundregistrene, company annual reports
- Project: Sirk Norge & NTNU EiT 2026
- Analysis: EiT Team 2026

---

## 👥 Team

**EiT 2026 Team** - NTNU Experts in Teams
**Project Sponsor:** Sirk Norge
**Course:** EiT, NTNU Spring 2026

---

## 📧 Contact

For questions about the data or methodology, please open an issue or contact the EiT team through NTNU.

---

## 🔗 Links

- [Interactive Report](https://johnnvelo7.github.io/eit-2026-srm-analysis/)
- [Sirk Norge](https://www.sirknorge.no/)
- [NTNU EiT](https://www.ntnu.edu/eit)
- [Brønnøysundregistrene](https://www.brreg.no/)

---

**Last Updated:** February 11, 2026
**Version:** 1.0
