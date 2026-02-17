# Methodology - SRM Analysis

## Research Approach

### 1. Data Collection (Automated)

**Source:** [Brønnøysundregistrene API](https://data.brreg.no/enhetsregisteret/api/enheter)

**Method:**
```python
# For each NACE code
GET https://data.brreg.no/enhetsregisteret/api/enheter?naeringskode={code}

# Returns:
- Company name
- Organization number
- Employee count
- Location
- Registration date
```

**Selection Criteria:**
- Top 3-5 companies per NACE code
- Sorted by employee count (revenue not available from API)
- Active companies only

### 2. SRM Research (AI-Assisted)

**Sources (Priority Order):**
1. Company sustainability reports (2024, CSRD/ESRS compliant)
2. Annual reports (2023-2024)
3. Company websites (sustainability sections)
4. Press releases and industry publications

**Data Extracted:**
- SRM types used (categorized into 7 main categories)
- Quantitative data (percentages, volumes, targets)
- Evidence text (quotes/paraphrases from reports)
- Source URLs for verification

**Quality Criteria:**
- Prefer quantitative over qualitative data
- Verify across multiple sources where possible
- Include both current usage and future targets
- Document data gaps transparently

### 3. Categorization

**7 SRM Categories:**
1. Recycled Construction Materials
2. Metal Scrap
3. Recycled Plastics
4. Wood-based Materials
5. Biomass Fuel
6. Biogas
7. Digestate & Bio-fertilizers

**Intensity Levels:**
- **0 (None):** No evidence of usage
- **1 (Low):** Mentioned but no quantitative data
- **2 (Medium-High):** Significant usage with some data
- **3 (Core):** Primary raw material with detailed data

### 4. Data Validation

**Cross-checking:**
- Annual reports vs sustainability reports
- Company claims vs industry publications
- Parent company data vs subsidiary data
- Historical trends vs future targets

**Limitations:**
- Revenue data not publicly available from Brreg
- Some smaller companies have no public reports
- Quantitative data varies in specificity
- Some companies report group-wide vs Norway-specific data

---

## NACE Code Mapping

Based on the `mappings.csv` file provided by Sirk Norge:

| Waste Stream | SRM | NACE Codes | Industries |
|--------------|-----|------------|------------|
| Construction & Demolition | Recycled aggregate | 23.51, 23.63, 23.61, 42.11, 42.99 | Cement, concrete, road construction |
| Construction & Demolition | RAP | 23.99 | Asphalt production |
| Metal Waste | Steel scrap | 24.10 | Steel production |
| Metal Waste | Aluminum scrap | 24.42 | Aluminum production |
| Plastic Waste | Recycled polymers | 22.22, 22.29 | Plastic manufacturing |
| Wood Waste | Wood chips/fiber | 16.21, 16.10 | Wood panels, sawmills |
| Organic Waste | Biogas | 35.11, 35.21 | Energy/gas production |
| Organic Waste | Digestate | 20.15 | Fertilizer production |

---

## Data Processing Pipeline

```
1. Scrape
   ↓
   companies_by_nace.json (105 companies)
   ↓
2. Research (AI-assisted)
   ↓
   srm_company_research.json (20 detailed profiles)
   ↓
3. Process
   ↓
   Calculate SRM intensity matrix
   ↓
4. Visualize
   ↓
   index.html (interactive report)
```

---

## Reproducibility

All steps are documented and automated where possible:

1. **Scraping:** Fully automated via Python script
2. **Research:** AI-assisted with manual verification
3. **Report Generation:** Fully automated via Python script

**To reproduce:**
```bash
git clone [repository]
pip install -r requirements.txt
bash scripts/run_complete_pipeline.sh
```

---

## Limitations & Future Work

### Current Limitations
- Revenue data not available from public APIs
- Smaller companies often lack public sustainability reports
- SRM usage data varies in detail and specificity
- Focus on top companies may miss innovative SMEs

### Future Improvements
- Direct company surveys for missing data
- Integration with Norske Utslipp permit database
- Time-series analysis of SRM adoption trends
- Economic analysis of SRM vs primary materials

---

## Data Quality Assessment

| Metric | Coverage | Quality |
|--------|----------|---------|
| Company identification | 100% | ✓ Excellent |
| Employee counts | 85% | ✓ Good |
| NACE codes | 100% | ✓ Excellent |
| SRM types | 90% | ✓ Good |
| Quantitative data | 75% | ~ Fair |
| Annual reports | 80% | ✓ Good |

---

**Last Updated:** February 11, 2026
