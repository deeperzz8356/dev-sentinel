#!/usr/bin/env python3
"""
Data collection script for training the ML model
Collects GitHub profiles and labels them for training
"""

import os
import json
import time
import pandas as pd
from datetime import datetime
from typing import List, Dict
import sys
sys.path.append('..')

from services.github_service import GitHubService
from services.simple_analyzer import SimpleAnalyzer

class TrainingDataCollector:
    def __init__(self, github_token: str = None):
        self.github_service = GitHubService(token=github_token)
        self.analyzer = SimpleAnalyzer()
        self.data = []
        
    def collect_authentic_profiles(self) -> List[Dict]:
        """
        Collect known authentic developer profiles
        These are well-known developers with verified authentic activity
        """
        authentic_users = [
            # Famous developers
            "torvalds",      # Linus Torvalds - Linux creator
            "gaearon",       # Dan Abramov - React team
            "tj",            # TJ Holowaychuk - Express.js
            "sindresorhus",  # Sindre Sorhus - Popular OSS maintainer
            "addyosmani",    # Addy Osmani - Google Chrome team
            "paulirish",     # Paul Irish - Google Chrome team
            "mdo",           # Mark Otto - Bootstrap creator
            "fat",           # Jacob Thornton - Bootstrap co-creator
            "defunkt",       # Chris Wanstrath - GitHub co-founder
            "mojombo",       # Tom Preston-Werner - GitHub co-founder
            
            # Active OSS contributors
            "kentcdodds",    # Kent C. Dodds - Testing expert
            "wesbos",        # Wes Bos - JavaScript teacher
            "bradtraversy",  # Brad Traversy - Web dev educator
            "mpj",           # Mattias Petter Johansson - FunFunFunction
            "getify",        # Kyle Simpson - You Don't Know JS
            "ryanflorence",  # Ryan Florence - React Router
            "mjackson",      # Michael Jackson - React Router
            "sebmarkbage",   # Sebastian Markbåge - React team
            "acdlite",       # Andrew Clark - React team
            "sophiebits",    # Sophie Alpert - Former React team lead
        ]
        
        print(f"🔍 Collecting {len(authentic_users)} authentic profiles...")
        return self._collect_profiles(authentic_users, label=1)
    
    def collect_suspicious_profiles(self) -> List[Dict]:
        """
        Collect potentially suspicious profiles
        These are profiles that show patterns of inauthentic activity
        """
        # Note: These are examples of patterns to look for, not accusations
        # In real implementation, you'd use profiles you've manually verified as suspicious
        suspicious_patterns = [
            # Profiles with very few original repos but many forks
            # Profiles with unusual commit timing patterns
            # Profiles with sudden activity spikes
            # You would manually curate this list based on analysis
        ]
        
        # For demonstration, we'll create synthetic suspicious profiles
        # In production, you'd have a curated list of verified suspicious accounts
        print("⚠️  For training purposes, we'll generate synthetic suspicious data")
        return []
    
    def _collect_profiles(self, usernames: List[str], label: int) -> List[Dict]:
        """Collect profile data for given usernames"""
        profiles = []
        
        for i, username in enumerate(usernames):
            try:
                print(f"📊 Collecting {username} ({i+1}/{len(usernames)})...")
                
                # Get GitHub data
                github_data = self.github_service.get_profile_data(username)
                
                # Extract features
                features = self.analyzer._extract_features(github_data)
                
                # Create training record
                record = {
                    'username': username,
                    'label': label,  # 1 = authentic, 0 = suspicious
                    **features,
                    'collected_at': datetime.now().isoformat()
                }
                
                profiles.append(record)
                print(f"✅ Collected {username}: {len(github_data.get('commits', []))} commits, {len(github_data.get('repositories', []))} repos")
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Failed to collect {username}: {e}")
                continue
                
        return profiles
    
    def generate_synthetic_suspicious_data(self, count: int = 50) -> List[Dict]:
        """
        Generate synthetic suspicious profile data for training
        This simulates patterns found in inauthentic profiles
        """
        import random
        import numpy as np
        
        print(f"🤖 Generating {count} synthetic suspicious profiles...")
        
        suspicious_profiles = []
        
        for i in range(count):
            # Create suspicious patterns
            profile = {
                'username': f'suspicious_user_{i}',
                'label': 0,  # 0 = suspicious
                
                # Suspicious patterns:
                'commit_frequency': random.choice([
                    random.uniform(0.5, 3),    # Too few commits
                    random.uniform(80, 200)    # Too many commits (bot-like)
                ]),
                
                # High weekend/night activity (bot-like)
                'weekend_commit_ratio': random.uniform(0.6, 0.9),
                'night_commit_ratio': random.uniform(0.5, 0.8),
                
                # Low original content
                'original_repo_ratio': random.uniform(0.05, 0.3),
                
                # Very uniform commit sizes (bot-like)
                'commit_size_variance': random.uniform(0.01, 0.1),
                
                # Inconsistent activity
                'activity_consistency': random.uniform(0.1, 0.4),
                
                # Extreme follower ratios
                'follower_repo_ratio': random.choice([
                    random.uniform(0.001, 0.05),  # Too few followers
                    random.uniform(15, 100)        # Too many followers
                ]),
                
                # Limited language diversity
                'language_diversity': random.randint(1, 2),
                
                'collected_at': datetime.now().isoformat()
            }
            
            suspicious_profiles.append(profile)
            
        return suspicious_profiles
    
    def collect_all_data(self) -> pd.DataFrame:
        """Collect all training data"""
        print("🚀 Starting training data collection...")
        
        # Collect authentic profiles
        authentic_data = self.collect_authentic_profiles()
        
        # Generate suspicious data (since we don't have real suspicious profiles)
        suspicious_data = self.generate_synthetic_suspicious_data(len(authentic_data))
        
        # Combine all data
        all_data = authentic_data + suspicious_data
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        
        print(f"📊 Collected {len(df)} total profiles:")
        print(f"  ✅ Authentic: {len(authentic_data)}")
        print(f"  ⚠️  Suspicious: {len(suspicious_data)}")
        
        return df
    
    def save_data(self, df: pd.DataFrame, filename: str = "training_data.csv"):
        """Save training data to file"""
        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}"
        df.to_csv(filepath, index=False)
        print(f"💾 Saved training data to {filepath}")
        return filepath

def main():
    """Main data collection function"""
    # Initialize collector
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("⚠️  No GitHub token found. Using unauthenticated requests (rate limited)")
    
    collector = TrainingDataCollector(github_token)
    
    # Collect data
    df = collector.collect_all_data()
    
    # Save data
    filepath = collector.save_data(df)
    
    # Show summary
    print("\n📈 Data Summary:")
    print(df.describe())
    print(f"\n🎯 Label distribution:")
    print(df['label'].value_counts())
    
    print(f"\n✅ Training data ready! Use this file to train your ML model: {filepath}")

if __name__ == "__main__":
    main()