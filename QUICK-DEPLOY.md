# 🚀 Quick Deploy Guide

## Current Status
- ✅ **Frontend**: Ready for Vercel (with mock mode)
- ⏳ **Backend**: Needs deployment for real ML analysis

## Option 1: Deploy with Mock Data (Immediate)

Your app will work immediately on Vercel with demo data:

```bash
# Build and deploy to Vercel
npm run build
vercel --prod
```

**Result**: Working demo with fake data showing how the app works.

## Option 2: Deploy Backend for Real ML Analysis

### A. Using Render (Easiest - No CLI needed)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Settings:
   - **Name**: `dev-sentinel-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Environment Variables:
   - `GITHUB_TOKEN`: `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`
   - `ENVIRONMENT`: `production`
7. Click "Create Web Service"

### B. Update Frontend After Backend Deployment

Once you get the backend URL (e.g., `https://dev-sentinel-api.onrender.com`):

1. Update `src/services/api.ts`:
   ```typescript
   const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://your-backend-url.onrender.com';
   ```

2. Set environment variable in Vercel:
   - Go to Vercel dashboard → Your project → Settings → Environment Variables
   - Add: `VITE_API_BASE_URL` = `https://your-backend-url.onrender.com`

3. Redeploy:
   ```bash
   npm run build
   vercel --prod
   ```

## Current Features in Mock Mode

- ✅ **UI/UX**: Full dashboard experience
- ✅ **Charts**: Interactive visualizations
- ✅ **Demo Data**: Realistic fake analysis results
- ✅ **Responsive**: Works on all devices
- ⏳ **Real ML**: Needs backend deployment

## Test URLs

Try these usernames in mock mode:
- `torvalds` (high authenticity score)
- `gaearon` (high authenticity score)  
- `testuser` (random score with red flags)

## Next Steps

1. **Immediate**: Deploy frontend to Vercel with mock mode
2. **Later**: Deploy backend to Render for real ML analysis
3. **Optional**: Add more features and improvements

Your Dev-Sentinel is ready to impress! 🎉