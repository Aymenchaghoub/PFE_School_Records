#!/usr/bin/env pwsh
# Frontend Modernization Installation Script
# Installs all required dependencies for the modernized UI

Write-Host "🎨 Installing Frontend Modernization Dependencies..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the frontend directory
if (!(Test-Path "package.json")) {
    Write-Host "❌ Error: Please run this script from the frontend directory" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing UI dependencies..." -ForegroundColor Yellow

# Install core dependencies
$packages = @(
    "lucide-react",
    "react-hot-toast",
    "clsx",
    "tailwind-merge"
)

Write-Host "  → Installing: $($packages -join ', ')" -ForegroundColor Gray
npm install $packages

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Installation failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review the new components in src/components/" -ForegroundColor Gray
Write-Host "  2. The Login page has been modernized automatically" -ForegroundColor Gray
Write-Host "  3. To use the modern Dashboard, rename:" -ForegroundColor Gray
Write-Host "     Dashboard.tsx → Dashboard_OLD.tsx" -ForegroundColor Gray
Write-Host "     Dashboard_MODERN.tsx → Dashboard.tsx" -ForegroundColor Gray
Write-Host "  4. Run 'npm run dev' to see the changes" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Ready to preview!" -ForegroundColor Green
Write-Host "   Run: npm run dev" -ForegroundColor Cyan
