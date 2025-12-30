from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

from services.github_service import GitHubService
from services.trained_ml_analyzer import TrainedMLAnalyzer
from services.rate_limiter import rate_limiter
from models.analysis_models import ProfileAnalysis, RedFlag

load_dotenv()

app = FastAPI(title="Dev-Sentinel API", version="1.0.0")

# Get environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# CORS origins based on environment
if ENVIRONMENT == "production":
    allowed_origins = [
        "https://dev-sentinel.vercel.app",
        "https://dev-sentinel-*.vercel.app",
        "https://*.vercel.app",
        "http://localhost:8080",
        "http://localhost:8081"
    ]
else:
    allowed_origins = [
        "http://localhost:8080", 
        "http://localhost:8081", 
        "http://localhost:8082", 
        "http://localhost:3000"
    ]

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
github_service = GitHubService(token=os.getenv("GITHUB_TOKEN"))
analyzer = TrainedMLAnalyzer()  # Using simple rule-based analyzer

class AnalysisRequest(BaseModel):
    username: str

@app.get("/")
async def root():
    return {"message": "Dev-Sentinel ML API is running"}

@app.post("/analyze/{username}", response_model=ProfileAnalysis)
async def analyze_profile(username: str):
    """
    Analyze a GitHub profile using ML model
    """
    try:
        # Fetch GitHub data
        github_data = await github_service.get_profile_data(username)
        
        # Run analysis
        analysis = analyzer.analyze_profile(github_data)
        
        return analysis
        
    except Exception as e:
        print(f"❌ Analysis failed for {username}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/test-mock/{username}")
async def test_mock_data(username: str):
    """
    Test endpoint to generate mock data for testing
    """
    try:
        # Force mock data generation
        mock_data = github_service._get_mock_profile_data(username)
        analysis = analyzer.analyze_profile(mock_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ml_model_loaded": analyzer.is_model_loaded()}

@app.get("/rate-limit")
async def get_rate_limit():
    """Get GitHub API rate limit status"""
    try:
        rate_info = github_service.get_rate_limit_info()
        return rate_info
    except Exception as e:
        return {"error": str(e)}

@app.get("/usage-stats")
async def get_usage_stats():
    """Get current API usage statistics"""
    try:
        stats = rate_limiter.get_usage_stats()
        return stats
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)