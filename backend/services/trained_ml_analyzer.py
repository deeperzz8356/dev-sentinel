import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import Counter

from models.analysis_models import ProfileAnalysis, RedFlag, MetricData, ComprehensiveFeatures, RepositoryHealth, ActivityPatterns, RepositoryInfo

class TrainedMLAnalyzer:
    """
    ML Analyzer using trained scikit-learn models
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = []
        self.model_metadata = {}
        self.model_loaded = False
        self._load_trained_model()
    
    def _load_trained_model(self):
        """Load the trained ML model and scaler"""
        model_path = "models/authenticity_model.joblib"
        scaler_path = "models/scaler.joblib"
        metadata_path = "models/model_metadata.json"
        
        try:
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                # Load model and scaler
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                
                # Load metadata
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        self.model_metadata = json.load(f)
                    self.feature_names = self.model_metadata.get('feature_names', [])
                
                self.model_loaded = True
                print(f"✅ Loaded trained {self.model_metadata.get('model_type', 'ML')} model")
                print(f"📊 Model AUC: {self.model_metadata.get('test_auc', 'Unknown')}")
                
            else:
                print("⚠️  No trained model found. Using fallback rule-based analysis.")
                print("To train a model, run: python ml_training/train_model.py")
                self.model_loaded = False
                
        except Exception as e:
            print(f"❌ Error loading trained model: {e}")
            print("⚠️  Falling back to rule-based analysis.")
            self.model_loaded = False
    
    def analyze_profile(self, github_data: Dict) -> ProfileAnalysis:
        """Main analysis function using trained ML model"""
        
        # Extract features from GitHub data
        features = self._extract_features(github_data)
        
        if self.model_loaded and self.model is not None:
            # Use trained ML model
            authenticity_score, confidence = self._predict_with_ml_model(features)
        else:
            # Fallback to rule-based analysis
            authenticity_score, confidence = self._predict_with_rules(features)
        
        # Generate red flags
        red_flags = self._generate_red_flags(features, github_data)
        
        # Generate metrics
        metrics = self._generate_metrics(github_data, features)
        
        # Generate comprehensive features object
        comprehensive_features = ComprehensiveFeatures(**features)
        
        # Generate repository health data
        repository_health = self._generate_repository_health(github_data)
        
        # Generate activity patterns
        activity_patterns = self._generate_activity_patterns(github_data)
        
        return ProfileAnalysis(
            username=github_data['username'],
            authenticity_score=authenticity_score,
            confidence=confidence,
            red_flags=red_flags,
            metrics=metrics,
            features=comprehensive_features,
            repository_health=repository_health,
            activity_patterns=activity_patterns,
            analysis_timestamp=datetime.now().isoformat()
        )
    
    def _predict_with_ml_model(self, features: Dict[str, float]) -> Tuple[int, int]:
        """Use trained ML model for prediction"""
        try:
            # Prepare features in correct order
            feature_vector = [features.get(name, 0) for name in self.feature_names]
            feature_array = np.array(feature_vector).reshape(1, -1)
            
            # Scale features if scaler is available
            if self.scaler is not None:
                feature_array = self.scaler.transform(feature_array)
            
            # Get prediction probability
            prediction_proba = self.model.predict_proba(feature_array)[0]
            authenticity_prob = prediction_proba[1]  # Probability of being authentic
            
            # Convert to score (0-100)
            authenticity_score = int(authenticity_prob * 100)
            
            # Calculate confidence based on prediction certainty
            confidence = int(max(prediction_proba) * 100)
            
            return authenticity_score, confidence
            
        except Exception as e:
            print(f"❌ ML prediction failed: {e}")
            # Fallback to rule-based
            return self._predict_with_rules(features)
    
    def _predict_with_rules(self, features: Dict[str, float]) -> Tuple[int, int]:
        """Fallback rule-based prediction"""
        score = 100  # Start with perfect score
        
        # Apply penalties for suspicious patterns
        if features['weekend_commit_ratio'] > 0.4:
            penalty = (features['weekend_commit_ratio'] - 0.4) * 50
            score -= penalty
        
        if features['night_commit_ratio'] > 0.3:
            penalty = (features['night_commit_ratio'] - 0.3) * 40
            score -= penalty
        
        if features['original_repo_ratio'] < 0.5:
            penalty = (0.5 - features['original_repo_ratio']) * 30
            score -= penalty
        
        if features['activity_consistency'] < 0.5:
            penalty = (0.5 - features['activity_consistency']) * 25
            score -= penalty
        
        if features['follower_repo_ratio'] < 0.1 or features['follower_repo_ratio'] > 5:
            score -= 15
        
        if features['language_diversity'] < 2:
            score -= 10
        
        if features['commit_frequency'] < 5 or features['commit_frequency'] > 100:
            score -= 20
        
        authenticity_score = max(0, min(100, int(score)))
        confidence = 75  # Fixed confidence for rule-based
        
        return authenticity_score, confidence
    
    def _extract_features(self, github_data: Dict) -> Dict[str, float]:
        """Extract comprehensive 23 ML features from GitHub data"""
        commits = github_data.get('commits', [])
        repos = github_data.get('repositories', [])
        user_data = github_data.get('user', {})
        
        # 1. Commit frequency (commits per year)
        commit_frequency = len(commits) / max(1, github_data.get('account_age_days', 1)) * 365
        
        # 2-3. Time-based patterns
        weekend_commits = sum(1 for c in commits if self._is_weekend(c.get('date', '')))
        weekend_commit_ratio = weekend_commits / max(1, len(commits))
        
        night_commits = sum(1 for c in commits if self._is_night_time(c.get('date', '')))
        night_commit_ratio = night_commits / max(1, len(commits))
        
        # 4. Repository patterns
        original_repos = sum(1 for r in repos if not r.get('fork', False))
        original_repo_ratio = original_repos / max(1, len(repos))
        
        # 5. Commit size variance
        commit_sizes = [c.get('additions', 0) + c.get('deletions', 0) for c in commits]
        commit_size_variance = np.var(commit_sizes) / (np.mean(commit_sizes) + 1) if commit_sizes else 0
        
        # 6. Activity consistency
        activity_consistency = self._calculate_activity_consistency(commits)
        
        # 7-8. Social metrics
        followers = user_data.get('followers', 0)
        following = user_data.get('following', 0)
        public_repos = user_data.get('public_repos', 1)
        follower_repo_ratio = followers / max(1, public_repos)
        follower_following_ratio = followers / max(1, following) if following > 0 else 0
        
        # 9. Language diversity
        languages = set()
        for repo in repos:
            if repo.get('language'):
                languages.add(repo['language'])
        language_diversity = len(languages)
        
        # 10. Repository health metrics
        total_stars = sum(r.get('stargazers_count', 0) for r in repos)
        total_forks = sum(r.get('forks_count', 0) for r in repos)
        avg_stars_per_repo = total_stars / max(1, len(repos))
        avg_forks_per_repo = total_forks / max(1, len(repos))
        
        # 11. Repository activity
        active_repos = sum(1 for r in repos if self._is_recently_active(r.get('updated_at', '')))
        repo_activity_ratio = active_repos / max(1, len(repos))
        
        # 12. Commit message quality
        commit_msg_quality = self._analyze_commit_messages(commits)
        
        # 13. Repository size distribution
        repo_sizes = [r.get('size', 0) for r in repos if r.get('size', 0) > 0]
        repo_size_variance = np.var(repo_sizes) / (np.mean(repo_sizes) + 1) if repo_sizes else 0
        
        # 14. Issue/PR engagement
        total_issues = sum(r.get('open_issues_count', 0) for r in repos)
        issue_engagement = total_issues / max(1, len(repos))
        
        # 15. Account age factor
        account_age_days = github_data.get('account_age_days', 1)
        account_maturity = min(1.0, account_age_days / 365)  # Normalized to 1 year
        
        # 16. Commit timing patterns
        hourly_distribution = self._analyze_hourly_patterns(commits)
        timing_entropy = self._calculate_entropy(hourly_distribution)
        
        # 17. Repository naming patterns
        repo_naming_quality = self._analyze_repo_names(repos)
        
        # 18. Contribution patterns
        contribution_diversity = self._analyze_contribution_types(commits)
        
        # 19. Profile completeness
        profile_completeness = self._calculate_profile_completeness(user_data)
        
        # 20. Repository collaboration
        collaboration_score = self._calculate_collaboration_score(repos)
        
        # 21. Code quality indicators
        code_quality_score = self._estimate_code_quality(repos, commits)
        
        # 22. Activity burst patterns
        burst_activity_score = self._detect_burst_patterns(commits)
        
        # 23. Repository maintenance
        maintenance_score = self._calculate_maintenance_score(repos)
        
        return {
            'commit_frequency': min(100, commit_frequency),
            'weekend_commit_ratio': weekend_commit_ratio,
            'night_commit_ratio': night_commit_ratio,
            'original_repo_ratio': original_repo_ratio,
            'commit_size_variance': min(1.0, commit_size_variance),
            'activity_consistency': activity_consistency,
            'follower_repo_ratio': min(10.0, follower_repo_ratio),
            'follower_following_ratio': min(10.0, follower_following_ratio),
            'language_diversity': min(15, language_diversity),
            'avg_stars_per_repo': min(100, avg_stars_per_repo),
            'avg_forks_per_repo': min(50, avg_forks_per_repo),
            'repo_activity_ratio': repo_activity_ratio,
            'commit_msg_quality': commit_msg_quality,
            'repo_size_variance': min(1.0, repo_size_variance),
            'issue_engagement': min(20, issue_engagement),
            'account_maturity': account_maturity,
            'timing_entropy': timing_entropy,
            'repo_naming_quality': repo_naming_quality,
            'contribution_diversity': contribution_diversity,
            'profile_completeness': profile_completeness,
            'collaboration_score': collaboration_score,
            'code_quality_score': code_quality_score,
            'burst_activity_score': burst_activity_score,
            'maintenance_score': maintenance_score
        }
    
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
    
    def _is_recently_active(self, updated_at: str) -> bool:
        """Check if repository was updated in last 6 months"""
        try:
            updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            six_months_ago = datetime.now() - timedelta(days=180)
            return updated_date > six_months_ago
        except:
            return False
    
    def _analyze_commit_messages(self, commits: List[Dict]) -> float:
        """Analyze commit message quality (0-1 score)"""
        if not commits:
            return 0.5
        
        quality_score = 0
        total_messages = 0
        
        for commit in commits:
            message = commit.get('message', '').strip()
            if not message:
                continue
            
            total_messages += 1
            score = 0
            
            # Length check (good messages are 10-72 chars)
            if 10 <= len(message) <= 72:
                score += 0.3
            
            # Capitalization
            if message[0].isupper():
                score += 0.2
            
            # No ending period
            if not message.endswith('.'):
                score += 0.2
            
            # Contains meaningful words (not just "update", "fix", etc.)
            meaningful_words = ['implement', 'add', 'create', 'refactor', 'optimize', 'enhance']
            if any(word in message.lower() for word in meaningful_words):
                score += 0.3
            
            quality_score += score
        
        return quality_score / max(1, total_messages)
    
    def _analyze_hourly_patterns(self, commits: List[Dict]) -> List[int]:
        """Analyze commit distribution across 24 hours"""
        hourly_counts = [0] * 24
        
        for commit in commits:
            try:
                date = datetime.fromisoformat(commit.get('date', '').replace('Z', '+00:00'))
                hourly_counts[date.hour] += 1
            except:
                continue
        
        return hourly_counts
    
    def _calculate_entropy(self, distribution: List[int]) -> float:
        """Calculate entropy of a distribution"""
        total = sum(distribution)
        if total == 0:
            return 0
        
        entropy = 0
        for count in distribution:
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        # Normalize to 0-1 range (max entropy for 24 hours is log2(24))
        return entropy / np.log2(24)
    
    def _analyze_repo_names(self, repos: List[Dict]) -> float:
        """Analyze repository naming quality"""
        if not repos:
            return 0.5
        
        quality_score = 0
        for repo in repos:
            name = repo.get('name', '').lower()
            score = 0
            
            # Avoid generic names
            generic_names = ['test', 'demo', 'sample', 'hello-world', 'untitled']
            if not any(generic in name for generic in generic_names):
                score += 0.4
            
            # Proper naming convention (kebab-case or snake_case)
            if '-' in name or '_' in name:
                score += 0.3
            
            # Reasonable length
            if 3 <= len(name) <= 30:
                score += 0.3
            
            quality_score += score
        
        return quality_score / len(repos)
    
    def _analyze_contribution_types(self, commits: List[Dict]) -> float:
        """Analyze diversity of contribution types"""
        if not commits:
            return 0.5
        
        # Categorize commits by type
        categories = {
            'feature': ['add', 'implement', 'create', 'new'],
            'fix': ['fix', 'bug', 'error', 'issue'],
            'refactor': ['refactor', 'clean', 'optimize', 'improve'],
            'docs': ['doc', 'readme', 'comment'],
            'style': ['style', 'format', 'lint'],
            'test': ['test', 'spec', 'coverage']
        }
        
        category_counts = {cat: 0 for cat in categories}
        
        for commit in commits:
            message = commit.get('message', '').lower()
            for category, keywords in categories.items():
                if any(keyword in message for keyword in keywords):
                    category_counts[category] += 1
                    break
        
        # Calculate diversity (how many categories are used)
        used_categories = sum(1 for count in category_counts.values() if count > 0)
        return used_categories / len(categories)
    
    def _calculate_profile_completeness(self, user_data: Dict) -> float:
        """Calculate profile completeness score"""
        score = 0
        max_score = 8
        
        # Check various profile fields
        if user_data.get('name'):
            score += 1
        if user_data.get('bio'):
            score += 1
        if user_data.get('location'):
            score += 1
        if user_data.get('company'):
            score += 1
        if user_data.get('blog'):
            score += 1
        if user_data.get('email'):
            score += 1
        if user_data.get('avatar_url'):
            score += 1
        if user_data.get('public_repos', 0) > 0:
            score += 1
        
        return score / max_score
    
    def _calculate_collaboration_score(self, repos: List[Dict]) -> float:
        """Calculate collaboration score based on forks and contributors"""
        if not repos:
            return 0.5
        
        collaboration_indicators = 0
        total_repos = len(repos)
        
        for repo in repos:
            # Has forks (others found it useful)
            if repo.get('forks_count', 0) > 0:
                collaboration_indicators += 0.5
            
            # Has stars (community engagement)
            if repo.get('stargazers_count', 0) > 0:
                collaboration_indicators += 0.3
            
            # Has issues (active discussion)
            if repo.get('open_issues_count', 0) > 0:
                collaboration_indicators += 0.2
        
        return min(1.0, collaboration_indicators / total_repos)
    
    def _estimate_code_quality(self, repos: List[Dict], commits: List[Dict]) -> float:
        """Estimate code quality based on various indicators"""
        quality_score = 0.5  # Base score
        
        # Repository indicators
        if repos:
            # Repositories with descriptions
            described_repos = sum(1 for r in repos if r.get('description'))
            if described_repos / len(repos) > 0.5:
                quality_score += 0.2
            
            # Repositories with README (indicated by size > 0)
            documented_repos = sum(1 for r in repos if r.get('size', 0) > 10)
            if documented_repos / len(repos) > 0.3:
                quality_score += 0.2
        
        # Commit indicators
        if commits:
            # Reasonable commit sizes (not too large, not too small)
            reasonable_commits = 0
            for commit in commits:
                size = commit.get('additions', 0) + commit.get('deletions', 0)
                if 5 <= size <= 500:  # Reasonable change size
                    reasonable_commits += 1
            
            if reasonable_commits / len(commits) > 0.6:
                quality_score += 0.1
        
        return min(1.0, quality_score)
    
    def _detect_burst_patterns(self, commits: List[Dict]) -> float:
        """Detect unusual burst patterns in commits"""
        if len(commits) < 10:
            return 0.5
        
        # Group commits by day
        daily_commits = {}
        for commit in commits:
            try:
                date = datetime.fromisoformat(commit.get('date', '').replace('Z', '+00:00'))
                day_key = date.strftime('%Y-%m-%d')
                daily_commits[day_key] = daily_commits.get(day_key, 0) + 1
            except:
                continue
        
        if not daily_commits:
            return 0.5
        
        commit_counts = list(daily_commits.values())
        mean_commits = np.mean(commit_counts)
        
        # Count days with unusually high activity (>3x average)
        burst_days = sum(1 for count in commit_counts if count > mean_commits * 3)
        burst_ratio = burst_days / len(commit_counts)
        
        # Lower score indicates more suspicious burst patterns
        return max(0, 1 - burst_ratio * 2)
    
    def _calculate_maintenance_score(self, repos: List[Dict]) -> float:
        """Calculate repository maintenance score"""
        if not repos:
            return 0.5
        
        maintenance_score = 0
        for repo in repos:
            score = 0
            
            # Recently updated
            if self._is_recently_active(repo.get('updated_at', '')):
                score += 0.4
            
            # Has releases/tags (indicates versioning)
            if repo.get('has_releases', False):
                score += 0.3
            
            # Not archived
            if not repo.get('archived', False):
                score += 0.3
            
            maintenance_score += score
        
        return maintenance_score / len(repos)
    
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
        
        # ML model specific red flag
        if self.model_loaded and hasattr(self, 'model'):
            try:
                feature_vector = [features.get(name, 0) for name in self.feature_names]
                feature_array = np.array(feature_vector).reshape(1, -1)
                
                if self.scaler is not None:
                    feature_array = self.scaler.transform(feature_array)
                
                prediction_proba = self.model.predict_proba(feature_array)[0]
                suspicious_prob = prediction_proba[0]
                
                if suspicious_prob > 0.7:  # High probability of being suspicious
                    red_flags.append(RedFlag(
                        id="ml_suspicious",
                        title="ML Model Alert",
                        description=f"ML model indicates {suspicious_prob:.1%} probability of suspicious activity",
                        severity="high",
                        details=f"Our trained {self.model_metadata.get('model_type', 'ML')} model has identified patterns consistent with inauthentic profiles."
                    ))
            except:
                pass  # Ignore ML-specific errors
        
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
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            'model_loaded': self.model_loaded,
            'model_type': self.model_metadata.get('model_type', 'Rule-based'),
            'trained_at': self.model_metadata.get('trained_at', 'N/A'),
            'test_auc': self.model_metadata.get('test_auc', 'N/A'),
            'features': self.feature_names
        }
    def _generate_repository_health(self, github_data: Dict) -> RepositoryHealth:
        """Generate repository health metrics"""
        repos = github_data.get('repositories', [])
        
        if not repos:
            return RepositoryHealth(
                total_repositories=0,
                active_repositories=0,
                forked_repositories=0,
                original_repositories=0,
                starred_repositories=0,
                average_repo_size=0,
                languages_used=[],
                top_repositories=[]
            )
        
        # Calculate repository metrics
        active_repos = sum(1 for r in repos if self._is_recently_active(r.get('updated_at', '')))
        forked_repos = sum(1 for r in repos if r.get('fork', False))
        original_repos = len(repos) - forked_repos
        starred_repos = sum(1 for r in repos if r.get('stargazers_count', 0) > 0)
        
        # Calculate average repository size
        repo_sizes = [r.get('size', 0) for r in repos]
        avg_size = sum(repo_sizes) / len(repo_sizes) if repo_sizes else 0
        
        # Get unique languages
        languages = list(set(r.get('language') for r in repos if r.get('language')))
        
        # Get top repositories by stars
        sorted_repos = sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)
        top_repos = []
        
        for repo in sorted_repos[:10]:  # Top 10 repositories
            top_repos.append(RepositoryInfo(
                name=repo.get('name', ''),
                stars=repo.get('stargazers_count', 0),
                forks=repo.get('forks_count', 0),
                language=repo.get('language'),
                last_updated=repo.get('updated_at', '')
            ))
        
        return RepositoryHealth(
            total_repositories=len(repos),
            active_repositories=active_repos,
            forked_repositories=forked_repos,
            original_repositories=original_repos,
            starred_repositories=starred_repos,
            average_repo_size=avg_size,
            languages_used=languages,
            top_repositories=top_repos
        )
    
    def _generate_activity_patterns(self, github_data: Dict) -> ActivityPatterns:
        """Generate activity pattern analysis"""
        commits = github_data.get('commits', [])
        repos = github_data.get('repositories', [])
        
        # Initialize distributions
        hourly_dist = [0] * 24
        daily_dist = [0] * 7  # Monday = 0, Sunday = 6
        monthly_dist = [0] * 12
        commit_sizes = []
        
        # Analyze commit patterns
        for commit in commits:
            try:
                date = datetime.fromisoformat(commit.get('date', '').replace('Z', '+00:00'))
                hourly_dist[date.hour] += 1
                daily_dist[date.weekday()] += 1
                monthly_dist[date.month - 1] += 1
                
                # Commit size
                size = commit.get('additions', 0) + commit.get('deletions', 0)
                commit_sizes.append(size)
            except:
                continue
        
        # Create commit size distribution (buckets)
        size_buckets = [0] * 10  # 10 buckets for different size ranges
        for size in commit_sizes:
            if size == 0:
                bucket = 0
            elif size <= 5:
                bucket = 1
            elif size <= 20:
                bucket = 2
            elif size <= 50:
                bucket = 3
            elif size <= 100:
                bucket = 4
            elif size <= 200:
                bucket = 5
            elif size <= 500:
                bucket = 6
            elif size <= 1000:
                bucket = 7
            elif size <= 2000:
                bucket = 8
            else:
                bucket = 9
            size_buckets[bucket] += 1
        
        # Language distribution
        lang_dist = {}
        for repo in repos:
            lang = repo.get('language')
            if lang:
                lang_dist[lang] = lang_dist.get(lang, 0) + 1
        
        # Contribution types (based on commit messages)
        contribution_types = {
            'features': 0,
            'fixes': 0,
            'refactoring': 0,
            'documentation': 0,
            'testing': 0,
            'other': 0
        }
        
        for commit in commits:
            message = commit.get('message', '').lower()
            if any(word in message for word in ['add', 'implement', 'create', 'new']):
                contribution_types['features'] += 1
            elif any(word in message for word in ['fix', 'bug', 'error', 'issue']):
                contribution_types['fixes'] += 1
            elif any(word in message for word in ['refactor', 'clean', 'optimize']):
                contribution_types['refactoring'] += 1
            elif any(word in message for word in ['doc', 'readme', 'comment']):
                contribution_types['documentation'] += 1
            elif any(word in message for word in ['test', 'spec', 'coverage']):
                contribution_types['testing'] += 1
            else:
                contribution_types['other'] += 1
        
        return ActivityPatterns(
            hourly_distribution=hourly_dist,
            daily_distribution=daily_dist,
            monthly_distribution=monthly_dist,
            commit_size_distribution=size_buckets,
            language_distribution=lang_dist,
            contribution_types=contribution_types
        )