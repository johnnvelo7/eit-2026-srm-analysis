# Setup Guide - GitHub Upload

## 🚀 Quick Setup

### 1. Initialize Git Repository

```bash
cd /home/kali/Documents/ntnu/eit-github

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
# Add remote (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/eit-2026-srm-analysis.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🌐 Enable GitHub Pages

### Option 1: Settings (Recommended)

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under "Source", select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**
6. Wait 1-2 minutes
7. Your site will be live at: `https://yourusername.github.io/eit-2026-srm-analysis/`

### Option 2: GitHub Actions (Advanced)

If you want to use the included workflow:

1. The `.github/workflows/pages.yml` file is already included
2. GitHub will automatically detect it
3. Go to **Settings → Pages**
4. Set source to **GitHub Actions**
5. The workflow will build and deploy automatically

---

## 🔄 Updating the Report

### When you update data or generate new reports:

```bash
# Navigate to the GitHub folder
cd /home/kali/Documents/ntnu/eit-github

# Generate new report (in original folder)
cd /home/kali/Documents/ntnu/eit
python scripts/3_generate_report.py

# Copy updated report to GitHub folder
cp outputs/reports/srm_analysis_report.html /home/kali/Documents/ntnu/eit-github/index.html

# Also copy updated data if needed
cp data/raw/*.json /home/kali/Documents/ntnu/eit-github/data/raw/
cp data/processed/*.csv /home/kali/Documents/ntnu/eit-github/data/processed/

# Commit and push
cd /home/kali/Documents/ntnu/eit-github
git add .
git commit -m "Update: [describe your changes]"
git push
```

---

## 📝 Update the README

**Don't forget to update the README.md with your actual GitHub username!**

Replace `yourusername` in these places:
- Line 6: Badge link
- Line 33: Report link
- Line 82: Clone URL
- Line 195: Report link

```bash
# Quick find and replace (Linux/Mac)
sed -i 's/yourusername/your-actual-username/g' README.md
```

---

## 🎨 Customize the Report

### To customize `index.html`:

1. Edit colors in the `<style>` section
2. Update header text
3. Add your team members' names
4. Modify the data visualizations

Then commit and push changes.

---

## 📊 Adding More Data

### To add more companies:

1. **In the original folder** (`/home/kali/Documents/ntnu/eit`):
   ```bash
   # Add companies
   python scripts/1_scrape_companies.py

   # Research SRM usage (with Claude)
   # Then generate report
   python scripts/3_generate_report.py
   ```

2. **Copy to GitHub folder:**
   ```bash
   cp outputs/reports/srm_analysis_report.html /home/kali/Documents/ntnu/eit-github/index.html
   cp data/raw/*.json /home/kali/Documents/ntnu/eit-github/data/raw/
   ```

3. **Commit and push:**
   ```bash
   cd /home/kali/Documents/ntnu/eit-github
   git add .
   git commit -m "Add: [X] new companies from [sector]"
   git push
   ```

---

## 🔐 Privacy Considerations

### Current setup includes:
- ✅ All company data (public information)
- ✅ Scripts and methodology
- ✅ Generated reports

### Consider removing if sensitive:
- Personal notes or internal communications
- Draft versions of reports
- Any data not intended for public view

To remove files from git:
```bash
git rm --cached [filename]
git commit -m "Remove sensitive file"
git push
```

---

## 🐛 Troubleshooting

### "Permission denied" when pushing
```bash
# Use personal access token instead of password
# Create token at: GitHub → Settings → Developer settings → Personal access tokens
```

### "index.html not showing on GitHub Pages"
- Check that file is named exactly `index.html` (lowercase)
- Ensure GitHub Pages is enabled in repository settings
- Wait 1-2 minutes for deployment
- Check Actions tab for build errors

### "Data files too large"
- GitHub has 100MB file size limit
- Consider compressing large JSON files
- Or use Git LFS for large files

---

## 📧 Support

For issues with:
- **Git/GitHub:** See [GitHub Docs](https://docs.github.com)
- **GitHub Pages:** See [Pages Docs](https://docs.github.com/en/pages)
- **Project Data:** Contact EiT team

---

**Ready to go!** 🎉

After following these steps, your project will be:
- ✅ Versioned with Git
- ✅ Hosted on GitHub
- ✅ Live on GitHub Pages
- ✅ Shareable with a public URL
