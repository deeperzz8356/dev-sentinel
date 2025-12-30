#!/bin/bash

# Dev-Sentinel Deployment Script
echo "🚀 Starting Dev-Sentinel deployment..."

# Build the frontend
echo "📦 Building frontend for production..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Frontend build successful!"
else
    echo "❌ Frontend build failed!"
    exit 1
fi

echo "🎉 Ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Deploy backend to Railway: railway deploy"
echo "2. Deploy frontend to Vercel: vercel --prod"
echo "3. Update environment variables with backend URL"