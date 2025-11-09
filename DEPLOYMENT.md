# 🚀 Deployment Guide - School Records Management System

Complete guide for deploying the full-stack application (FastAPI + React + MySQL) to various platforms.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment (Render + Netlify)](#cloud-deployment)
- [Alternative Platforms](#alternative-platforms)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.13+** (for backend)
- **Node.js 20+** (for frontend)
- **MySQL 8.0+** (for database)
- **Docker & Docker Compose** (optional, for containerized deployment)
- **Git** (for version control)

### Accounts Needed (for cloud deployment)
- **Render.com** account (for backend)
- **Netlify** account (for frontend)
- **MySQL** cloud database (e.g., PlanetScale, Railway, or Render PostgreSQL)

---

## 🏠 Local Development

### Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env
# Edit .env with your configuration

# Run migrations
python -m alembic upgrade head

# Start development server
python -m uvicorn app.main:app --reload

# Or use the start script
.\start_backend.ps1          # Windows
# bash start_backend.sh        # Linux/Mac
```

**Backend will be available at:** `http://localhost:8000`  
**API Documentation:** `http://localhost:8000/docs`

### Frontend Setup

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env.development
# Edit with: VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

**Frontend will be available at:** `http://localhost:5173`

### Database Setup (XAMPP)

1. Start **XAMPP Control Panel**
2. Start **Apache** and **MySQL** services
3. Open **phpMyAdmin**: `http://localhost/phpmyadmin`
4. Create database: `CREATE DATABASE pfc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

---

## 🐳 Docker Deployment

### Quick Start

```bash
# Copy environment file
cp .env.docker.example .env.docker
# Edit .env.docker with your configuration

# Build and start all services
docker-compose --env-file .env.docker up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (⚠️ deletes database data)
docker-compose down -v
```

### Access Points
- **Frontend:** `http://localhost` (port 80)
- **Backend API:** `http://localhost:8000`
- **Backend Docs:** `http://localhost:8000/docs`
- **MySQL:** `localhost:3306`

### Docker Commands

```bash
# View running containers
docker-compose ps

# Execute commands in backend
docker-compose exec backend python -m alembic upgrade head

# View backend logs
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Rebuild specific service
docker-compose up -d --build backend
```

---

## ☁️ Cloud Deployment (Render + Netlify)

### Backend Deployment (Render)

1. **Prepare Repository**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`
   
4. **Configure Environment Variables**
   - Go to Environment tab
   - Add all variables from `render.yaml`:
     - `DATABASE_URL`: Your MySQL connection string
     - `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`
     - `CORS_ORIGINS`: `["https://your-frontend.netlify.app"]`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~5-10 minutes)
   - Your API will be at: `https://your-app.onrender.com`

### Frontend Deployment (Netlify)

1. **Prepare Frontend**
   ```bash
   cd frontend
   
   # Install Netlify CLI (optional)
   npm install -g netlify-cli
   
   # Test build locally
   npm run build
   npm run preview
   ```

2. **Deploy to Netlify**

   **Option A: Netlify UI**
   - Go to [netlify.com](https://netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect GitHub and select repository
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Add environment variable:
     - `VITE_API_URL`: `https://your-backend.onrender.com`
   - Click "Deploy"

   **Option B: Netlify CLI**
   ```bash
   cd frontend
   netlify login
   netlify init
   netlify deploy --prod
   ```

3. **Configure Custom Domain** (Optional)
   - Go to Site settings → Domain management
   - Add custom domain

### Update CORS Origins

After deploying frontend, update backend CORS:

1. Go to Render dashboard → Your service → Environment
2. Update `CORS_ORIGINS`:
   ```
   ["https://your-app.netlify.app","http://localhost:5173"]
   ```
3. Redeploy backend

---

## 🔄 Alternative Platforms

### Railway

```yaml
# railway.yaml
version: 2
services:
  backend:
    build:
      dockerfile: backend/Dockerfile
    env:
      - DATABASE_URL=${{DATABASE_URL}}
      - SECRET_KEY=${{SECRET_KEY}}
```

### Vercel (Frontend)

```json
// vercel.json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/dist",
  "framework": "vite",
  "env": {
    "VITE_API_URL": "https://your-backend.onrender.com"
  }
}
```

---

## 🔐 Environment Variables

### Backend (.env)

```env
DATABASE_URL=mysql+pymysql://user:pass@host:3306/db
SECRET_KEY=minimum-32-character-random-string
JWT_EXPIRE_MINUTES=60
JWT_REFRESH_EXPIRE_DAYS=7
ALGORITHM=HS256
CORS_ORIGINS=["https://frontend.com"]
API_V1_PREFIX=/api
ENVIRONMENT=production
```

### Frontend (.env.production)

```env
VITE_API_URL=https://your-backend.onrender.com
VITE_APP_NAME="School Records Management"
VITE_APP_VERSION=1.0.0
```

---

## 🔧 Troubleshooting

### Backend Issues

**Database Connection Error**
```bash
# Test connection
python -c "from app.core.database import engine; print(engine.connect())"

# Check DATABASE_URL format
# Correct: mysql+pymysql://user:pass@host:3306/dbname
```

**Migration Errors**
```bash
# Reset migrations (⚠️ deletes data)
python -m alembic downgrade base
python -m alembic upgrade head

# Create new migration
python -m alembic revision --autogenerate -m "description"
```

**Import Errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**API Connection Error**
- Check `VITE_API_URL` in `.env`
- Verify backend CORS settings
- Check browser console for errors

**Build Failures**
```bash
# Clear cache
rm -rf node_modules dist
npm install
npm run build
```

### Docker Issues

**Port Already in Use**
```bash
# Change ports in .env.docker
FRONTEND_PORT=8080
BACKEND_PORT=8001
```

**Database Connection Refused**
```bash
# Wait for database to be ready
docker-compose logs db

# Restart backend after database is up
docker-compose restart backend
```

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] All tests passing (`pytest`)
- [ ] Environment variables configured
- [ ] `.env` files created (not committed to git)
- [ ] Database migrations tested
- [ ] Frontend builds successfully
- [ ] API documentation accessible

### Post-Deployment
- [ ] Backend health check: `https://api.com/health`
- [ ] Frontend loads correctly
- [ ] Login functionality works
- [ ] API requests successful
- [ ] Database connected
- [ ] CORS configured correctly
- [ ] HTTPS enabled
- [ ] Monitoring set up

---

## 📊 Performance Tips

1. **Enable Caching**
   - Use CDN for static assets
   - Configure browser caching headers

2. **Database Optimization**
   - Add indexes to frequently queried columns
   - Use connection pooling

3. **Backend Scaling**
   - Increase Gunicorn workers based on CPU cores
   - Enable gzip compression

4. **Frontend Optimization**
   - Code splitting
   - Lazy loading
   - Image optimization

---

## 🆘 Support

- **Documentation**: `http://localhost:8000/docs`
- **GitHub Issues**: Create an issue on the repository
- **Render Support**: https://render.com/docs
- **Netlify Support**: https://docs.netlify.com

---

**Last Updated**: November 2025  
**Python Version**: 3.13  
**Node Version**: 20+
