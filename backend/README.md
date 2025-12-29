# Dev-Sentinel ML Backend

This is the ML-powered backend for Dev-Sentinel that analyzes GitHub profiles for authenticity using machine learning.

## Features

- **ML-Powered Analysis**: Uses Random Forest and Isolation Forest algorithms
- **GitHub API Integration**: Fetches real profile data via PyGithub
- **Real-time Analysis**: Fast API endpoints for instant results
- **Anomaly Detection**: Identifies statistically unusual patterns
- **Red Flag Generation**: Automatically detects suspicious behaviors

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your GitHub Personal Access Token:
```
GITHUB_TOKEN=your_github_token_here
```

**To get a GitHub token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `public_repo`, `read:user`
4. Copy the token to your `.env` file

### 3. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Analyze a profile
curl -X POST http://localhost:8000/analyze/octocat
```

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check and ML model status
- `POST /analyze/{username}` - Analyze GitHub profile

## ML Model Features

The model analyzes these patterns:

1. **Commit Frequency** - How often the user commits
2. **Weekend Commit Ratio** - Percentage of weekend commits
3. **Night Commit Ratio** - Percentage of late-night commits
4. **Original Repo Ratio** - Percentage of non-forked repositories
5. **Commit Size Variance** - Consistency of commit sizes
6. **Activity Consistency** - Regularity of activity patterns
7. **Follower/Repo Ratio** - Social engagement metrics
8. **Language Diversity** - Number of programming languages used

## Red Flags Detected

- Suspicious weekend activity (>40% weekend commits)
- Unusual night activity (>30% night commits)
- Low original content (<40% original repos)
- Inconsistent activity patterns
- Statistical anomalies detected by ML model

## Model Training

The system includes an initial synthetic dataset for training. For production use:

1. Collect labeled data of authentic vs suspicious profiles
2. Replace `_generate_synthetic_training_data()` with real data
3. Retrain the model with `ml_analyzer._train_initial_model()`

## Rate Limits

- GitHub API: 5000 requests/hour (authenticated)
- Unauthenticated: 60 requests/hour
- The service automatically handles rate limiting

## Architecture

```
backend/
├── main.py                 # FastAPI application
├── services/
│   ├── github_service.py   # GitHub API integration
│   └── ml_analyzer.py      # ML model and analysis
├── models/
│   └── analysis_models.py  # Pydantic data models
└── models/                 # Trained ML models (auto-generated)
    ├── authenticity_model.joblib
    └── scaler.joblib
```