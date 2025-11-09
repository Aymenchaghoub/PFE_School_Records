#!/usr/bin/env pwsh
# Deployment Validation Script
# Checks if frontend and backend are properly configured and accessible

Write-Host "🔍 School Records Management - Deployment Validation" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host ""

$errors = 0
$warnings = 0

# Function to test HTTP endpoint
function Test-Endpoint {
    param(
        [string]$Url,
        [string]$Name,
        [int]$ExpectedStatus = 200
    )
    
    try {
        $response = Invoke-WebRequest -Uri $Url -Method GET -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq $ExpectedStatus) {
            Write-Host "✅ $Name is accessible" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ $Name returned status $($response.StatusCode)" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ $Name is not accessible: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Check Backend
Write-Host "🔧 Checking Backend..." -ForegroundColor Yellow
if (Test-Endpoint "http://localhost:8000/health" "Backend Health Check") {
    Write-Host "  → Testing API documentation..." -ForegroundColor Gray
    Test-Endpoint "http://localhost:8000/docs" "API Documentation" | Out-Null
} else {
    $errors++
    Write-Host "  ⚠️  Backend is not running. Start it with:" -ForegroundColor Yellow
    Write-Host "     cd backend && .\start_backend.ps1" -ForegroundColor Gray
}
Write-Host ""

# Check Frontend
Write-Host "🎨 Checking Frontend..." -ForegroundColor Yellow
if (Test-Path "frontend/dist/index.html") {
    Write-Host "✅ Frontend build exists" -ForegroundColor Green
    
    # Check if dev server is running
    if (Test-Endpoint "http://localhost:5173" "Frontend Dev Server") {
        # All good
    } else {
        $warnings++
        Write-Host "  ⚠️  Frontend dev server is not running. Start it with:" -ForegroundColor Yellow
        Write-Host "     cd frontend && npm run dev" -ForegroundColor Gray
    }
} else {
    $warnings++
    Write-Host "⚠️  Frontend not built. Build it with:" -ForegroundColor Yellow
    Write-Host "   cd frontend && npm run build" -ForegroundColor Gray
}
Write-Host ""

# Check Environment Files
Write-Host "📄 Checking Environment Files..." -ForegroundColor Yellow

if (Test-Path "backend/.env") {
    Write-Host "✅ Backend .env exists" -ForegroundColor Green
} else {
    $errors++
    Write-Host "❌ Backend .env missing. Copy from .env.example" -ForegroundColor Red
}

if (Test-Path "frontend/.env.development" -or Test-Path "frontend/.env") {
    Write-Host "✅ Frontend .env exists" -ForegroundColor Green
} else {
    $warnings++
    Write-Host "⚠️  Frontend .env missing. Copy from .env.example" -ForegroundColor Yellow
}
Write-Host ""

# Check Database Connection
Write-Host "🗄️  Checking Database..." -ForegroundColor Yellow
try {
    $dbCheck = python -c "from backend.app.core.database import engine; engine.connect(); print('OK')" 2>&1
    if ($dbCheck -like "*OK*") {
        Write-Host "✅ Database connection successful" -ForegroundColor Green
    } else {
        $errors++
        Write-Host "❌ Database connection failed" -ForegroundColor Red
    }
} catch {
    $errors++
    Write-Host "❌ Cannot check database: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Check Docker (if available)
Write-Host "🐳 Checking Docker Setup..." -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker is installed" -ForegroundColor Green
    
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        Write-Host "✅ Docker Compose is installed" -ForegroundColor Green
        
        if (Test-Path "docker-compose.yml") {
            Write-Host "✅ docker-compose.yml exists" -ForegroundColor Green
            
            # Check if containers are running
            $running = docker ps --format "{{.Names}}" 2>$null
            if ($running -match "pfc-") {
                Write-Host "✅ Docker containers are running" -ForegroundColor Green
            } else {
                Write-Host "  ℹ️  Docker containers not running. Start with:" -ForegroundColor Cyan
                Write-Host "     docker-compose up -d" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "⚠️  Docker Compose not found" -ForegroundColor Yellow
    }
} else {
    Write-Host "ℹ️  Docker not installed (optional)" -ForegroundColor Cyan
}
Write-Host ""

# Check Git Status
Write-Host "📦 Checking Git Status..." -ForegroundColor Yellow
if (Get-Command git -ErrorAction SilentlyContinue) {
    $gitStatus = git status --porcelain 2>$null
    if ($gitStatus) {
        Write-Host "⚠️  Uncommitted changes detected" -ForegroundColor Yellow
        Write-Host "   Run 'git status' to see changes" -ForegroundColor Gray
    } else {
        Write-Host "✅ Git repository is clean" -ForegroundColor Green
    }
} else {
    Write-Host "ℹ️  Git not installed (optional)" -ForegroundColor Cyan
}
Write-Host ""

# Summary
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host "📊 Validation Summary" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "✅ All checks passed! Deployment is ready." -ForegroundColor Green
    exit 0
} else {
    if ($errors -gt 0) {
        Write-Host "❌ Found $errors error(s)" -ForegroundColor Red
    }
    if ($warnings -gt 0) {
        Write-Host "⚠️  Found $warnings warning(s)" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Please fix the issues above before deploying." -ForegroundColor Yellow
    exit 1
}
