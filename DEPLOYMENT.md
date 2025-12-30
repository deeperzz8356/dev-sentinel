# 🚀 Dev-Sentinel Deployment Guide

This guide will help you deploy Dev-Sentinel to production using Vercel (frontend) and Railway (backend).

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- **Git** repository
- **GitHub** account
- **Vercel** account
- **Railway** account (or alternative: Render, Heroku)

## 🔧 **Step 1: Deploy Backend to Railway**

### 1.1 Install Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
```

### 1.2 Deploy Backend

```bash
# Navigate to backend directory
cd backend

# Initialize Railway project
railway new dev-sentinel-api

# Add current directory to Railway
railway add

# Set environment variables
railway variables set GITHUB_TOKEN=your_github_token_here
railway variables set ENVIRONMENT=production

# Deploy to Railway
railway deploy
```

### 1.3 Get Backend URL

After deployment, Railway will provide you with a URL like:
`https://dev-sentinel-api-production.up.railway.app`

## 🎨 **Step 2: Deploy Frontend to Vercel**

### 2.1 Install Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login
```

### 2.2 Configure Environment Variables

Update `.env.production` with your backend URL:

```env
VITE_API_BASE_URL=https://your-railway-backend-url.railway.app
VITE_ENVIRONMENT=production
VITE_APP_NAME=Dev-Sentinel
VITE_APP_VERSION=1.0.0
```

### 2.3 Deploy to Vercel

```bash
# From the root directory (dev-sentinel/)
# Build for production
npm run build:prod

# Deploy to Vercel
vercel --prod

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name: dev-sentinel
# - Directory: ./
# - Override settings? No
```

### 2.4 Set Environment Variables in Vercel

In the Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables:

```
VITE_API_BASE_URL = https://your-railway-backend-url.railway.app
VITE_ENVIRONMENT = production
```

4. Redeploy the project

## 🔗 **Step 3: Update CORS Settings**

Update your backend's CORS settings to include your Vercel domain:

```python
# In backend/main.py
allowed_origins = [
    "https://dev-sentinel.vercel.app",
    "https://dev-sentinel-*.vercel.app",
    "https://*.vercel.app",
    "http://localhost:8080",
    "http://localhost:8081"
]
```

Redeploy your backend after making this change.

## ✅ **Step 4: Verify Deployment**

### 4.1 Test Backend

```bash
# Test backend health
curl https://your-railway-backend-url.railway.app/health

# Test profile analysis
curl -X POST https://your-railway-backend-url.railway.app/analyze/octocat
```

### 4.2 Test Frontend

1. Visit your Vercel URL: `https://dev-sentinel.vercel.app`
2. Try analyzing a GitHub profile
3. Check browser console for any errors

## 🔧 **Alternative Backend Deployment Options**

### Option 1: Render

```bash
# Create render.yaml in backend/
service:
  name: dev-sentinel-api
  env: python
  buildCommand: pip install -r requirements.txt
  startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
  envVars:
    - key: GITHUB_TOKEN
      value: your_token_here
    - key: ENVIRONMENT
      value: production
```

### Option 2: Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create dev-sentinel-api

# Set environment variables
heroku config:set GITHUB_TOKEN=your_token_here
heroku config:set ENVIRONMENT=production

# Deploy
git push heroku main
```

## 🚀 **Continuous Deployment**

### Auto-deploy on Git Push

**Vercel**: Automatically deploys on push to main branch

**Railway**: Set up auto-deploy in Railway dashboard:
1. Connect your GitHub repository
2. Set branch to `main`
3. Enable auto-deploy

## 📊 **Monitoring & Maintenance**

### Health Checks

- **Backend**: `https://your-backend-url/health`
- **Frontend**: Check Vercel deployment status

### Logs

- **Vercel**: View logs in Vercel dashboard
- **Railway**: View logs in Railway dashboard

### Updates

1. Push changes to your Git repository
2. Services will auto-deploy (if configured)
3. Manual deploy: `vercel --prod` and `railway deploy`

## 🔒 **Security Considerations**

1. **Environment Variables**: Never commit `.env` files
2. **CORS**: Restrict to your domains only
3. **Rate Limiting**: Monitor API usage
4. **GitHub Token**: Use minimal required permissions

## 🐛 **Troubleshooting**

### Common Issues

1. **CORS Errors**: Check backend CORS configuration
2. **API Not Found**: Verify backend URL in frontend env vars
3. **Build Failures**: Check Node.js/Python versions
4. **ML Model Loading**: Ensure model files are included in deployment

### Debug Commands

```bash
# Check Vercel deployment logs
vercel logs

# Check Railway deployment logs
railway logs

# Test API connectivity
curl -v https://your-backend-url/health
```

## 🎉 **Success!**

Your Dev-Sentinel application should now be live at:

- **Frontend**: `https://dev-sentinel.vercel.app`
- **Backend**: `https://your-backend-url.railway.app`
- **API Docs**: `https://your-backend-url.railway.app/docs`

## 📞 **Support**

If you encounter issues:

1. Check the logs in respective dashboards
2. Verify environment variables
3. Test API endpoints manually
4. Check CORS configuration

Happy deploying! 🚀