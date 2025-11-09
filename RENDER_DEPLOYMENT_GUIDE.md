# 🚀 Render Deployment Guide - pfc-backend

## Prerequisites ✅
- ✅ `.env` file created with production credentials
- ✅ `.env.example` updated for GitHub
- ✅ `render.yaml` configured for Frankfurt region
- ✅ GitHub repository: https://github.com/Aymenchaghoub/PFE_School_Records

---

## Step-by-Step Deployment

### 1. Login to Render
1. Go to: https://dashboard.render.com/
2. Sign in with your GitHub account

### 2. Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Select **"Connect Account"** if GitHub not connected
3. Choose repository: **Aymenchaghoub/PFE_School_Records**
4. Click **"Connect"**

### 3. Configure Service (Auto-detected from render.yaml)
Render should auto-detect the configuration. Verify these settings:

```
Name: pfc-backend
Root Directory: backend
Environment: Python
Region: Frankfurt (EU Central)
Branch: main
Build Command: cd backend && pip install --upgrade pip && pip install -r requirements.txt
Start Command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4. Add Environment Variables
**CRITICAL:** Add these environment variables manually:

Click **"Advanced"** → **"Add Environment Variable"**

```bash
# Database Connection (from AlwaysData)
DATABASE_URL=mysql+pymysql://439792:MySecurePassword2025!@mysql-aymenchaghoub.alwaysdata.net/aymenchaghoub_pfc

# Security Key (generated for you)
SECRET_KEY=GagEXwsULsGCsReho1Pu4vREiIv-FIWSfSxK6oUAlYY

# JWT Configuration
JWT_EXPIRE_MINUTES=60
JWT_REFRESH_EXPIRE_DAYS=7
ALGORITHM=HS256

# CORS Origins (JSON array)
CORS_ORIGINS=["http://localhost:5173","https://school-records-aymen.netlify.app"]

# API Configuration
API_V1_PREFIX=/api
ENVIRONMENT=production

# Python Version
PYTHON_VERSION=3.13.0
```

### 5. Deploy
1. Select **"Free"** plan
2. Click **"Create Web Service"**
3. Wait 5-10 minutes for initial deployment

---

## 5️⃣ Verify Deployment

### Automatic Health Check (once deployed)
```bash
# Run this in PowerShell from your PFE directory
python C:\Users\Aymen\Desktop\PFE\backend\verify_render_deployment.py
```

### Manual Health Check
Once Render shows "Live", visit:
```
https://pfc-backend.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-09T18:00:00Z"
}
```

---

## Troubleshooting

### Issue: Build Failed
**Solution:** Check logs for missing dependencies
```bash
# Add to requirements.txt if needed
pip freeze > requirements.txt
```

### Issue: Database Connection Error
**Solution:** Verify DATABASE_URL format
```
mysql+pymysql://USER:PASS@HOST/DATABASE
```

### Issue: Application Not Starting
**Solution:** Check start command uses correct port
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Issue: Health Check Failing
**Solution:** Ensure `/health` endpoint exists in app/main.py

---

## Expected Deployment URLs

- **Backend API**: https://pfc-backend.onrender.com
- **API Docs**: https://pfc-backend.onrender.com/docs
- **Health Check**: https://pfc-backend.onrender.com/health

---

## Post-Deployment Checklist

- [ ] Service shows "Live" status
- [ ] Health endpoint returns 200
- [ ] API docs accessible
- [ ] Database connected
- [ ] CORS configured for frontend

---

## 📝 Notes

- Free tier may have **cold starts** (30 seconds delay after inactivity)
- Service **spins down after 15 minutes** of inactivity
- First request after spin down takes **30-60 seconds**
- Consider upgrading to paid tier for production use

---

**Estimated Deployment Time:** 10-15 minutes
