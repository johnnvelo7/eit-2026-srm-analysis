# Setup Guide - GitHub Repository

## Quick Setup

### 1. Initialize Git Repository

```bash
# Navigate to the project directory
cd eit-2026-srm-analysis

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: EiT 2026 SRM Analysis"
```

### 2. Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click "New Repository"
3. Name it: `eit-2026-srm-analysis`
4. **Don't** initialize with README (we already have one)
5. Click "Create Repository"

### 3. Push to GitHub

```bash
# Add remote (replace 'johnnvelo7' with your GitHub username if forked)
git remote add origin https://github.com/johnnvelo7/eit-2026-srm-analysis.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Updating the Report

### When you update data or generate new reports:

```bash
# Navigate to the project root
cd eit-2026-srm-analysis

# Generate new report
python scripts/3_generate_report.py

# Commit and push
git add .
git commit -m "Update: [describe your changes]"
git push
```

---

## Update the README

The README.md links are already set to the correct repository URL.

---

## Customize the Report

### To customize `index.html`:

1. Edit colors in the `<style>` section
2. Update header text
3. Add your team members' names
4. Modify the data visualizations

Then commit and push changes.

---

## Adding More Data

### To add more companies:

1. Add NACE codes to `scripts/1_scrape_companies.py`
2. Run the scraper: `python scripts/1_scrape_companies.py`
3. Research SRM usage and update `data/raw/srm_company_research.json`
4. Regenerate report: `python scripts/3_generate_report.py`

```bash
git add .
git commit -m "Add: [X] new companies from [sector]"
git push
```

---

## Privacy Considerations

### Current setup includes:
- All company data (public information)
- Scripts and methodology
- Generated reports

### Consider removing if sensitive:
- Personal notes or internal communications
- Draft versions of reports
- Any data not intended for public view

To remove files from git:
```bash
git rm --cached [filename]
git commit -m "Remove file"
git push
```

---

## Troubleshooting

### "Permission denied" when pushing
```bash
# Use personal access token instead of password
# Create token at: GitHub -> Settings -> Developer settings -> Personal access tokens
```

### "Data files too large"
- GitHub has 100MB file size limit
- Consider compressing large JSON files
- Or use Git LFS for large files

---

## Support

For issues with:
- **Git/GitHub:** See [GitHub Docs](https://docs.github.com)
- **Project Data:** Contact EiT team

---

**Ready to go!**

After following these steps, your project will be:
- Versioned with Git
- Hosted on GitHub
- Shareable with a public URL
