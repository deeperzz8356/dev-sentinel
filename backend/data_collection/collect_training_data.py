#!/usr/bin/env python3
"""
Enhanced Data collection script for training the ML model
Collects comprehensive GitHub profiles and labels them for training
"""

import os
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sys
import requests
from collections import Counter
import re
sys.path.append('..')

from services.github_service import GitHubService
from services.trained_ml_analyzer import TrainedMLAnalyzer

class EnhancedTrainingDataCollector:
    def __init__(self, github_token: str = None):
        self.github_service = GitHubService(token=github_token)
        self.analyzer = TrainedMLAnalyzer()
        self.data = []
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = None
        
    def get_rate_limit_info(self):
        """Check GitHub API rate limit status"""
        try:
            response = requests.get(
                'https://api.github.com/rate_limit',
                headers={'Authorization': f'token {self.github_service.token}'} if self.github_service.token else {}
            )
            if response.status_code == 200:
                data = response.json()
                self.rate_limit_remaining = data['rate']['remaining']
                self.rate_limit_reset = datetime.fromtimestamp(data['rate']['reset'])
                print(f"📊 Rate limit: {self.rate_limit_remaining} requests remaining")
                return True
        except Exception as e:
            print(f"⚠️  Could not check rate limit: {e}")
        return False
    
    def wait_for_rate_limit(self):
        """Wait if rate limit is low"""
        if self.rate_limit_remaining < 100:
            if self.rate_limit_reset:
                wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
                if wait_time > 0:
                    print(f"⏳ Rate limit low. Waiting {wait_time/60:.1f} minutes...")
                    time.sleep(min(wait_time, 3600))  # Max 1 hour wait
    
    def extract_comprehensive_features(self, github_data: Dict, username: str) -> Dict:
        """Extract comprehensive features for ML training"""
        try:
            commits = github_data.get('commits', [])
            repos = github_data.get('repositories', [])
            user_data = github_data.get('user', {})
            
            # Basic user metrics
            features = {
                'username': username,
                'account_age_days': github_data.get('account_age_days', 0),
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'public_gists': user_data.get('public_gists', 0),
                'total_commits': len(commits),
                'total_repositories': len(repos)
            }
            
            # Profile completeness
            profile_fields = ['name', 'bio', 'location', 'company', 'blog', 'email']
            profile_completeness = sum(1 for field in profile_fields if user_data.get(field))
            features['profile_completeness'] = profile_completeness / len(profile_fields)
            
            # Temporal patterns
            if commits:
                features.update(self._extract_temporal_features(commits))
            else:
                features.update(self._get_default_temporal_features())
            
            # Repository features
            if repos:
                features.update(self._extract_repository_features(repos))
            else:
                features.update(self._get_default_repository_features())
            
            # Social features
            features.update(self._extract_social_features(user_data, repos))
            
            # Activity patterns
            features.update(self._extract_activity_patterns(commits, repos))
            
            # Code quality indicators
            features.update(self._extract_code_quality_features(repos, commits))
            
            return features
            
        except Exception as e:
            print(f"❌ Error extracting features for {username}: {e}")
            return self._get_default_features(username)
    
    def _extract_temporal_features(self, commits: List[Dict]) -> Dict:
        """Extract temporal pattern features"""
        if not commits:
            return self._get_default_temporal_features()
        
        # Parse commit dates
        commit_dates = []
        hourly_dist = [0] * 24
        daily_dist = [0] * 7
        
        for commit in commits:
            try:
                date_str = commit.get('date', '')
                if date_str:
                    date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    commit_dates.append(date)
                    hourly_dist[date.hour] += 1
                    daily_dist[date.weekday()] += 1
            except:
                continue
        
        if not commit_dates:
            return self._get_default_temporal_features()
        
        # Calculate temporal features
        weekend_commits = sum(daily_dist[5:])  # Saturday + Sunday
        total_commits = len(commit_dates)
        weekend_ratio = weekend_commits / total_commits if total_commits > 0 else 0
        
        # Night commits (10 PM - 6 AM)
        night_commits = sum(hourly_dist[22:24]) + sum(hourly_dist[0:6])
        night_ratio = night_commits / total_commits if total_commits > 0 else 0
        
        # Commit frequency
        if commit_dates:
            date_range = (max(commit_dates) - min(commit_dates)).days
            commit_frequency = len(commit_dates) / max(1, date_range) * 365
        else:
            commit_frequency = 0
        
        # Activity consistency (coefficient of variation of daily commits)
        daily_counts = list(daily_dist)
        if sum(daily_counts) > 0:
            mean_daily = np.mean(daily_counts)
            std_daily = np.std(daily_counts)
            activity_consistency = 1 - (std_daily / mean_daily) if mean_daily > 0 else 0
        else:
            activity_consistency = 0
        
        # Timing entropy
        total_hourly = sum(hourly_dist)
        if total_hourly > 0:
            entropy = 0
            for count in hourly_dist:
                if count > 0:
                    p = count / total_hourly
                    entropy -= p * np.log2(p)
            timing_entropy = entropy / np.log2(24)  # Normalize
        else:
            timing_entropy = 0
        
        # Burst activity detection
        if len(commit_dates) > 10:
            # Group by day and find burst patterns
            daily_commits = {}
            for date in commit_dates:
                day_key = date.strftime('%Y-%m-%d')
                daily_commits[day_key] = daily_commits.get(day_key, 0) + 1
            
            daily_counts = list(daily_commits.values())
            mean_daily = np.mean(daily_counts)
            burst_days = sum(1 for count in daily_counts if count > mean_daily * 3)
            burst_ratio = burst_days / len(daily_counts)
            burst_activity_score = max(0, 1 - burst_ratio * 2)
        else:
            burst_activity_score = 0.5
        
        return {
            'weekend_commit_ratio': weekend_ratio,
            'night_commit_ratio': night_ratio,
            'commit_frequency': min(200, commit_frequency),
            'activity_consistency': max(0, min(1, activity_consistency)),
            'timing_entropy': timing_entropy,
            'burst_activity_score': burst_activity_score
        }
    
    def _extract_repository_features(self, repos: List[Dict]) -> Dict:
        """Extract repository-related features"""
        if not repos:
            return self._get_default_repository_features()
        
        # Basic repository metrics
        total_repos = len(repos)
        forked_repos = sum(1 for r in repos if r.get('fork', False))
        original_repos = total_repos - forked_repos
        original_ratio = original_repos / total_repos if total_repos > 0 else 0
        
        # Repository activity
        recently_active = sum(1 for r in repos if self._is_recently_active(r.get('updated_at', '')))
        activity_ratio = recently_active / total_repos if total_repos > 0 else 0
        
        # Stars and forks
        total_stars = sum(r.get('stargazers_count', 0) for r in repos)
        total_forks = sum(r.get('forks_count', 0) for r in repos)
        avg_stars = total_stars / total_repos if total_repos > 0 else 0
        avg_forks = total_forks / total_repos if total_repos > 0 else 0
        
        # Language diversity
        languages = set()
        for repo in repos:
            lang = repo.get('language')
            if lang:
                languages.add(lang)
        language_diversity = len(languages)
        
        # Repository sizes
        repo_sizes = [r.get('size', 0) for r in repos if r.get('size', 0) > 0]
        if repo_sizes:
            avg_repo_size = np.mean(repo_sizes)
            repo_size_variance = np.var(repo_sizes) / (np.mean(repo_sizes) + 1)
        else:
            avg_repo_size = 0
            repo_size_variance = 0
        
        # Repository naming quality
        repo_names = [r.get('name', '') for r in repos]
        naming_quality = self._analyze_repo_naming_quality(repo_names)
        
        # Issues and engagement
        total_issues = sum(r.get('open_issues_count', 0) for r in repos)
        avg_issues = total_issues / total_repos if total_repos > 0 else 0
        
        # Archived repositories
        archived_repos = sum(1 for r in repos if r.get('archived', False))
        archived_ratio = archived_repos / total_repos if total_repos > 0 else 0
        
        return {
            'original_repo_ratio': original_ratio,
            'fork_ratio': 1 - original_ratio,
            'repo_activity_ratio': activity_ratio,
            'avg_stars_per_repo': min(100, avg_stars),
            'avg_forks_per_repo': min(50, avg_forks),
            'language_diversity': min(15, language_diversity),
            'avg_repo_size': min(10000, avg_repo_size),
            'repo_size_variance': min(1, repo_size_variance),
            'repo_naming_quality': naming_quality,
            'avg_issues_per_repo': min(20, avg_issues),
            'archived_repo_ratio': archived_ratio,
            'zero_star_repo_ratio': sum(1 for r in repos if r.get('stargazers_count', 0) == 0) / total_repos
        }
    
    def _extract_social_features(self, user_data: Dict, repos: List[Dict]) -> Dict:
        """Extract social behavior features"""
        followers = user_data.get('followers', 0)
        following = user_data.get('following', 0)
        public_repos = max(1, user_data.get('public_repos', 1))
        
        # Social ratios
        follower_repo_ratio = followers / public_repos
        follower_following_ratio = followers / max(1, following) if following > 0 else 0
        
        # Engagement metrics
        total_stars = sum(r.get('stargazers_count', 0) for r in repos) if repos else 0
        total_forks = sum(r.get('forks_count', 0) for r in repos) if repos else 0
        
        return {
            'follower_repo_ratio': min(20, follower_repo_ratio),
            'follower_following_ratio': min(10, follower_following_ratio),
            'total_stars_received': min(1000, total_stars),
            'total_forks_received': min(500, total_forks),
            'public_gist_count': min(100, user_data.get('public_gists', 0))
        }
    
    def _extract_activity_patterns(self, commits: List[Dict], repos: List[Dict]) -> Dict:
        """Extract activity pattern features"""
        # Commit patterns
        if commits:
            commit_sizes = []
            commit_messages = []
            
            for commit in commits:
                # Commit size
                additions = commit.get('additions', 0)
                deletions = commit.get('deletions', 0)
                total_changes = additions + deletions
                commit_sizes.append(total_changes)
                
                # Commit message
                message = commit.get('message', '')
                commit_messages.append(message)
            
            # Commit size analysis
            if commit_sizes:
                avg_commit_size = np.mean(commit_sizes)
                commit_size_variance = np.var(commit_sizes) / (avg_commit_size + 1)
                large_commits = sum(1 for size in commit_sizes if size > 500)
                large_commit_ratio = large_commits / len(commit_sizes)
                trivial_commits = sum(1 for size in commit_sizes if size < 5)
                trivial_commit_ratio = trivial_commits / len(commit_sizes)
            else:
                avg_commit_size = 0
                commit_size_variance = 0
                large_commit_ratio = 0
                trivial_commit_ratio = 0
            
            # Commit message analysis
            if commit_messages:
                avg_msg_length = np.mean([len(msg) for msg in commit_messages])
                empty_messages = sum(1 for msg in commit_messages if len(msg.strip()) < 3)
                empty_commit_ratio = empty_messages / len(commit_messages)
            else:
                avg_msg_length = 0
                empty_commit_ratio = 0
        else:
            avg_commit_size = 0
            commit_size_variance = 0
            large_commit_ratio = 0
            trivial_commit_ratio = 0
            avg_msg_length = 0
            empty_commit_ratio = 0
        
        # Repository contribution patterns
        if repos:
            contributions_per_repo = len(commits) / len(repos) if repos else 0
        else:
            contributions_per_repo = 0
        
        return {
            'avg_commit_size': min(1000, avg_commit_size),
            'commit_size_variance': min(1, commit_size_variance),
            'large_commit_ratio': large_commit_ratio,
            'trivial_commit_ratio': trivial_commit_ratio,
            'commit_message_length_avg': min(200, avg_msg_length),
            'empty_commit_ratio': empty_commit_ratio,
            'contributions_per_repo': min(100, contributions_per_repo)
        }
    
    def _extract_code_quality_features(self, repos: List[Dict], commits: List[Dict]) -> Dict:
        """Extract code quality indicators"""
        if not repos:
            return {
                'has_readme_ratio': 0,
                'has_license_ratio': 0,
                'maintenance_score': 0
            }
        
        # Documentation indicators
        readme_repos = sum(1 for r in repos if r.get('size', 0) > 10)  # Proxy for README
        readme_ratio = readme_repos / len(repos)
        
        # License indicators (proxy)
        license_repos = sum(1 for r in repos if r.get('license'))
        license_ratio = license_repos / len(repos) if repos else 0
        
        # Maintenance score
        active_repos = sum(1 for r in repos if self._is_recently_active(r.get('updated_at', '')))
        maintenance_score = active_repos / len(repos) if repos else 0
        
        return {
            'has_readme_ratio': readme_ratio,
            'has_license_ratio': license_ratio,
            'maintenance_score': maintenance_score
        }
    
    def _is_recently_active(self, updated_at: str) -> bool:
        """Check if repository was updated in last 6 months"""
        try:
            updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            six_months_ago = datetime.now() - timedelta(days=180)
            return updated_date > six_months_ago
        except:
            return False
    
    def _analyze_repo_naming_quality(self, repo_names: List[str]) -> float:
        """Analyze repository naming quality"""
        if not repo_names:
            return 0.5
        
        quality_score = 0
        for name in repo_names:
            score = 0
            name_lower = name.lower()
            
            # Avoid generic names
            generic_names = ['test', 'demo', 'sample', 'hello-world', 'untitled', 'new-repo']
            if not any(generic in name_lower for generic in generic_names):
                score += 0.4
            
            # Proper naming convention
            if '-' in name or '_' in name:
                score += 0.3
            
            # Reasonable length
            if 3 <= len(name) <= 30:
                score += 0.3
            
            quality_score += score
        
        return quality_score / len(repo_names)
    
    def _get_default_temporal_features(self) -> Dict:
        """Default temporal features for profiles with no commits"""
        return {
            'weekend_commit_ratio': 0,
            'night_commit_ratio': 0,
            'commit_frequency': 0,
            'activity_consistency': 0,
            'timing_entropy': 0,
            'burst_activity_score': 0.5
        }
    
    def _get_default_repository_features(self) -> Dict:
        """Default repository features for profiles with no repos"""
        return {
            'original_repo_ratio': 0,
            'fork_ratio': 0,
            'repo_activity_ratio': 0,
            'avg_stars_per_repo': 0,
            'avg_forks_per_repo': 0,
            'language_diversity': 0,
            'avg_repo_size': 0,
            'repo_size_variance': 0,
            'repo_naming_quality': 0.5,
            'avg_issues_per_repo': 0,
            'archived_repo_ratio': 0,
            'zero_star_repo_ratio': 1
        }
    
    def _get_default_features(self, username: str) -> Dict:
        """Get default features for failed extractions"""
        features = {
            'username': username,
            'account_age_days': 0,
            'public_repos': 0,
            'followers': 0,
            'following': 0,
            'public_gists': 0,
            'total_commits': 0,
            'total_repositories': 0,
            'profile_completeness': 0,
            'follower_repo_ratio': 0,
            'follower_following_ratio': 0,
            'total_stars_received': 0,
            'total_forks_received': 0,
            'public_gist_count': 0,
            'avg_commit_size': 0,
            'commit_size_variance': 0,
            'large_commit_ratio': 0,
            'trivial_commit_ratio': 0,
            'commit_message_length_avg': 0,
            'empty_commit_ratio': 0,
            'contributions_per_repo': 0,
            'has_readme_ratio': 0,
            'has_license_ratio': 0,
            'maintenance_score': 0
        }
        features.update(self._get_default_temporal_features())
        features.update(self._get_default_repository_features())
        return features
        
    def collect_authentic_profiles(self) -> List[Dict]:
        """
        Collect known authentic developer profiles with comprehensive data extraction
        """
        # Expanded list of authentic developers
        authentic_users = [
            # Linux/Kernel developers
            "torvalds",      # Linus Torvalds - Linux creator
            "gregkh",        # Greg Kroah-Hartman - Linux stable maintainer
            
            # JavaScript/Node.js ecosystem
            "tj",            # TJ Holowaychuk - Express.js
            "sindresorhus",  # Sindre Sorhus - Popular OSS maintainer
            "addyosmani",    # Addy Osmani - Google Chrome team
            "paulirish",     # Paul Irish - Google Chrome team
            "kentcdodds",    # Kent C. Dodds - Testing expert
            "wesbos",        # Wes Bos - JavaScript teacher
            "getify",        # Kyle Simpson - You Don't Know JS
            "ryanflorence",  # Ryan Florence - React Router
            "mjackson",      # Michael Jackson - React Router
            
            # React ecosystem
            "gaearon",       # Dan Abramov - React team
            "sebmarkbage",   # Sebastian Markbåge - React team
            "acdlite",       # Andrew Clark - React team
            "sophiebits",    # Sophie Alpert - Former React team lead
            
            # GitHub founders/early employees
            "defunkt",       # Chris Wanstrath - GitHub co-founder
            "mojombo",       # Tom Preston-Werner - GitHub co-founder
            "pjhyett",       # PJ Hyett - GitHub co-founder
            
            # CSS/Frontend
            "mdo",           # Mark Otto - Bootstrap creator
            "fat",           # Jacob Thornton - Bootstrap co-creator
            "necolas",       # Nicolas Gallagher - Normalize.css
            
            # Python ecosystem
            "gvanrossum",    # Guido van Rossum - Python creator
            "kennethreitz",  # Kenneth Reitz - Requests library
            "mitsuhiko",     # Armin Ronacher - Flask creator
            
            # Ruby ecosystem
            "dhh",           # David Heinemeier Hansson - Rails creator
            "tenderlove",    # Aaron Patterson - Rails core team
            "wycats",        # Yehuda Katz - Ember.js, jQuery
            
            # Go ecosystem
            "bradfitz",      # Brad Fitzpatrick - Go team
            "robpike",       # Rob Pike - Go co-creator
            
            # Security/DevOps
            "jessfraz",      # Jessie Frazelle - Docker/Kubernetes
            "kelseyhightower", # Kelsey Hightower - Kubernetes
            
            # Machine Learning/AI
            "fchollet",      # François Chollet - Keras creator
            "karpathy",      # Andrej Karpathy - AI researcher
            
            # Database/Systems
            "antirez",       # Salvatore Sanfilippo - Redis creator
            
            # Mobile development
            "JakeWharton",   # Jake Wharton - Android libraries
            
            # Educators/Content creators
            "bradtraversy",  # Brad Traversy - Web dev educator
            "mpj",           # Mattias Petter Johansson - FunFunFunction
            
            # Compiler/Language designers
            "lattner",       # Chris Lattner - Swift/LLVM
            
            # Additional verified developers
            "holman",        # Zach Holman - GitHub
            "jashkenas",     # Jeremy Ashkenas - Backbone.js, CoffeeScript
            "isaacs",        # Isaac Schlueter - npm
            "substack",      # James Halliday - Browserify
            "mikeal",        # Mikeal Rogers - Request
            "dominictarr",   # Dominic Tarr - Streams
            "maxogden",      # Max Ogden - Dat project
            "feross",        # Feross Aboukhadijeh - WebTorrent
            "rauchg",        # Guillermo Rauch - Vercel/Next.js
        ]
        
        print(f"🔍 Collecting {len(authentic_users)} authentic profiles with comprehensive data...")
        return self._collect_profiles_with_features(authentic_users, label=1)
    
    def collect_suspicious_profiles(self) -> List[Dict]:
        """
        Collect potentially suspicious profiles
        Note: In production, you would have a curated list of verified suspicious accounts
        """
        # For demonstration, we'll generate synthetic suspicious data
        # In production, you'd manually curate suspicious profiles
        print("⚠️  Generating synthetic suspicious profiles for training...")
        return self.generate_synthetic_suspicious_data(50)
    
    def collect_borderline_profiles(self) -> List[Dict]:
        """
        Collect borderline/edge case profiles that are harder to classify
        These help the model learn nuanced patterns
        """
        borderline_users = [
            # New but legitimate developers
            # Inactive but authentic accounts  
            # Developers with unusual but legitimate patterns
            # Note: You would manually curate these based on analysis
        ]
        
        # For now, we'll create some synthetic borderline cases
        print("🔄 Generating borderline cases for robust training...")
        return self.generate_borderline_cases(25)
    
    def _collect_profiles_with_features(self, usernames: List[str], label: int) -> List[Dict]:
        """Collect profile data with comprehensive feature extraction"""
        profiles = []
        failed_profiles = []
        
        for i, username in enumerate(usernames):
            try:
                print(f"📊 Collecting {username} ({i+1}/{len(usernames)})...")
                
                # Check rate limit
                if i % 10 == 0:  # Check every 10 requests
                    self.get_rate_limit_info()
                    self.wait_for_rate_limit()
                
                # Get GitHub data
                github_data = self.github_service.get_profile_data(username)
                
                if not github_data or not github_data.get('user'):
                    print(f"⚠️  No data found for {username}")
                    failed_profiles.append(username)
                    continue
                
                # Extract comprehensive features
                features = self.extract_comprehensive_features(github_data, username)
                
                # Add label
                features['label'] = label
                features['collected_at'] = datetime.now().isoformat()
                
                profiles.append(features)
                
                # Log collection success
                commits_count = len(github_data.get('commits', []))
                repos_count = len(github_data.get('repositories', []))
                print(f"✅ {username}: {commits_count} commits, {repos_count} repos, {features.get('followers', 0)} followers")
                
                # Rate limiting - be respectful to GitHub API
                time.sleep(1.5)  # 1.5 second delay between requests
                
            except Exception as e:
                print(f"❌ Failed to collect {username}: {e}")
                failed_profiles.append(username)
                continue
        
        if failed_profiles:
            print(f"⚠️  Failed to collect {len(failed_profiles)} profiles: {failed_profiles}")
        
        return profiles
    
    def generate_synthetic_suspicious_data(self, count: int = 50) -> List[Dict]:
        """
        Generate synthetic suspicious profile data based on real patterns
        """
        import random
        import numpy as np
        
        print(f"🤖 Generating {count} synthetic suspicious profiles with realistic patterns...")
        
        suspicious_profiles = []
        
        for i in range(count):
            # Create different types of suspicious patterns
            pattern_type = random.choice(['bot_like', 'fake_engagement', 'content_farm', 'inactive_fake'])
            
            if pattern_type == 'bot_like':
                # Bot-like patterns: very regular, high weekend/night activity
                profile = self._generate_bot_like_profile(i)
            elif pattern_type == 'fake_engagement':
                # Fake engagement: high followers, low quality content
                profile = self._generate_fake_engagement_profile(i)
            elif pattern_type == 'content_farm':
                # Content farm: many repos, low originality
                profile = self._generate_content_farm_profile(i)
            else:
                # Inactive fake: old account, sudden activity
                profile = self._generate_inactive_fake_profile(i)
            
            suspicious_profiles.append(profile)
        
        return suspicious_profiles
    
    def _generate_bot_like_profile(self, index: int) -> Dict:
        """Generate bot-like profile with regular patterns"""
        import random
        
        return {
            'username': f'bot_like_user_{index}',
            'label': 0,
            'account_age_days': random.randint(30, 365),
            'public_repos': random.randint(10, 50),
            'followers': random.randint(1, 20),
            'following': random.randint(50, 200),
            'public_gists': random.randint(0, 5),
            'total_commits': random.randint(100, 1000),
            'total_repositories': random.randint(10, 50),
            'profile_completeness': random.uniform(0.2, 0.5),
            
            # Bot-like temporal patterns
            'weekend_commit_ratio': random.uniform(0.6, 0.9),
            'night_commit_ratio': random.uniform(0.5, 0.8),
            'commit_frequency': random.uniform(100, 300),
            'activity_consistency': random.uniform(0.9, 1.0),  # Too consistent
            'timing_entropy': random.uniform(0.1, 0.3),  # Low entropy
            'burst_activity_score': random.uniform(0.1, 0.3),  # High burst
            
            # Repository patterns
            'original_repo_ratio': random.uniform(0.1, 0.4),
            'fork_ratio': random.uniform(0.6, 0.9),
            'repo_activity_ratio': random.uniform(0.2, 0.5),
            'avg_stars_per_repo': random.uniform(0, 2),
            'avg_forks_per_repo': random.uniform(0, 1),
            'language_diversity': random.randint(1, 3),
            'avg_repo_size': random.uniform(10, 100),
            'repo_size_variance': random.uniform(0.05, 0.2),
            'repo_naming_quality': random.uniform(0.2, 0.5),
            'avg_issues_per_repo': random.uniform(0, 1),
            'archived_repo_ratio': random.uniform(0, 0.2),
            'zero_star_repo_ratio': random.uniform(0.7, 1.0),
            
            # Social patterns
            'follower_repo_ratio': random.uniform(0.1, 0.5),
            'follower_following_ratio': random.uniform(0.05, 0.2),
            'total_stars_received': random.randint(0, 20),
            'total_forks_received': random.randint(0, 10),
            'public_gist_count': random.randint(0, 5),
            
            # Activity patterns
            'avg_commit_size': random.uniform(5, 50),  # Small, regular commits
            'commit_size_variance': random.uniform(0.05, 0.2),  # Low variance
            'large_commit_ratio': random.uniform(0, 0.1),
            'trivial_commit_ratio': random.uniform(0.3, 0.7),
            'commit_message_length_avg': random.uniform(10, 30),
            'empty_commit_ratio': random.uniform(0.1, 0.3),
            'contributions_per_repo': random.uniform(5, 20),
            
            # Code quality
            'has_readme_ratio': random.uniform(0.2, 0.6),
            'has_license_ratio': random.uniform(0.1, 0.4),
            'maintenance_score': random.uniform(0.2, 0.5),
            
            'collected_at': datetime.now().isoformat()
        }
    
    def _generate_fake_engagement_profile(self, index: int) -> Dict:
        """Generate profile with fake engagement patterns"""
        import random
        
        return {
            'username': f'fake_engagement_user_{index}',
            'label': 0,
            'account_age_days': random.randint(180, 1000),
            'public_repos': random.randint(5, 25),
            'followers': random.randint(100, 5000),  # Suspiciously high
            'following': random.randint(10, 100),
            'public_gists': random.randint(0, 10),
            'total_commits': random.randint(50, 300),
            'total_repositories': random.randint(5, 25),
            'profile_completeness': random.uniform(0.6, 0.9),  # Looks complete
            
            # Normal-ish temporal patterns
            'weekend_commit_ratio': random.uniform(0.2, 0.5),
            'night_commit_ratio': random.uniform(0.1, 0.4),
            'commit_frequency': random.uniform(20, 80),
            'activity_consistency': random.uniform(0.4, 0.7),
            'timing_entropy': random.uniform(0.4, 0.7),
            'burst_activity_score': random.uniform(0.3, 0.7),
            
            # Low quality repositories
            'original_repo_ratio': random.uniform(0.3, 0.7),
            'fork_ratio': random.uniform(0.3, 0.7),
            'repo_activity_ratio': random.uniform(0.3, 0.6),
            'avg_stars_per_repo': random.uniform(0, 5),
            'avg_forks_per_repo': random.uniform(0, 2),
            'language_diversity': random.randint(2, 5),
            'avg_repo_size': random.uniform(50, 500),
            'repo_size_variance': random.uniform(0.3, 0.8),
            'repo_naming_quality': random.uniform(0.3, 0.7),
            'avg_issues_per_repo': random.uniform(0, 3),
            'archived_repo_ratio': random.uniform(0, 0.3),
            'zero_star_repo_ratio': random.uniform(0.4, 0.8),
            
            # Suspicious social patterns
            'follower_repo_ratio': random.uniform(5, 50),  # Too many followers
            'follower_following_ratio': random.uniform(2, 20),
            'total_stars_received': random.randint(10, 100),
            'total_forks_received': random.randint(5, 50),
            'public_gist_count': random.randint(0, 20),
            
            # Activity patterns
            'avg_commit_size': random.uniform(20, 200),
            'commit_size_variance': random.uniform(0.3, 0.8),
            'large_commit_ratio': random.uniform(0.1, 0.3),
            'trivial_commit_ratio': random.uniform(0.2, 0.5),
            'commit_message_length_avg': random.uniform(15, 50),
            'empty_commit_ratio': random.uniform(0.05, 0.2),
            'contributions_per_repo': random.uniform(3, 15),
            
            # Code quality
            'has_readme_ratio': random.uniform(0.4, 0.8),
            'has_license_ratio': random.uniform(0.2, 0.6),
            'maintenance_score': random.uniform(0.3, 0.7),
            
            'collected_at': datetime.now().isoformat()
        }
    
    def _generate_content_farm_profile(self, index: int) -> Dict:
        """Generate content farm profile with many low-quality repos"""
        import random
        
        return {
            'username': f'content_farm_user_{index}',
            'label': 0,
            'account_age_days': random.randint(90, 500),
            'public_repos': random.randint(50, 200),  # Many repos
            'followers': random.randint(10, 100),
            'following': random.randint(20, 200),
            'public_gists': random.randint(0, 50),
            'total_commits': random.randint(200, 2000),
            'total_repositories': random.randint(50, 200),
            'profile_completeness': random.uniform(0.3, 0.7),
            
            # Temporal patterns
            'weekend_commit_ratio': random.uniform(0.3, 0.6),
            'night_commit_ratio': random.uniform(0.2, 0.5),
            'commit_frequency': random.uniform(150, 500),  # High frequency
            'activity_consistency': random.uniform(0.2, 0.5),  # Inconsistent
            'timing_entropy': random.uniform(0.3, 0.6),
            'burst_activity_score': random.uniform(0.2, 0.5),  # Bursty
            
            # Repository patterns - many forks/copies
            'original_repo_ratio': random.uniform(0.1, 0.3),  # Low originality
            'fork_ratio': random.uniform(0.7, 0.9),  # Mostly forks
            'repo_activity_ratio': random.uniform(0.1, 0.4),
            'avg_stars_per_repo': random.uniform(0, 1),
            'avg_forks_per_repo': random.uniform(0, 0.5),
            'language_diversity': random.randint(3, 8),
            'avg_repo_size': random.uniform(20, 200),
            'repo_size_variance': random.uniform(0.4, 0.9),
            'repo_naming_quality': random.uniform(0.2, 0.5),
            'avg_issues_per_repo': random.uniform(0, 2),
            'archived_repo_ratio': random.uniform(0.1, 0.4),
            'zero_star_repo_ratio': random.uniform(0.8, 1.0),
            
            # Social patterns
            'follower_repo_ratio': random.uniform(0.1, 1),
            'follower_following_ratio': random.uniform(0.2, 2),
            'total_stars_received': random.randint(0, 50),
            'total_forks_received': random.randint(0, 20),
            'public_gist_count': random.randint(0, 50),
            
            # Activity patterns
            'avg_commit_size': random.uniform(10, 100),
            'commit_size_variance': random.uniform(0.2, 0.7),
            'large_commit_ratio': random.uniform(0.05, 0.2),
            'trivial_commit_ratio': random.uniform(0.4, 0.8),  # Many trivial commits
            'commit_message_length_avg': random.uniform(8, 25),
            'empty_commit_ratio': random.uniform(0.1, 0.4),
            'contributions_per_repo': random.uniform(1, 10),
            
            # Code quality
            'has_readme_ratio': random.uniform(0.2, 0.5),
            'has_license_ratio': random.uniform(0.1, 0.3),
            'maintenance_score': random.uniform(0.1, 0.4),
            
            'collected_at': datetime.now().isoformat()
        }
    
    def _generate_inactive_fake_profile(self, index: int) -> Dict:
        """Generate inactive account with sudden activity"""
        import random
        
        return {
            'username': f'inactive_fake_user_{index}',
            'label': 0,
            'account_age_days': random.randint(500, 2000),  # Old account
            'public_repos': random.randint(5, 30),
            'followers': random.randint(5, 50),
            'following': random.randint(10, 100),
            'public_gists': random.randint(0, 10),
            'total_commits': random.randint(20, 200),
            'total_repositories': random.randint(5, 30),
            'profile_completeness': random.uniform(0.2, 0.6),
            
            # Temporal patterns - sudden activity
            'weekend_commit_ratio': random.uniform(0.4, 0.7),
            'night_commit_ratio': random.uniform(0.3, 0.6),
            'commit_frequency': random.uniform(5, 30),  # Low but recent
            'activity_consistency': random.uniform(0.1, 0.3),  # Very inconsistent
            'timing_entropy': random.uniform(0.2, 0.5),
            'burst_activity_score': random.uniform(0.1, 0.4),  # High burst
            
            # Repository patterns
            'original_repo_ratio': random.uniform(0.2, 0.6),
            'fork_ratio': random.uniform(0.4, 0.8),
            'repo_activity_ratio': random.uniform(0.1, 0.3),  # Low activity
            'avg_stars_per_repo': random.uniform(0, 3),
            'avg_forks_per_repo': random.uniform(0, 1),
            'language_diversity': random.randint(1, 4),
            'avg_repo_size': random.uniform(30, 300),
            'repo_size_variance': random.uniform(0.3, 0.8),
            'repo_naming_quality': random.uniform(0.3, 0.6),
            'avg_issues_per_repo': random.uniform(0, 2),
            'archived_repo_ratio': random.uniform(0.2, 0.6),
            'zero_star_repo_ratio': random.uniform(0.6, 0.9),
            
            # Social patterns
            'follower_repo_ratio': random.uniform(0.5, 3),
            'follower_following_ratio': random.uniform(0.2, 1),
            'total_stars_received': random.randint(0, 30),
            'total_forks_received': random.randint(0, 15),
            'public_gist_count': random.randint(0, 10),
            
            # Activity patterns
            'avg_commit_size': random.uniform(15, 150),
            'commit_size_variance': random.uniform(0.4, 0.9),
            'large_commit_ratio': random.uniform(0.1, 0.4),
            'trivial_commit_ratio': random.uniform(0.2, 0.6),
            'commit_message_length_avg': random.uniform(12, 40),
            'empty_commit_ratio': random.uniform(0.05, 0.3),
            'contributions_per_repo': random.uniform(2, 12),
            
            # Code quality
            'has_readme_ratio': random.uniform(0.3, 0.7),
            'has_license_ratio': random.uniform(0.2, 0.5),
            'maintenance_score': random.uniform(0.2, 0.5),
            
            'collected_at': datetime.now().isoformat()
        }
    
    def generate_borderline_cases(self, count: int = 25) -> List[Dict]:
        """Generate borderline cases that are harder to classify"""
        import random
        
        print(f"🔄 Generating {count} borderline cases...")
        
        borderline_profiles = []
        
        for i in range(count):
            # Create profiles that are ambiguous
            case_type = random.choice(['new_legitimate', 'unusual_but_real', 'low_activity_real'])
            
            if case_type == 'new_legitimate':
                profile = self._generate_new_legitimate_profile(i)
            elif case_type == 'unusual_but_real':
                profile = self._generate_unusual_but_real_profile(i)
            else:
                profile = self._generate_low_activity_real_profile(i)
            
            borderline_profiles.append(profile)
        
        return borderline_profiles
    
    def _generate_new_legitimate_profile(self, index: int) -> Dict:
        """Generate new but legitimate developer profile"""
        import random
        
        return {
            'username': f'new_legitimate_user_{index}',
            'label': 1,  # Actually authentic
            'account_age_days': random.randint(30, 180),  # New account
            'public_repos': random.randint(3, 15),
            'followers': random.randint(0, 20),
            'following': random.randint(5, 50),
            'public_gists': random.randint(0, 5),
            'total_commits': random.randint(20, 150),
            'total_repositories': random.randint(3, 15),
            'profile_completeness': random.uniform(0.4, 0.8),
            
            # Normal temporal patterns
            'weekend_commit_ratio': random.uniform(0.1, 0.3),
            'night_commit_ratio': random.uniform(0.05, 0.25),
            'commit_frequency': random.uniform(30, 120),
            'activity_consistency': random.uniform(0.5, 0.8),
            'timing_entropy': random.uniform(0.5, 0.8),
            'burst_activity_score': random.uniform(0.4, 0.8),
            
            # Good repository patterns
            'original_repo_ratio': random.uniform(0.6, 0.9),
            'fork_ratio': random.uniform(0.1, 0.4),
            'repo_activity_ratio': random.uniform(0.6, 0.9),
            'avg_stars_per_repo': random.uniform(0, 5),
            'avg_forks_per_repo': random.uniform(0, 2),
            'language_diversity': random.randint(2, 5),
            'avg_repo_size': random.uniform(100, 1000),
            'repo_size_variance': random.uniform(0.4, 0.8),
            'repo_naming_quality': random.uniform(0.6, 0.9),
            'avg_issues_per_repo': random.uniform(0, 3),
            'archived_repo_ratio': random.uniform(0, 0.2),
            'zero_star_repo_ratio': random.uniform(0.3, 0.7),
            
            # Normal social patterns
            'follower_repo_ratio': random.uniform(0.5, 3),
            'follower_following_ratio': random.uniform(0.2, 2),
            'total_stars_received': random.randint(0, 50),
            'total_forks_received': random.randint(0, 20),
            'public_gist_count': random.randint(0, 5),
            
            # Good activity patterns
            'avg_commit_size': random.uniform(50, 300),
            'commit_size_variance': random.uniform(0.4, 0.8),
            'large_commit_ratio': random.uniform(0.1, 0.3),
            'trivial_commit_ratio': random.uniform(0.1, 0.4),
            'commit_message_length_avg': random.uniform(25, 60),
            'empty_commit_ratio': random.uniform(0, 0.1),
            'contributions_per_repo': random.uniform(5, 25),
            
            # Good code quality
            'has_readme_ratio': random.uniform(0.6, 0.9),
            'has_license_ratio': random.uniform(0.3, 0.7),
            'maintenance_score': random.uniform(0.6, 0.9),
            
            'collected_at': datetime.now().isoformat()
        }
    
    def _generate_unusual_but_real_profile(self, index: int) -> Dict:
        """Generate unusual but legitimate profile"""
        import random
        
        return {
            'username': f'unusual_but_real_user_{index}',
            'label': 1,  # Actually authentic
            'account_age_days': random.randint(200, 1500),
            'public_repos': random.randint(10, 40),
            'followers': random.randint(20, 200),
            'following': random.randint(10, 100),
            'public_gists': random.randint(0, 20),
            'total_commits': random.randint(100, 800),
            'total_repositories': random.randint(10, 40),
            'profile_completeness': random.uniform(0.5, 0.9),
            
            # Unusual but legitimate temporal patterns
            'weekend_commit_ratio': random.uniform(0.35, 0.5),  # Higher but not extreme
            'night_commit_ratio': random.uniform(0.25, 0.4),   # Higher but not extreme
            'commit_frequency': random.uniform(80, 200),
            'activity_consistency': random.uniform(0.3, 0.7),
            'timing_entropy': random.uniform(0.4, 0.7),
            'burst_activity_score': random.uniform(0.3, 0.7),
            
            # Mixed repository patterns
            'original_repo_ratio': random.uniform(0.4, 0.7),
            'fork_ratio': random.uniform(0.3, 0.6),
            'repo_activity_ratio': random.uniform(0.4, 0.8),
            'avg_stars_per_repo': random.uniform(1, 10),
            'avg_forks_per_repo': random.uniform(0, 3),
            'language_diversity': random.randint(3, 8),
            'avg_repo_size': random.uniform(200, 2000),
            'repo_size_variance': random.uniform(0.5, 0.9),
            'repo_naming_quality': random.uniform(0.5, 0.8),
            'avg_issues_per_repo': random.uniform(1, 5),
            'archived_repo_ratio': random.uniform(0.1, 0.3),
            'zero_star_repo_ratio': random.uniform(0.2, 0.6),
            
            # Social patterns
            'follower_repo_ratio': random.uniform(1, 8),
            'follower_following_ratio': random.uniform(0.5, 4),
            'total_stars_received': random.randint(10, 200),
            'total_forks_received': random.randint(5, 100),
            'public_gist_count': random.randint(0, 20),
            
            # Activity patterns
            'avg_commit_size': random.uniform(30, 400),
            'commit_size_variance': random.uniform(0.5, 0.9),
            'large_commit_ratio': random.uniform(0.15, 0.4),
            'trivial_commit_ratio': random.uniform(0.15, 0.5),
            'commit_message_length_avg': random.uniform(20, 80),
            'empty_commit_ratio': random.uniform(0, 0.15),
            'contributions_per_repo': random.uniform(8, 30),
            
            # Code quality
            'has_readme_ratio': random.uniform(0.5, 0.8),
            'has_license_ratio': random.uniform(0.3, 0.6),
            'maintenance_score': random.uniform(0.4, 0.8),
            
            'collected_at': datetime.now().isoformat()
        }
    
    def _generate_low_activity_real_profile(self, index: int) -> Dict:
        """Generate low activity but real profile"""
        import random
        
        return {
            'username': f'low_activity_real_user_{index}',
            'label': 1,  # Actually authentic
            'account_age_days': random.randint(365, 2500),  # Older account
            'public_repos': random.randint(2, 12),
            'followers': random.randint(0, 30),
            'following': random.randint(5, 50),
            'public_gists': random.randint(0, 8),
            'total_commits': random.randint(10, 100),
            'total_repositories': random.randint(2, 12),
            'profile_completeness': random.uniform(0.3, 0.7),
            
            # Low activity temporal patterns
            'weekend_commit_ratio': random.uniform(0.15, 0.35),
            'night_commit_ratio': random.uniform(0.1, 0.3),
            'commit_frequency': random.uniform(5, 40),  # Low frequency
            'activity_consistency': random.uniform(0.2, 0.6),
            'timing_entropy': random.uniform(0.3, 0.7),
            'burst_activity_score': random.uniform(0.3, 0.8),
            
            # Repository patterns
            'original_repo_ratio': random.uniform(0.5, 0.9),
            'fork_ratio': random.uniform(0.1, 0.5),
            'repo_activity_ratio': random.uniform(0.2, 0.6),
            'avg_stars_per_repo': random.uniform(0, 8),
            'avg_forks_per_repo': random.uniform(0, 3),
            'language_diversity': random.randint(1, 4),
            'avg_repo_size': random.uniform(100, 1500),
            'repo_size_variance': random.uniform(0.3, 0.8),
            'repo_naming_quality': random.uniform(0.5, 0.8),
            'avg_issues_per_repo': random.uniform(0, 2),
            'archived_repo_ratio': random.uniform(0, 0.4),
            'zero_star_repo_ratio': random.uniform(0.4, 0.8),
            
            # Social patterns
            'follower_repo_ratio': random.uniform(0.5, 5),
            'follower_following_ratio': random.uniform(0.2, 2),
            'total_stars_received': random.randint(0, 80),
            'total_forks_received': random.randint(0, 30),
            'public_gist_count': random.randint(0, 8),
            
            # Activity patterns
            'avg_commit_size': random.uniform(40, 500),
            'commit_size_variance': random.uniform(0.4, 0.9),
            'large_commit_ratio': random.uniform(0.1, 0.4),
            'trivial_commit_ratio': random.uniform(0.1, 0.4),
            'commit_message_length_avg': random.uniform(20, 70),
            'empty_commit_ratio': random.uniform(0, 0.2),
            'contributions_per_repo': random.uniform(2, 15),
            
            # Code quality
            'has_readme_ratio': random.uniform(0.4, 0.8),
            'has_license_ratio': random.uniform(0.2, 0.6),
            'maintenance_score': random.uniform(0.3, 0.7),
            
            'collected_at': datetime.now().isoformat()
        }
    
    def collect_all_data(self) -> pd.DataFrame:
        """Collect comprehensive training data"""
        print("🚀 Starting comprehensive training data collection...")
        
        # Check rate limit before starting
        self.get_rate_limit_info()
        
        # Collect authentic profiles
        print("\n📊 Collecting authentic developer profiles...")
        authentic_data = self.collect_authentic_profiles()
        
        # Collect borderline cases
        print("\n🔄 Collecting borderline cases...")
        borderline_data = self.collect_borderline_profiles()
        
        # Generate suspicious data
        print("\n⚠️  Generating suspicious profiles...")
        suspicious_data = self.generate_synthetic_suspicious_data(len(authentic_data))
        
        # Combine all data
        all_data = authentic_data + borderline_data + suspicious_data
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        
        # Data quality checks
        print(f"\n📊 Data Collection Summary:")
        print(f"  ✅ Authentic profiles: {len(authentic_data)}")
        print(f"  🔄 Borderline profiles: {len(borderline_data)}")
        print(f"  ⚠️  Suspicious profiles: {len(suspicious_data)}")
        print(f"  📈 Total profiles: {len(df)}")
        
        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            print(f"\n⚠️  Missing data detected:")
            print(missing_data[missing_data > 0])
        
        # Label distribution
        print(f"\n🎯 Label distribution:")
        label_counts = df['label'].value_counts()
        print(f"  Authentic (1): {label_counts.get(1, 0)}")
        print(f"  Suspicious (0): {label_counts.get(0, 0)}")
        
        return df
    
    def save_data(self, df: pd.DataFrame, filename: str = None) -> str:
        """Save training data with timestamp"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_data_{timestamp}.csv"
        
        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}"
        
        # Save main dataset
        df.to_csv(filepath, index=False)
        
        # Save metadata
        metadata = {
            'filename': filename,
            'created_at': datetime.now().isoformat(),
            'total_profiles': len(df),
            'authentic_profiles': len(df[df['label'] == 1]),
            'suspicious_profiles': len(df[df['label'] == 0]),
            'features': list(df.columns),
            'feature_count': len(df.columns) - 3,  # Exclude username, label, collected_at
            'data_sources': {
                'real_github_profiles': len(df[(df['label'] == 1) & (~df['username'].str.contains('synthetic|fake|bot'))]),
                'synthetic_profiles': len(df[df['username'].str.contains('synthetic|fake|bot|suspicious|borderline|new_legitimate|unusual|low_activity')])
            }
        }
        
        metadata_path = f"data/{filename.replace('.csv', '_metadata.json')}"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Saved training data to {filepath}")
        print(f"📋 Saved metadata to {metadata_path}")
        
        return filepath
    
    def analyze_collected_data(self, df: pd.DataFrame):
        """Analyze the collected training data"""
        print("\n🔍 Analyzing collected training data...")
        
        # Basic statistics
        print(f"\n📊 Dataset Statistics:")
        print(f"  Shape: {df.shape}")
        print(f"  Features: {df.shape[1] - 3}")  # Exclude username, label, collected_at
        
        # Feature statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col != 'label']
        
        if len(numeric_cols) > 0:
            print(f"\n📈 Feature Statistics:")
            stats = df[numeric_cols].describe()
            print(stats.round(3))
        
        # Label analysis
        print(f"\n🎯 Label Analysis:")
        for label in [0, 1]:
            subset = df[df['label'] == label]
            label_name = "Suspicious" if label == 0 else "Authentic"
            print(f"\n  {label_name} profiles ({len(subset)}):")
            
            if len(subset) > 0:
                # Key distinguishing features
                key_features = ['weekend_commit_ratio', 'night_commit_ratio', 'original_repo_ratio', 
                              'commit_frequency', 'follower_repo_ratio', 'language_diversity']
                
                for feature in key_features:
                    if feature in subset.columns:
                        mean_val = subset[feature].mean()
                        print(f"    {feature}: {mean_val:.3f}")
        
        # Feature correlations with label
        print(f"\n🔗 Top features correlated with authenticity:")
        correlations = df[numeric_cols + ['label']].corr()['label'].abs().sort_values(ascending=False)
        top_features = correlations.head(10)
        
        for feature, corr in top_features.items():
            if feature != 'label':
                print(f"  {feature}: {corr:.3f}")
        
        return df

def main():
    """Main data collection function with comprehensive options"""
    print("🚀 Enhanced GitHub Profile Data Collection for ML Training")
    print("=" * 70)
    
    # Initialize collector
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("⚠️  No GitHub token found. Using unauthenticated requests (rate limited)")
        print("💡 Set GITHUB_TOKEN environment variable for better rate limits")
    else:
        print("✅ GitHub token found - using authenticated requests")
    
    collector = EnhancedTrainingDataCollector(github_token)
    
    # Check rate limit
    collector.get_rate_limit_info()
    
    # Collect comprehensive data
    df = collector.collect_all_data()
    
    if df.empty:
        print("❌ No data collected. Please check your GitHub token and network connection.")
        return
    
    # Analyze collected data
    collector.analyze_collected_data(df)
    
    # Save data with timestamp
    filepath = collector.save_data(df)
    
    # Generate summary report
    print(f"\n📋 Training Data Summary Report:")
    print(f"  📁 File: {filepath}")
    print(f"  📊 Total samples: {len(df)}")
    print(f"  🎯 Features: {len([col for col in df.columns if col not in ['username', 'label', 'collected_at']])}")
    print(f"  ⚖️  Balance: {len(df[df['label']==1])} authentic, {len(df[df['label']==0])} suspicious")
    
    # Feature importance preview
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col != 'label']
    
    if len(numeric_cols) > 0:
        correlations = df[numeric_cols + ['label']].corr()['label'].abs().sort_values(ascending=False)
        print(f"\n🔝 Top 5 most predictive features:")
        for i, (feature, corr) in enumerate(correlations.head(6).items()):
            if feature != 'label':
                print(f"  {i+1}. {feature}: {corr:.3f}")
    
    print(f"\n✅ Enhanced training data ready!")
    print(f"💡 Next steps:")
    print(f"  1. Review the data quality and feature distributions")
    print(f"  2. Train your ML model: python ml_training/train_model.py")
    print(f"  3. Or use Excel training: python train_with_excel_data.py")
    print(f"  4. The model will automatically use the new features")
    
    # Optional: Create a quick visualization
    try:
        import matplotlib.pyplot as plt
        
        # Create a simple feature distribution plot
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.ravel()
        
        key_features = ['weekend_commit_ratio', 'night_commit_ratio', 'original_repo_ratio', 
                       'commit_frequency', 'follower_repo_ratio', 'language_diversity']
        
        for i, feature in enumerate(key_features):
            if feature in df.columns and i < 6:
                authentic = df[df['label'] == 1][feature]
                suspicious = df[df['label'] == 0][feature]
                
                axes[i].hist(authentic, alpha=0.7, label='Authentic', bins=20, color='green')
                axes[i].hist(suspicious, alpha=0.7, label='Suspicious', bins=20, color='red')
                axes[i].set_title(f'{feature}')
                axes[i].legend()
        
        plt.tight_layout()
        
        # Save plot
        os.makedirs("visualizations", exist_ok=True)
        plot_path = "visualizations/training_data_distributions.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"📊 Saved feature distributions to {plot_path}")
        
    except ImportError:
        print("📊 Install matplotlib to generate feature distribution plots")
    except Exception as e:
        print(f"⚠️  Could not generate plots: {e}")

if __name__ == "__main__":
    main()