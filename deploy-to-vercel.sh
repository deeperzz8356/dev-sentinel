#!/bin/bash

echo "🚀 Deploying Dev-Sentinel to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Build the application
echo "🔨 Building application..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Deploy to Vercel
    echo "🚀 Deploying to Vercel..."
    vercel --prod
    
    echo "🎉 Deployment complete!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Set environment variables in Vercel dashboard"
    echo "2. Add your backend URL to VITE_API_BASE_URL"
    echo "3. Update CORS settings in your backend"
    
else
    echo "❌ Build failed! Please fix the errors and try again."
    exit 1
fi