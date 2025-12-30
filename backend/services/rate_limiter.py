import time
import os
from typing import Dict, Optional
from datetime import datetime, timedelta
import json

class RateLimiter:
    """
    Rate limiter to protect GitHub API usage and costs
    """
    
    def __init__(self):
        self.requests_file = "rate_limit_data.json"
        self.max_requests_per_hour = int(os.getenv("MAX_REQUESTS_PER_HOUR", "50"))
        self.max_requests_per_day = int(os.getenv("MAX_REQUESTS_PER_DAY", "200"))
        self.max_repos_per_analysis = int(os.getenv("MAX_REPOS_PER_ANALYSIS", "10"))
        self.max_commits_per_repo = int(os.getenv("MAX_COMMITS_PER_REPO", "20"))
        
        # Load existing rate limit data
        self.rate_data = self._load_rate_data()
        
    def _load_rate_data(self) -> Dict:
        """Load rate limit data from file"""
        try:
            if os.path.exists(self.requests_file):
                with open(self.requests_file, 'r') as f:
                    data = json.load(f)
                    # Clean old data (older than 24 hours)
                    current_time = time.time()
                    data['requests'] = [
                        req for req in data.get('requests', [])
                        if current_time - req['timestamp'] < 86400  # 24 hours
                    ]
                    return data
        except Exception as e:
            print(f"Error loading rate data: {e}")
        
        return {
            'requests': [],
            'daily_count': 0,
            'last_reset': time.time()
        }
    
    def _save_rate_data(self):
        """Save rate limit data to file"""
        try:
            with open(self.requests_file, 'w') as f:
                json.dump(self.rate_data, f)
        except Exception as e:
            print(f"Error saving rate data: {e}")
    
    def _reset_daily_count_if_needed(self):
        """Reset daily count if 24 hours have passed"""
        current_time = time.time()
        if current_time - self.rate_data.get('last_reset', 0) >= 86400:  # 24 hours
            self.rate_data['daily_count'] = 0
            self.rate_data['last_reset'] = current_time
            self.rate_data['requests'] = []
    
    def can_make_request(self, estimated_api_calls: int = 1) -> tuple[bool, str]:
        """
        Check if we can make a request without exceeding limits
        Returns (can_make_request, reason_if_not)
        """
        self._reset_daily_count_if_needed()
        
        current_time = time.time()
        
        # Check hourly limit
        hourly_requests = [
            req for req in self.rate_data['requests']
            if current_time - req['timestamp'] < 3600  # 1 hour
        ]
        
        hourly_count = sum(req['api_calls'] for req in hourly_requests)
        if hourly_count + estimated_api_calls > self.max_requests_per_hour:
            return False, f"Hourly limit exceeded ({hourly_count}/{self.max_requests_per_hour}). Try again in {60 - int((current_time % 3600) / 60)} minutes."
        
        # Check daily limit
        if self.rate_data['daily_count'] + estimated_api_calls > self.max_requests_per_day:
            return False, f"Daily limit exceeded ({self.rate_data['daily_count']}/{self.max_requests_per_day}). Try again tomorrow."
        
        return True, ""
    
    def record_request(self, api_calls_used: int, username: str):
        """Record a successful request"""
        current_time = time.time()
        
        self.rate_data['requests'].append({
            'timestamp': current_time,
            'api_calls': api_calls_used,
            'username': username
        })
        
        self.rate_data['daily_count'] += api_calls_used
        self._save_rate_data()
        
        print(f"📊 API Usage: {api_calls_used} calls for {username}. Daily total: {self.rate_data['daily_count']}/{self.max_requests_per_day}")
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics"""
        self._reset_daily_count_if_needed()
        
        current_time = time.time()
        
        # Hourly stats
        hourly_requests = [
            req for req in self.rate_data['requests']
            if current_time - req['timestamp'] < 3600
        ]
        hourly_count = sum(req['api_calls'] for req in hourly_requests)
        
        return {
            'hourly_usage': {
                'used': hourly_count,
                'limit': self.max_requests_per_hour,
                'remaining': max(0, self.max_requests_per_hour - hourly_count)
            },
            'daily_usage': {
                'used': self.rate_data['daily_count'],
                'limit': self.max_requests_per_day,
                'remaining': max(0, self.max_requests_per_day - self.rate_data['daily_count'])
            },
            'limits': {
                'max_repos_per_analysis': self.max_repos_per_analysis,
                'max_commits_per_repo': self.max_commits_per_repo
            }
        }
    
    def estimate_api_calls(self, analysis_type: str = "full") -> int:
        """Estimate API calls needed for different analysis types"""
        if analysis_type == "full":
            # User info (1) + repos (1) + commits from repos (max_repos_per_analysis)
            return 2 + self.max_repos_per_analysis
        elif analysis_type == "basic":
            # User info (1) + repos (1) + commits from 2 repos
            return 4
        else:
            return 1

# Global rate limiter instance
rate_limiter = RateLimiter()