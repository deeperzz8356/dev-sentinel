from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

from services.github_service import GitHubService
from services.simple_analyzer import SimpleAnalyzer  # Using simple analyzer instead
from models.analysis_models import ProfileAnalysis, RedFlag

load_dotenv()

app = FastAPI(title="Dev-Sentinel API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
github_service = GitHubService(token=os.getenv("GITHUB_TOKEN"))
analyzer = SimpleAnalyzer()  # Using simple rule-based analyzer

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
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ml_model_loaded": analyzer.is_model_loaded()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)