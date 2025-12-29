import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import joblib
import os
from typing import Dict, List, Tuple
from collections import Counter

from models.analysis_models import ProfileAnalysis, RedFlag, MetricData

class MLAnalyzer:
    def __init__(self):
        self.authenticity_model = None
        self.anomaly_detector = None
        self.scaler = StandardScaler()
        self.model_loaded = False
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Load existing model or train a new one"""
        model_path = "models/authenticity_model.joblib"
        scaler_path = "models/scaler.joblib"
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.authenticity_model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
            self.model_loaded = True
        else:
            self._train_initial_model()
    
    def _train_initial_model(self):
        """Train initial model with synthetic data (replace with real data later)"""
        # Generate synthetic training data for demonstration
        synthetic_data = self._generate_synthetic_training_data()
        
        X = synthetic_data.drop(['is_authentic'], axis=1)
        y = synthetic_data['is_authentic']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest for authenticity classification
        self.authenticity_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.authenticity_model.fit(X_train_scaled, y_train)
        
        # Train anomaly detector
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.anomaly_detector.fit(X_train_scaled)
        
        # Save models
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.authenticity_model, "models/authenticity_model.joblib")
        joblib.dump(self.scaler, "models/scaler.joblib")
        
        self.model_loaded = True
        print("ML models trained and saved successfully!")
    
    def _generate_synthetic_training_data(self) -> pd.DataFrame:
        """Generate synthetic training data for initial model"""
        np.random.seed(42)
        n_samples = 1000
        
        data = []
        for i in range(n_samples):
            # Authentic profiles (70% of data)
            if i < 700:
                is_authentic = 1
                # Authentic profile characteristics
                commit_frequency = np.random.normal(15, 5)  # Regular commits
                weekend_commit_ratio = np.random.uniform(0.1, 0.3)  # Low weekend commits
                night_commit_ratio = np.random.uniform(0.05, 0.2)  # Low night commits
                original_repo_ratio = np.random.uniform(0.6, 0.9)  # High original content
                commit_size_variance = np.random.uniform(0.3, 0.8)  # Varied commit sizes
                activity_consistency = np.random.uniform(0.7, 0.95)  # Consistent activity
                follower_repo_ratio = np.random.uniform(0.5, 3.0)  # Reasonable ratio
                language_diversity = np.random.randint(3, 8)  # Multiple languages
            else:
                is_authentic = 0
                # Suspicious profile characteristics
                commit_frequency = np.random.choice([
                    np.random.normal(50, 10),  # Too many commits
                    np.random.normal(2, 1)     # Too few commits
                ])
                weekend_commit_ratio = np.random.uniform(0.4, 0.8)  # High weekend commits
                night_commit_ratio = np.random.uniform(0.3, 0.7)   # High night commits
                original_repo_ratio = np.random.uniform(0.1, 0.4)  # Low original content
                commit_size_variance = np.random.uniform(0.05, 0.2) # Uniform commit sizes
                activity_consistency = np.random.uniform(0.2, 0.6)  # Inconsistent activity
                follower_repo_ratio = np.random.choice([
                    np.random.uniform(0.01, 0.1),  # Too few followers
                    np.random.uniform(10, 50)      # Too many followers
                ])
                language_diversity = np.random.randint(1, 3)  # Limited languages
            
            data.append({
                'commit_frequency': max(0, commit_frequency),
                'weekend_commit_ratio': np.clip(weekend_commit_ratio, 0, 1),
                'night_commit_ratio': np.clip(night_commit_ratio, 0, 1),
                'original_repo_ratio': np.clip(original_repo_ratio, 0, 1),
                'commit_size_variance': np.clip(commit_size_variance, 0, 1),
                'activity_consistency': np.clip(activity_consistency, 0, 1),
                'follower_repo_ratio': max(0, follower_repo_ratio),
                'language_diversity': language_diversity,
                'is_authentic': is_authentic
            })
        
        return pd.DataFrame(data)
    
    def analyze_profile(self, github_data: Dict) -> ProfileAnalysis:
        """Main analysis function using ML model"""
        if not self.model_loaded:
            raise Exception("ML model not loaded")
        
        # Extract features from GitHub data
        features = self._extract_features(github_data)
        
        # Scale features
        features_scaled = self.scaler.transform([list(features.values())])
        
        # Get authenticity prediction
        authenticity_prob = self.authenticity_model.predict_proba(features_scaled)[0]
        authenticity_score = int(authenticity_prob[1] * 100)  # Probability of being authentic
        
        # Detect anomalies
        anomaly_score = self.anomaly_detector.decision_function(features_scaled)[0]
        is_anomaly = self.anomaly_detector.predict(features_scaled)[0] == -1
        
        # Calculate confidence based on model certainty
        confidence = int(max(authenticity_prob) * 100)
        
        # Generate red flags
        red_flags = self._generate_red_flags(features, github_data, is_anomaly)
        
        # Generate metrics
        metrics = self._generate_metrics(github_data, features)
        
        return ProfileAnalysis(
            username=github_data['username'],
            authenticity_score=authenticity_score,
            confidence=confidence,
            red_flags=red_flags,
            metrics=metrics,
            analysis_timestamp=datetime.now().isoformat()
        )
    
    def _extract_features(self, github_data: Dict) -> Dict[str, float]:
        """Extract ML features from GitHub data"""
        commits = github_data.get('commits', [])
        repos = github_data.get('repositories', [])
        user_data = github_data.get('user', {})
        
        # Commit pattern features
        commit_frequency = len(commits) / max(1, github_data.get('account_age_days', 1)) * 365
        
        # Time-based patterns
        weekend_commits = sum(1 for c in commits if self._is_weekend(c.get('date', '')))
        weekend_commit_ratio = weekend_commits / max(1, len(commits))
        
        night_commits = sum(1 for c in commits if self._is_night_time(c.get('date', '')))
        night_commit_ratio = night_commits / max(1, len(commits))
        
        # Repository patterns
        original_repos = sum(1 for r in repos if not r.get('fork', False))
        original_repo_ratio = original_repos / max(1, len(repos))
        
        # Commit size variance
        commit_sizes = [c.get('additions', 0) + c.get('deletions', 0) for c in commits]
        commit_size_variance = np.var(commit_sizes) / (np.mean(commit_sizes) + 1) if commit_sizes else 0
        
        # Activity consistency (simplified)
        activity_consistency = self._calculate_activity_consistency(commits)
        
        # Social metrics
        followers = user_data.get('followers', 0)
        public_repos = user_data.get('public_repos', 1)
        follower_repo_ratio = followers / max(1, public_repos)
        
        # Language diversity
        languages = set()
        for repo in repos:
            if repo.get('language'):
                languages.add(repo['language'])
        language_diversity = len(languages)
        
        return {
            'commit_frequency': commit_frequency,
            'weekend_commit_ratio': weekend_commit_ratio,
            'night_commit_ratio': night_commit_ratio,
            'original_repo_ratio': original_repo_ratio,
            'commit_size_variance': min(1.0, commit_size_variance),  # Cap at 1.0
            'activity_consistency': activity_consistency,
            'follower_repo_ratio': min(10.0, follower_repo_ratio),  # Cap at 10.0
            'language_diversity': min(10, language_diversity)  # Cap at 10
        }
    
    def _is_weekend(self, date_str: str) -> bool:
        """Check if commit was made on weekend"""
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date.weekday() >= 5  # Saturday = 5, Sunday = 6
        except:
            return False
    
    def _is_night_time(self, date_str: str) -> bool:
        """Check if commit was made during night hours (10 PM - 6 AM)"""
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            hour = date.hour
            return hour >= 22 or hour <= 6
        except:
            return False
    
    def _calculate_activity_consistency(self, commits: List[Dict]) -> float:
        """Calculate how consistent the activity pattern is"""
        if len(commits) < 7:
            return 0.5  # Not enough data
        
        # Group commits by week
        weekly_commits = {}
        for commit in commits:
            try:
                date = datetime.fromisoformat(commit.get('date', '').replace('Z', '+00:00'))
                week = date.isocalendar()[1]  # Week number
                weekly_commits[week] = weekly_commits.get(week, 0) + 1
            except:
                continue
        
        if not weekly_commits:
            return 0.0
        
        # Calculate coefficient of variation (lower = more consistent)
        commit_counts = list(weekly_commits.values())
        mean_commits = np.mean(commit_counts)
        std_commits = np.std(commit_counts)
        
        if mean_commits == 0:
            return 0.0
        
        cv = std_commits / mean_commits
        # Convert to consistency score (0-1, higher = more consistent)
        consistency = max(0, 1 - cv)
        return min(1.0, consistency)
    
    def _generate_red_flags(self, features: Dict, github_data: Dict, is_anomaly: bool) -> List[RedFlag]:
        """Generate red flags based on ML analysis"""
        red_flags = []
        
        # High weekend commit ratio
        if features['weekend_commit_ratio'] > 0.4:
            red_flags.append(RedFlag(
                id="weekend_commits",
                title="Suspicious Weekend Activity",
                description=f"{features['weekend_commit_ratio']:.1%} of commits on weekends",
                severity="high" if features['weekend_commit_ratio'] > 0.6 else "medium",
                details="Authentic developers typically commit less on weekends. High weekend activity may indicate automated or batch commits."
            ))
        
        # High night commit ratio
        if features['night_commit_ratio'] > 0.3:
            red_flags.append(RedFlag(
                id="night_commits",
                title="Unusual Night Activity",
                description=f"{features['night_commit_ratio']:.1%} of commits between 10 PM - 6 AM",
                severity="high" if features['night_commit_ratio'] > 0.5 else "medium",
                details="Most developers commit during regular hours. Excessive night commits may indicate automated activity."
            ))
        
        # Low original content
        if features['original_repo_ratio'] < 0.4:
            red_flags.append(RedFlag(
                id="low_original_content",
                title="Low Original Content Ratio",
                description=f"Only {features['original_repo_ratio']:.1%} of repositories are original",
                severity="medium",
                details="Authentic developers typically have a mix of original projects showcasing their skills."
            ))
        
        # Low activity consistency
        if features['activity_consistency'] < 0.4:
            red_flags.append(RedFlag(
                id="inconsistent_activity",
                title="Inconsistent Activity Pattern",
                description="Irregular commit patterns detected",
                severity="medium",
                details="Authentic developers usually have more consistent activity patterns over time."
            ))
        
        # Anomaly detection
        if is_anomaly:
            red_flags.append(RedFlag(
                id="statistical_anomaly",
                title="Statistical Anomaly Detected",
                description="Profile shows unusual patterns compared to typical developers",
                severity="high",
                details="ML model detected this profile as statistically anomalous compared to authentic developer patterns."
            ))
        
        return red_flags
    
    def _generate_metrics(self, github_data: Dict, features: Dict) -> MetricData:
        """Generate metrics for the analysis"""
        user_data = github_data.get('user', {})
        commits = github_data.get('commits', [])
        repos = github_data.get('repositories', [])
        
        return MetricData(
            total_commits=len(commits),
            public_repos=user_data.get('public_repos', 0),
            followers=user_data.get('followers', 0),
            original_repos_percent=int(features['original_repo_ratio'] * 100),
            activity_consistency=int(features['activity_consistency'] * 100),
            language_diversity=int(features['language_diversity'])
        )
    
    def is_model_loaded(self) -> bool:
        """Check if ML model is loaded"""
        return self.model_loaded