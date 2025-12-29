import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import Counter

from models.analysis_models import ProfileAnalysis, RedFlag, MetricData

class SimpleAnalyzer:
    """
    Simplified analyzer that doesn't require scikit-learn
    Uses rule-based analysis with statistical methods
    """
    
    def __init__(self):
        self.model_loaded = True
    
    def analyze_profile(self, github_data: Dict) -> ProfileAnalysis:
        """Main analysis function using rule-based approach"""
        
        # Extract features from GitHub data
        features = self._extract_features(github_data)
        
        # Calculate authenticity score using rule-based approach
        authenticity_score = self._calculate_authenticity_score(features)
        
        # Calculate confidence based on data quality
        confidence = self._calculate_confidence(github_data, features)
        
        # Generate red flags
        red_flags = self._generate_red_flags(features, github_data)
        
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
        """Extract analysis features from GitHub data"""
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
        
        # Commit size analysis
        commit_sizes = [c.get('additions', 0) + c.get('deletions', 0) for c in commits]
        commit_size_variance = np.var(commit_sizes) / (np.mean(commit_sizes) + 1) if commit_sizes else 0
        
        # Activity consistency
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
            'commit_size_variance': min(1.0, commit_size_variance),
            'activity_consistency': activity_consistency,
            'follower_repo_ratio': min(10.0, follower_repo_ratio),
            'language_diversity': min(10, language_diversity)
        }
    
    def _calculate_authenticity_score(self, features: Dict[str, float]) -> int:
        """Calculate authenticity score using rule-based approach"""
        score = 100  # Start with perfect score
        
        # Penalize suspicious weekend activity
        if features['weekend_commit_ratio'] > 0.4:
            penalty = (features['weekend_commit_ratio'] - 0.4) * 50
            score -= penalty
        
        # Penalize suspicious night activity
        if features['night_commit_ratio'] > 0.3:
            penalty = (features['night_commit_ratio'] - 0.3) * 40
            score -= penalty
        
        # Penalize low original content
        if features['original_repo_ratio'] < 0.5:
            penalty = (0.5 - features['original_repo_ratio']) * 30
            score -= penalty
        
        # Penalize low activity consistency
        if features['activity_consistency'] < 0.5:
            penalty = (0.5 - features['activity_consistency']) * 25
            score -= penalty
        
        # Penalize extreme follower ratios
        if features['follower_repo_ratio'] < 0.1 or features['follower_repo_ratio'] > 5:
            score -= 15
        
        # Penalize low language diversity
        if features['language_diversity'] < 2:
            score -= 10
        
        # Penalize extreme commit frequencies
        if features['commit_frequency'] < 5 or features['commit_frequency'] > 100:
            score -= 20
        
        return max(0, min(100, int(score)))
    
    def _calculate_confidence(self, github_data: Dict, features: Dict) -> int:
        """Calculate confidence based on data quality and quantity"""
        confidence = 50  # Base confidence
        
        commits = github_data.get('commits', [])
        repos = github_data.get('repositories', [])
        account_age = github_data.get('account_age_days', 0)
        
        # More data = higher confidence
        if len(commits) > 50:
            confidence += 20
        elif len(commits) > 20:
            confidence += 10
        
        if len(repos) > 10:
            confidence += 15
        elif len(repos) > 5:
            confidence += 10
        
        # Older accounts = higher confidence
        if account_age > 365:
            confidence += 15
        elif account_age > 180:
            confidence += 10
        
        return max(50, min(100, confidence))
    
    def _is_weekend(self, date_str: str) -> bool:
        """Check if commit was made on weekend"""
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date.weekday() >= 5
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
            return 0.5
        
        # Group commits by week
        weekly_commits = {}
        for commit in commits:
            try:
                date = datetime.fromisoformat(commit.get('date', '').replace('Z', '+00:00'))
                week = date.isocalendar()[1]
                weekly_commits[week] = weekly_commits.get(week, 0) + 1
            except:
                continue
        
        if not weekly_commits:
            return 0.0
        
        # Calculate coefficient of variation
        commit_counts = list(weekly_commits.values())
        mean_commits = np.mean(commit_counts)
        std_commits = np.std(commit_counts)
        
        if mean_commits == 0:
            return 0.0
        
        cv = std_commits / mean_commits
        consistency = max(0, 1 - cv)
        return min(1.0, consistency)
    
    def _generate_red_flags(self, features: Dict, github_data: Dict) -> List[RedFlag]:
        """Generate red flags based on analysis"""
        red_flags = []
        
        # High weekend commit ratio
        if features['weekend_commit_ratio'] > 0.4:
            red_flags.append(RedFlag(
                id="weekend_commits",
                title="Suspicious Weekend Activity",
                description=f"{features['weekend_commit_ratio']:.1%} of commits on weekends",
                severity="high" if features['weekend_commit_ratio'] > 0.6 else "medium",
                details="Authentic developers typically commit less on weekends. High weekend activity may indicate automated commits."
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
        
        # Extreme follower ratios
        if features['follower_repo_ratio'] < 0.1:
            red_flags.append(RedFlag(
                id="low_engagement",
                title="Low Social Engagement",
                description="Very few followers relative to repository count",
                severity="low",
                details="Authentic developers typically have some social engagement with their work."
            ))
        elif features['follower_repo_ratio'] > 5:
            red_flags.append(RedFlag(
                id="high_engagement",
                title="Unusually High Social Engagement",
                description="Very high follower to repository ratio",
                severity="low",
                details="This could indicate purchased followers or viral content."
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
        """Check if analyzer is ready"""
        return self.model_loaded