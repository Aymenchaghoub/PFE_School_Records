# 📥 PDF Documentation Export

This folder contains the exported PDF documentation for the School Records Management System.

---

## 📄 Available PDFs

### School_Records_Management_Documentation.pdf
**Status**: 🔄 Generation Pending

**Contents**:
1. Cover Page (Title, Author, Date)
2. Table of Contents
3. Project Overview
4. Architecture Guide
5. Tech Stack Details
6. API Reference
7. Deployment Guide

**Size**: ~50-80 pages  
**Theme**: Violet (#6A1B9A) accents

---

## 🛠️ How to Generate PDF

### Method 1: Using Pandoc (Recommended)

**Install Pandoc**:
```bash
# Windows (via Chocolatey)
choco install pandoc

# Mac
brew install pandoc

# Or download from: https://pandoc.org/installing.html
```

**Generate PDF**:
```bash
# Navigate to project root
cd c:/Users/Aymen/Desktop/PFE

# Combine all markdown files and convert to PDF
pandoc docs/README_FINAL.md docs/ARCHITECTURE.md docs/TECH_STACK.md docs/API_REFERENCE.md DEPLOYMENT.md -o docs/exports/School_Records_Management_Documentation.pdf --pdf-engine=xelatex -V geometry:margin=1in -V colorlinks=true -V linkcolor=violet -V urlcolor=violet -V toccolor=violet --toc --toc-depth=2 --metadata title="School Records Management System" --metadata author="Aymen Chaghoub" --metadata date="November 2025"
```

### Method 2: Using Markdown to PDF Tools

**VS Code Extensions**:
- **Markdown PDF** by yzane
  1. Install extension
  2. Open each markdown file
  3. Right-click → "Markdown PDF: Export (pdf)"
  4. Manually combine PDFs

**Online Tools**:
- **Markdown to PDF**: https://www.markdowntopdf.com
- **Dillinger**: https://dillinger.io (export as PDF)

### Method 3: Using Node.js (md-to-pdf)

```bash
# Install globally
npm install -g md-to-pdf

# Generate PDF
md-to-pdf docs/README_FINAL.md --pdf-options '{"format":"A4","margin":"20mm"}' --stylesheet style.css
```

### Method 4: Using Python (markdown2pdf)

```bash
# Install
pip install markdown2pdf

# Generate
python -m markdown2pdf docs/README_FINAL.md -o docs/exports/Documentation.pdf
```

---

## 🎨 Custom Styling (Optional)

Create `pdf-style.css` for custom PDF styling:

```css
/* pdf-style.css */
@page {
  margin: 2cm;
}

body {
  font-family: 'Arial', 'Helvetica', sans-serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #333;
}

h1 {
  color: #6A1B9A;
  font-size: 28pt;
  margin-top: 1.5em;
  border-bottom: 3px solid #6A1B9A;
  padding-bottom: 0.3em;
}

h2 {
  color: #6A1B9A;
  font-size: 20pt;
  margin-top: 1.2em;
}

h3 {
  color: #8E24AA;
  font-size: 16pt;
  margin-top: 1em;
}

code {
  background-color: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 10pt;
}

pre {
  background-color: #f5f5f5;
  padding: 12px;
  border-left: 4px solid #6A1B9A;
  overflow-x: auto;
}

a {
  color: #6A1B9A;
  text-decoration: none;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

th {
  background-color: #6A1B9A;
  color: white;
  padding: 10px;
  text-align: left;
}

td {
  border: 1px solid #ddd;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

blockquote {
  border-left: 4px solid #6A1B9A;
  padding-left: 1em;
  color: #666;
  font-style: italic;
}
```

Use with Pandoc:
```bash
pandoc docs/README_FINAL.md -o docs/exports/Documentation.pdf --pdf-engine=xelatex --css=pdf-style.css
```

---

## 📋 Checklist

Before generating PDF:
- [ ] All markdown files updated
- [ ] Images/screenshots added
- [ ] Code blocks formatted correctly
- [ ] Tables render properly
- [ ] Links are functional
- [ ] Table of contents generated
- [ ] Cover page included
- [ ] Page numbers added
- [ ] Violet theme applied

---

## 🔍 Quality Check

After generating PDF:
- [ ] Open PDF and verify all pages
- [ ] Check table of contents navigation
- [ ] Verify images display correctly
- [ ] Test internal links
- [ ] Check code blocks are readable
- [ ] Verify tables fit on pages
- [ ] Ensure proper page breaks
- [ ] Check header/footer formatting
- [ ] File size reasonable (<10MB)

---

## 📤 Alternative: Pre-generated PDF

If you're unable to generate the PDF, you can:

1. **Use GitHub Actions**: Set up automated PDF generation
2. **Request from Author**: Contact for pre-generated PDF
3. **Use Cloud Service**: Upload markdown to cloud PDF converters

---

## 🚀 Quick Generate (PowerShell Script)

Save as `generate-pdf.ps1`:

```powershell
#!/usr/bin/env pwsh
# PDF Generation Script

Write-Host "📄 Generating PDF Documentation..." -ForegroundColor Cyan

# Check if pandoc is installed
if (!(Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Pandoc not found. Please install: choco install pandoc" -ForegroundColor Red
    exit 1
}

# Files to include
$files = @(
    "docs/README_FINAL.md",
    "docs/ARCHITECTURE.md",
    "docs/TECH_STACK.md",
    "docs/API_REFERENCE.md",
    "DEPLOYMENT.md"
)

# Output file
$output = "docs/exports/School_Records_Management_Documentation.pdf"

# Generate PDF
Write-Host "🔄 Converting markdown to PDF..." -ForegroundColor Yellow

pandoc $files `
    -o $output `
    --pdf-engine=xelatex `
    -V geometry:margin=1in `
    -V colorlinks=true `
    -V linkcolor=violet `
    -V urlcolor=violet `
    -V toccolor=violet `
    --toc `
    --toc-depth=2 `
    --metadata title="School Records Management System - Complete Documentation" `
    --metadata author="Aymen Chaghoub" `
    --metadata date="November 2025"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ PDF generated successfully!" -ForegroundColor Green
    Write-Host "📄 Location: $output" -ForegroundColor Cyan
    
    # Open PDF
    Start-Process $output
} else {
    Write-Host "❌ PDF generation failed" -ForegroundColor Red
    exit 1
}
```

Run:
```powershell
.\generate-pdf.ps1
```

---

**Last Updated**: November 2025  
**Status**: 📋 Instructions Complete - PDF Generation Pending
