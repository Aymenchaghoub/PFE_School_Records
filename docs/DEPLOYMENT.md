# 🚀 Deployment Guide

This guide covers deploying the School Records Management System to free hosting platforms.

## Prerequisites

- GitHub account
- PlanetScale account (free tier)
- Render account (free tier)
- Netlify account (free tier)

## Step 1: Database Setup (PlanetScale)

1. **Create PlanetScale Account**
   - Go to [planetscale.com](https://planetscale.com)
   - Sign up for free account

2. **Create Database**
   - Click "New database"
   - Name it `school-records`
   - Select region closest to you
   - Click "Create database"

3. **Get Connection String**
   - Go to database settings
   - Click "Connect"
   - Copy the connection string (format: `mysql://user:password@host/database`)
   - Save this for backend deployment

## Step 2: Backend Deployment (Render)

1. **Prepare Repository**
   - Push your code to GitHub
   - Ensure `Procfile` is in the root directory
   - Ensure `backend/requirements.txt` exists

2. **Create Web Service on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   - **Name**: `school-records-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main` or `master`
   - **Root Directory**: `backend` (important!)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**
   Add these in Render dashboard:
   ```
   DATABASE_URL=mysql+pymysql://user:password@host/database
   SECRET_KEY=your-secret-key-min-32-characters
   JWT_EXPIRE_MINUTES=60
   JWT_REFRESH_EXPIRE_DAYS=7
   ```
   - Replace `DATABASE_URL` with your PlanetScale connection string
   - Generate a strong `SECRET_KEY` (use `openssl rand -hex 32`)

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your service URL (e.g., `https://school-records-backend.onrender.com`)

## Step 3: Frontend Deployment (Netlify)

1. **Build Frontend Locally** (Optional)
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub repository

3. **Configure Build Settings**
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`

4. **Environment Variables**
   Add in Netlify dashboard:
   ```
   VITE_API_BASE_URL=https://your-backend-url.onrender.com
   ```
   - Replace with your Render backend URL (without `/api`)

5. **Deploy**
   - Click "Deploy site"
   - Wait for deployment
   - Your site will be live at `https://your-site.netlify.app`

## Step 4: Seed Initial Data

After backend is deployed:

1. **SSH into Render** (or use Render shell)
   ```bash
   cd backend
   python -m app.seed_data
   ```

2. **Or use Render Shell**
   - Go to Render dashboard
   - Click on your service
   - Click "Shell" tab
   - Run: `python -m app.seed_data`

## Step 5: Update CORS

Update backend CORS settings in `app/core/config.py`:

```python
cors_origins: list[str] = [
    "https://your-site.netlify.app",
    "http://localhost:3000"  # For local development
]
```

Or set environment variable:
```
CORS_ORIGINS=https://your-site.netlify.app,http://localhost:3000
```

## Troubleshooting

### Backend Issues

- **Database Connection Error**: Check `DATABASE_URL` format
- **Port Error**: Ensure `$PORT` is used in start command
- **Import Errors**: Check that `backend` is set as root directory

### Frontend Issues

- **API Connection Error**: Verify `VITE_API_BASE_URL` is correct
- **Build Errors**: Check Node.js version (should be 18+)
- **CORS Errors**: Update CORS settings in backend

### Database Issues

- **Connection Timeout**: Check PlanetScale database is active
- **SSL Required**: Ensure connection string includes SSL parameters

## Post-Deployment Checklist

- [ ] Backend is accessible at Render URL
- [ ] Frontend is accessible at Netlify URL
- [ ] Database connection is working
- [ ] Seed data script ran successfully
- [ ] Login works with demo credentials
- [ ] CORS is configured correctly
- [ ] HTTPS is enabled on both platforms

## Monitoring

- **Render**: Check service logs in dashboard
- **Netlify**: Check deploy logs and functions
- **PlanetScale**: Monitor database usage and connections

## Cost

All services are free:
- **Render**: Free tier (spins down after inactivity)
- **Netlify**: Free tier (100GB bandwidth/month)
- **PlanetScale**: Free tier (5GB storage, 1 billion row reads/month)

For production, consider upgrading for:
- Always-on service (Render)
- More bandwidth (Netlify)
- Higher database limits (PlanetScale)

