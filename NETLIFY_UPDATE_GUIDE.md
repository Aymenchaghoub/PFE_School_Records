# 🎨 NETLIFY FRONTEND UPDATE GUIDE

**Prerequisites**: Backend deployed on Render at `https://pfc-backend.onrender.com`

---

## 🎯 OBJECTIVE

Update the frontend to connect to your production backend on Render.

---

## 📋 NETLIFY UPDATE STEPS

### Step 1: Login to Netlify
1. Go to: https://app.netlify.com/
2. Sign in with your account
3. Find your site: **school-management-pfe**
4. Click on the site to open dashboard

### Step 2: Update Environment Variables

1. Click **"Site settings"** (in the site dashboard)
2. Click **"Environment variables"** (left sidebar under "Build & deploy")
3. Click **"Add a variable"** or **"Edit variables"**

**Add/Update this variable:**

```bash
Key: VITE_API_URL
Value: https://pfc-backend.onrender.com
```

**Important**: 
- No trailing slash in the URL
- Must start with `https://`
- Exact URL from Render deployment

### Step 3: Trigger New Deploy

**Option A: Redeploy (Fastest)**
1. Go to **"Deploys"** tab
2. Click **"Trigger deploy"** dropdown
3. Select **"Deploy site"**
4. Wait 2-3 minutes for build

**Option B: Git Push (Recommended for code changes)**
1. If you also have code changes to commit
2. Push to GitHub main branch
3. Netlify auto-deploys

### Step 4: Verify Build

Watch the deploy logs for:
```
✓ Build script success
✓ Site is live
```

**Build time**: 2-3 minutes

---

## ✅ VERIFICATION STEPS

### 1. Check Site Loads
Open: https://school-management-pfe.netlify.app

**Expected**: Site loads without errors

### 2. Open Browser Console
Press `F12` or right-click → "Inspect" → "Console" tab

**Check for**:
- ✅ No CORS errors
- ✅ No network errors
- ✅ API calls going to `https://pfc-backend.onrender.com`

### 3. Test Login (if you have test credentials)
Try logging in with test account:
- Should connect to backend
- Should receive JWT token
- Dashboard should load

### 4. Test API Connectivity
Open Network tab (F12 → Network):
- Try any action (login, load data, etc.)
- Check requests go to: `https://pfc-backend.onrender.com/api/...`
- Status should be `200 OK` or `401` (if not authenticated)

---

## 🔧 COMMON ISSUES & FIXES

### Issue: Site shows old backend URL
**Symptom**: API calls still going to old URL

**Fix**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Do a hard refresh (Ctrl+F5)
3. Try incognito/private window

### Issue: CORS Error
**Symptom**: Browser console shows CORS policy error

**Fix**:
1. Verify Netlify URL is in backend CORS_ORIGINS
2. Check Render environment variables
3. Redeploy backend if CORS_ORIGINS was wrong

### Issue: 404 or 500 Errors
**Symptom**: API calls return errors

**Fix**:
1. Verify backend is "Live" on Render
2. Test backend health: `https://pfc-backend.onrender.com/health`
3. Check backend logs on Render for errors

### Issue: Site won't load
**Symptom**: Netlify site shows error or blank page

**Fix**:
1. Check Netlify deploy logs for build errors
2. Verify all environment variables are set
3. Try redeploying

---

## 📊 FRONTEND ENVIRONMENT VARIABLES

Your frontend should have these environment variables:

```bash
# Production (Netlify)
VITE_API_URL=https://pfc-backend.onrender.com

# Optional (if you set these up)
VITE_ENABLE_ANALYTICS=false
VITE_ANALYTICS_PROVIDER=plausible
VITE_ANALYTICS_ID=your-domain.com
```

---

## 🔍 TESTING CHECKLIST

After deployment, test these features:

- [ ] Site loads successfully
- [ ] No console errors
- [ ] Login page appears
- [ ] Can attempt login (even if fails, should connect to backend)
- [ ] API calls visible in Network tab
- [ ] Requests go to Render backend URL
- [ ] Response times acceptable (<2 seconds)

---

## 📈 EXPECTED BEHAVIOR

### First Request (Cold Start)
- **Time**: 30-60 seconds (Render waking up)
- **Status**: May timeout initially
- **Fix**: Retry after 30 seconds

### Subsequent Requests
- **Time**: <2 seconds
- **Status**: 200 OK
- **Response**: JSON data

### After 15 Minutes Idle
- Backend spins down (free tier)
- Next request will be slow (cold start)
- Normal behavior for free tier

---

## 🎯 SUCCESS INDICATORS

✅ **Frontend Successfully Connected When:**
- Site loads without errors
- No CORS errors in console
- API calls reach Render backend
- Login/signup forms work
- Data loads from backend
- JWT tokens received and stored

---

## 🔗 KEY URLS

**Frontend**: https://school-management-pfe.netlify.app  
**Backend**: https://pfc-backend.onrender.com  
**API Docs**: https://pfc-backend.onrender.com/docs  
**Health Check**: https://pfc-backend.onrender.com/health

---

## 💡 PRO TIPS

1. **Keep Console Open**: Monitor for errors during testing
2. **Network Tab**: Check API request/response details
3. **Hard Refresh**: Clear cache if changes don't appear (Ctrl+F5)
4. **Incognito Mode**: Test without cached data
5. **Mobile Test**: Check responsiveness on mobile

---

## 📞 SUPPORT

If issues persist:
1. Check backend is "Live" on Render
2. Verify environment variables on both platforms
3. Review deploy logs for errors
4. Test backend health endpoint directly

---

**Estimated Time**: 5-10 minutes  
**Difficulty**: Easy

🎨 **Ready to update? Let's connect your frontend!**
