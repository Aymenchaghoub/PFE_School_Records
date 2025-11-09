#!/usr/bin/env pwsh
# Portfolio Creation Quick-Start Script
# Creates Next.js portfolio project with all dependencies

Write-Host "🎨 Portfolio Website Creation Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
if (!(Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js not found. Please install Node.js 20+ first." -ForegroundColor Red
    Write-Host "   Download from: https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

$nodeVersion = node --version
Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green

# Navigate to Desktop
$desktopPath = "C:\Users\Aymen\Desktop"
Set-Location $desktopPath

Write-Host ""
Write-Host "📂 Creating portfolio project at: $desktopPath\portfolio-aymen" -ForegroundColor Yellow
Write-Host ""

# Create Next.js project (using lowercase name for npm compatibility)
Write-Host "⚡ Creating Next.js 15 project..." -ForegroundColor Cyan
npx create-next-app@latest portfolio-aymen --typescript --tailwind --eslint --app --no-git --import-alias "@/*"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create Next.js project" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Next.js project created successfully!" -ForegroundColor Green

# Navigate to project
Set-Location portfolio-aymen

Write-Host ""
Write-Host "📦 Installing additional dependencies..." -ForegroundColor Cyan

# Install dependencies
npm install framer-motion lucide-react react-hot-toast emailjs-com clsx tailwind-merge

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green

# Create directory structure
Write-Host ""
Write-Host "📁 Creating directory structure..." -ForegroundColor Cyan

$directories = @(
    "components",
    "data",
    "lib",
    "scripts",
    ".github/workflows",
    "public/images/screenshots"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    Write-Host "   ✓ Created: $dir" -ForegroundColor Gray
}

# Create empty data file
Write-Host ""
Write-Host "📄 Creating initial data files..." -ForegroundColor Cyan

@"
[]
"@ | Out-File -FilePath "data/projects.json" -Encoding UTF8

Write-Host "   ✓ Created: data/projects.json" -ForegroundColor Gray

# Create .env.example
@"
# EmailJS Configuration (for contact form)
NEXT_PUBLIC_EMAILJS_SERVICE_ID=your_service_id
NEXT_PUBLIC_EMAILJS_TEMPLATE_ID=your_template_id
NEXT_PUBLIC_EMAILJS_PUBLIC_KEY=your_public_key

# GitHub API (optional for private repos)
GITHUB_TOKEN=your_github_token

# Analytics (optional)
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=aymen-chaghoub.vercel.app
"@ | Out-File -FilePath ".env.example" -Encoding UTF8

Write-Host "   ✓ Created: .env.example" -ForegroundColor Gray

# Create vercel.json
@"
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["cdg1"],
  "github": {
    "enabled": true,
    "autoAlias": true
  }
}
"@ | Out-File -FilePath "vercel.json" -Encoding UTF8

Write-Host "   ✓ Created: vercel.json" -ForegroundColor Gray

# Create lib/utils.ts
@"
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}
"@ | Out-File -FilePath "lib/utils.ts" -Encoding UTF8

Write-Host "   ✓ Created: lib/utils.ts" -ForegroundColor Gray

Write-Host ""
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ Portfolio project setup complete!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   1. Add Components" -ForegroundColor Yellow
Write-Host "      - Copy component code from: ../PFE/PORTFOLIO_SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host "      - Create files in: components/" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Add Pages" -ForegroundColor Yellow
Write-Host "      - Update: app/page.tsx" -ForegroundColor Gray
Write-Host "      - Create: app/about/page.tsx" -ForegroundColor Gray
Write-Host "      - Create: app/projects/page.tsx" -ForegroundColor Gray
Write-Host "      - Create: app/contact/page.tsx" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. Add Project Data" -ForegroundColor Yellow
Write-Host "      - Edit: data/projects.json" -ForegroundColor Gray
Write-Host "      - Add screenshots to: public/images/screenshots/" -ForegroundColor Gray
Write-Host ""
Write-Host "   4. Configure Tailwind" -ForegroundColor Yellow
Write-Host "      - Update: tailwind.config.ts (add violet colors)" -ForegroundColor Gray
Write-Host "      - See: ../PFE/PORTFOLIO_SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host ""
Write-Host "   5. Add Auto-Sync (Phase 9.5)" -ForegroundColor Yellow
Write-Host "      - Create: scripts/sync_portfolio.py" -ForegroundColor Gray
Write-Host "      - Create: .github/workflows/sync.yml" -ForegroundColor Gray
Write-Host "      - See: ../PFE/AUTO_SYNC_GUIDE.md" -ForegroundColor Gray
Write-Host ""
Write-Host "   6. Run Development Server" -ForegroundColor Yellow
Write-Host "      cd portfolio-aymen" -ForegroundColor Gray
Write-Host "      npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Access your portfolio at: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - Setup Guide: ../PFE/PORTFOLIO_SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host "   - Auto-Sync Guide: ../PFE/AUTO_SYNC_GUIDE.md" -ForegroundColor Gray
Write-Host "   - Phase 9 Summary: ../PFE/PHASE_9_SUMMARY.md" -ForegroundColor Gray
Write-Host "   - Phase 9.5 Summary: ../PFE/PHASE_9_5_SUMMARY.md" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Tip: Follow the PORTFOLIO_SETUP_GUIDE.md step by step!" -ForegroundColor Yellow
Write-Host ""
