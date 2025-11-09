# 🚀 DEPLOYMENT INSTRUCTIONS

## Prerequisites ✅
- GitHub Repository: https://github.com/Aymenchaghoub/PFE_School_Records
- Status: Code pushed and ready for deployment

---

## 📦 1. Backend Deployment (Render)

### Step-by-Step Instructions:

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com/
   - Sign in with your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select repository: `Aymenchaghoub/PFE_School_Records`

3. **Configure Service Settings**
   ```
   Name: school-records-backend
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

4. **Add Environment Variables**
   Click "Advanced" and add:
   ```
   DATABASE_URL=<your-mysql-database-url>
   SECRET_KEY=<generate-a-secure-32-character-key>
   JWT_EXPIRE_MINUTES=60
   JWT_REFRESH_EXPIRE_DAYS=7
   ALGORITHM=HS256
   CORS_ORIGINS=["https://your-frontend.netlify.app","http://localhost:5173"]
   API_V1_PREFIX=/api
   ENVIRONMENT=production
   ```

5. **Create Service**
   - Select "Free" plan
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

6. **Verify Deployment**
   - Check logs for successful startup
   - Visit: `https://school-records-backend.onrender.com/health`
   - Should return: `{"status":"healthy"}`

---

## 🎨 2. Frontend Deployment (Netlify)

### Step-by-Step Instructions:

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com/
   - Sign in with your GitHub account

2. **Import Project**
   - Click "Add new site" → "Import an existing project"
   - Choose "GitHub"
   - Select repository: `Aymenchaghoub/PFE_School_Records`

3. **Configure Build Settings**
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/dist
   ```

4. **Add Environment Variables**
   Click "Show advanced" and add:
   ```
   VITE_API_URL=https://school-records-backend.onrender.com
   VITE_ENABLE_ANALYTICS=false
   ```

5. **Deploy Site**
   - Click "Deploy site"
   - Wait for build to complete (2-5 minutes)

6. **Configure Custom Domain (Optional)**
   - Go to "Site settings" → "Domain management"
   - Add custom domain or use Netlify subdomain

7. **Verify Deployment**
   - Visit the provided URL
   - Test login functionality
   - Check API connectivity

---

## 🗄️ 3. Database Setup (Recommended: PlanetScale or Aiven)

### Option A: PlanetScale (MySQL-compatible)

1. **Create Account**
   - Visit: https://planetscale.com/
   - Sign up for free account

2. **Create Database**
   ```
   Name: school-records
   Region: Choose nearest to your location
   Plan: Free (Hobby)
   ```

3. **Get Connection String**
   - Go to "Connect" → "Connect with: Prisma"
   - Copy the DATABASE_URL
   - Update in Render environment variables

### Option B: Aiven (MySQL)

1. **Create Account**
   - Visit: https://aiven.io/
   - Sign up for free trial

2. **Create MySQL Service**
   ```
   Service: MySQL
   Cloud: Choose your region
   Plan: Free trial
   ```

3. **Get Connection Details**
   - Copy connection string
   - Update in Render environment variables

---

## 🔍 4. Post-Deployment Checklist

### Backend Verification
- [ ] Health endpoint responding: `/health`
- [ ] API documentation accessible: `/docs`
- [ ] Authentication working: `/api/auth/login`
- [ ] Database connected and migrations run
- [ ] CORS configured for frontend URL

### Frontend Verification
- [ ] Site loads without errors
- [ ] API URL correctly configured
- [ ] Login/logout functionality working
- [ ] Dashboard data loading
- [ ] All pages accessible

### Security Checks
- [ ] HTTPS enabled on all services
- [ ] Environment variables secure
- [ ] No sensitive data in logs
- [ ] JWT tokens working properly

---

## 🛠️ 5. Troubleshooting

### Common Issues and Solutions:

**Backend not starting on Render:**
```bash
# Check if all dependencies are in requirements.txt
# Verify Python version compatibility
# Check DATABASE_URL format
```

**Frontend build failing on Netlify:**
```bash
# Ensure Node version is specified
# Check for TypeScript errors
# Verify all dependencies in package.json
```

**Database connection issues:**
```bash
# Verify DATABASE_URL format
# Check network access permissions
# Ensure SSL is enabled if required
```

**CORS errors:**
```bash
# Update CORS_ORIGINS in backend
# Include full frontend URL with protocol
# Restart backend service
```

---

## 📊 6. Monitoring & Maintenance

### Setup Monitoring
1. **Uptime Monitoring**
   - Use: https://uptimerobot.com/ (free)
   - Monitor: Backend health endpoint
   - Alert: Email/SMS on downtime

2. **Error Tracking**
   - Enable Sentry in backend (optional)
   - Add SENTRY_DSN to environment variables

3. **Analytics**
   - Enable Plausible or Google Analytics
   - Add tracking code to frontend

### Regular Maintenance
- Check logs weekly for errors
- Update dependencies monthly
- Backup database regularly
- Monitor usage and upgrade if needed

---

## 🎉 7. Success Verification

Once deployed, your services should be available at:

- **Backend API**: `https://school-records-backend.onrender.com`
- **API Docs**: `https://school-records-backend.onrender.com/docs`
- **Frontend**: `https://[your-site-name].netlify.app`

### Final Testing Steps:
1. Create a test admin account
2. Log in and navigate all pages
3. Test CRUD operations
4. Verify PDF generation
5. Check responsive design

---

## 📝 Notes

- Render free tier may have cold starts (30+ seconds)
- Netlify free tier includes 100GB bandwidth/month
- Database free tiers have storage limits
- Consider upgrading for production use

## 🆘 Need Help?

- Render Docs: https://render.com/docs
- Netlify Docs: https://docs.netlify.com
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- React Deployment: https://create-react-app.dev/docs/deployment/

---

**Last Updated**: November 9, 2025
**Author**: Aymen Chaghoub
