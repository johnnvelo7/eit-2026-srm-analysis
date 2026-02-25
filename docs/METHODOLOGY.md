# Methodology - SRM Analysis

## Research Approach

### 1. Company Identification

**Source:** [Bronnoysundregistrene API](https://data.brreg.no/enhetsregisteret/api/enheter)

Companies were identified by querying the Norwegian Business Register for relevant NACE industry codes covering sectors where secondary raw material usage is expected (construction, metals, plastics, paper, energy, chemicals, etc.).

**Selection criteria:**
- Active Norwegian companies in relevant NACE codes
- Prioritized by employee count and industry relevance
- 109 companies selected across multiple sectors

### 2. Data Enrichment

Each company was cross-referenced against multiple public sources:

| Source | Data Extracted |
|--------|---------------|
| Bronnoysundregistrene | Org number, NACE codes, registration |
| Proff.no | Revenue, employee count, legal name |
| Norske Utslipp | Environmental permits, emission data |
| Company websites | Homepage URL, descriptions |

### 3. SRM Assessment

**Sources (priority order):**
1. Company sustainability reports (2023-2024, CSRD/ESRS where available)
2. Annual reports (2023-2024)
3. Environmental Product Declarations (EPDs)
4. Company websites and press releases
5. Industry publications

**Method:** AI-assisted analysis of source documents with manual verification. Each identified SRM input was:
- Classified into one of 13 MECE categories (A1-A10 material, B1-B3 energy)
- Assigned a tier (T0-T3) based on evidence strength and scale
- Documented with evidence snippets linking back to source documents
- Quantified where data was available (tonnes, MWh, percentages)

### 4. MECE Classification System

**13 mutually exclusive, collectively exhaustive categories:**

**Material Inputs (A1-A10):**
- A1: Mineral & Construction Materials
- A2: Industrial Mineral By-Products
- A3: Metals - Ferrous & Non-Ferrous Scrap
- A4: Plastics - Reprocessed Polymers
- A5: Glass & Ceramics
- A6: Paper & Cardboard Fibres
- A7: Textiles & Fibres
- A8: Rubber & Tyres
- A9: Bio-Based Material Residues (non-energy)
- A10: Chemical & Liquid Feedstocks

**Energy Inputs (B1-B3):**
- B1: Solid Recovered Fuel (SRF/RDF)
- B2: Biomass Fuels
- B3: Biogas

### 5. Tier Assignment

| Tier | Criteria |
|------|----------|
| T3 - Core | SRM is a primary/significant input with strong quantitative evidence |
| T2 - Meaningful | Documented non-trivial usage with some quantitative data |
| T1 - Minor | Mentioned in reports, pilot projects, or small-scale use |
| T0 - No evidence | Company assessed but no SRM usage found in available sources |
| N/D - No data | Company not yet assessed (included in dataset for completeness) |

### 6. Data Validation

**Cross-checking:**
- Sustainability reports vs annual reports
- Company claims vs environmental permits (Norske Utslipp)
- Parent company data vs subsidiary-specific data
- Multiple source documents per company where available

---

## Limitations

- 43 of 109 companies have not yet been fully assessed (N/D status)
- Revenue data availability varies
- Smaller companies often lack public sustainability reports
- Quantitative data specificity varies between companies
- Some companies report group-wide figures rather than Norway-specific
- AI-assisted analysis may miss nuances in source documents

## Future Work

- Complete assessments for remaining N/D companies
- Direct company surveys for missing quantitative data
- Time-series analysis of SRM adoption trends
- Integration with additional data sources (EU databases, industry associations)

---

*Last updated: February 25, 2026*
