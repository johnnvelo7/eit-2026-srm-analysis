# Secondary Raw Materials in Norwegian Industry

**EiT 2026 | Sirk Norge | NTNU Experts in Teams**

[![Live Site](https://img.shields.io/badge/Live-eitsrm.no-2563eb?style=for-the-badge)](https://www.eitsrm.no/)
[![Companies](https://img.shields.io/badge/Companies-109-059669?style=flat-square)](aggregated.json)
[![Categories](https://img.shields.io/badge/SRM_Categories-13-0891b2?style=flat-square)](aggregated.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-d97706?style=flat-square)](LICENSE)

---

## About

This project maps **secondary raw material (SRM)** usage across **109 Norwegian industrial companies** to understand circular economy activity. SRMs are recycled or recovered materials and energy sources used as inputs in industrial production - such as metal scrap, recycled plastics, biomass fuels, and biogas.

The analysis was conducted as part of the **Experts in Teams (EiT) 2026** course at NTNU, in collaboration with **Sirk Norge**.

---

## Live Website

**[https://www.eitsrm.no/](https://www.eitsrm.no/)**

The website consists of three pages:

| Page | Description |
|------|-------------|
| **Dashboard** (`index.html`) | Overview with heatmap matrix, company cards, charts, and key findings |
| **Company Viewer** (`viewer.html`) | Sortable, searchable table with click-to-expand detail panels |
| **SRM Analytics** (`analytics.html`) | Input-level analysis with quantity rollups and category filters |

Each page has a **"How to use"** guide at the top explaining how to interpret the data.

---

## SRM Classification (MECE)

Companies are assessed against **13 mutually exclusive categories** covering material and energy inputs:

### Material Inputs (A1-A10)
| Code | Category | Examples |
|------|----------|----------|
| A1 | Mineral & Construction Materials | Recycled aggregates, reclaimed asphalt |
| A2 | Industrial Mineral By-Products | Slag, fly ash, silica fume |
| A3 | Metals Scrap | Steel scrap, aluminium scrap |
| A4 | Reprocessed Plastics | Recycled polymer pellets, regranulate |
| A5 | Glass & Ceramics | Cullet, recycled refractory material |
| A6 | Paper & Cardboard Fibres | Recovered paper, recycled pulp |
| A7 | Textiles & Fibres | Recovered textile fibres |
| A8 | Rubber & Tyres | Crumb rubber, devulcanised rubber |
| A9 | Bio-Based Residues (Material) | Wood chips, sawdust, digestate |
| A10 | Chemical & Liquid Feedstocks | Recovered solvents, recycled oils |

### Energy Inputs (B1-B3)
| Code | Category | Examples |
|------|----------|----------|
| B1 | SRF / RDF | Solid recovered fuel, refuse-derived fuel |
| B2 | Biomass Fuels | Wood pellets, bio-oil |
| B3 | Biogas | Biogas, biomethane |

---

## Tier System

Each company receives an overall tier and per-category tier:

| Tier | Meaning | Description |
|------|---------|-------------|
| **T3** | Core / Significant | SRM use is a major part of operations |
| **T2** | Meaningful | Documented, non-trivial SRM usage |
| **T1** | Minor / Pilot | Small-scale or pilot-stage use |
| **T0** | No evidence | Assessed, but no SRM use found |
| **N/D** | No data | Not yet assessed |

---

## Running Locally

No build step required. Clone and open in a browser:

```bash
git clone https://github.com/johnnvelo7/eit-2026-srm-analysis.git
cd eit-2026-srm-analysis

# Open in your browser
open index.html        # macOS
xdg-open index.html    # Linux
start index.html       # Windows
```

Or serve with any static file server:

```bash
python3 -m http.server 8000
# Then visit http://localhost:8000
```

All data is included in `aggregated.json` - no external API calls or dependencies needed.

---

## Repository Structure

```
eit-2026-srm-analysis/
├── index.html              # Dashboard - main page
├── viewer.html             # Company Viewer - sortable table
├── analytics.html          # SRM Analytics - input-level data
├── aggregated.json         # Dataset (109 companies, all SRM assessments)
├── data/
│   ├── raw/                # Raw data from APIs and research
│   ├── processed/          # Processed CSVs (company lists, NACE codes)
│   └── new files/          # Per-company assessment outputs
├── docs/
│   └── METHODOLOGY.md      # Research methodology
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## Data Sources

| Source | Usage |
|--------|-------|
| [Bronnoysundregistrene](https://data.brreg.no) | Company registry, org numbers, NACE codes |
| [Proff.no](https://www.proff.no) | Revenue, employees, company details |
| [Norske Utslipp](https://www.norskeutslipp.no) | Environmental permits |
| Company sustainability reports | SRM usage evidence, quantities |
| Company annual reports | Financial and operational data |
| EPDs (Environmental Product Declarations) | Material composition data |

---

## Methodology

1. **Company identification** - Scraped from Bronnoysundregistrene by relevant NACE codes
2. **Data enrichment** - Cross-referenced with Proff.no, Norske Utslipp, and company websites
3. **SRM assessment** - AI-assisted analysis of sustainability reports, annual reports, and EPDs with manual verification
4. **Classification** - Each SRM input categorized into the 13 MECE categories and assigned a tier (T0-T3)
5. **Aggregation** - All assessments compiled into `aggregated.json` for the web interface

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for full details.

---

## License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.

**Data attribution:**
- Company registry data: Bronnoysundregistrene (Norwegian Business Register)
- Annual/sustainability reports: Property of respective companies
- Analysis and visualizations: EiT 2026 Team for Sirk Norge

---

## Team

**EiT 2026 Team** - NTNU Experts in Teams
**Project Sponsor:** Sirk Norge
**Course:** Experts in Teams (EiT), NTNU Spring 2026

---

## Links

- [Live Website](https://www.eitsrm.no/)
- [Sirk Norge](https://www.sirknorge.no/)
- [NTNU EiT](https://www.ntnu.edu/eit)
- [Bronnoysundregistrene](https://www.brreg.no/)

---

*Last updated: February 25, 2026*
