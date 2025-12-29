#!/usr/bin/env python3
"""
Test script to verify the ML-powered GitHub analysis integration
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health():
    """Test API health endpoint"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_BASE}/health")
        data = response.json()
        print(f"✅ Health check: {data['status']}")
        print(f"🧠 ML Model loaded: {data['ml_model_loaded']}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_analysis(username="octocat"):
    """Test profile analysis"""
    print(f"\n🔍 Testing analysis for user: {username}")
    try:
        start_time = time.time()
        response = requests.post(f"{API_BASE}/analyze/{username}")
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis completed in {end_time - start_time:.2f}s")
            print(f"👤 Username: {data['username']}")
            print(f"🎯 Authenticity Score: {data['authenticity_score']}/100")
            print(f"🔒 Confidence: {data['confidence']}%")
            print(f"🚩 Red Flags: {len(data['red_flags'])}")
            
            # Print red flags
            for flag in data['red_flags']:
                severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                print(f"  {severity_emoji.get(flag['severity'], '⚪')} {flag['title']}: {flag['description']}")
            
            # Print metrics
            metrics = data['metrics']
            print(f"\n📊 Metrics:")
            print(f"  • Total Commits: {metrics['total_commits']}")
            print(f"  • Public Repos: {metrics['public_repos']}")
            print(f"  • Followers: {metrics['followers']}")
            print(f"  • Original Content: {metrics['original_repos_percent']}%")
            print(f"  • Activity Consistency: {metrics['activity_consistency']}%")
            print(f"  • Language Diversity: {metrics['language_diversity']}")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def main():
    print("🚀 Dev-Sentinel ML Integration Test")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("❌ API is not healthy. Make sure the backend is running.")
        return
    
    # Test analysis with different users
    test_users = ["octocat", "torvalds", "gaearon"]
    
    for user in test_users:
        success = test_analysis(user)
        if not success:
            print(f"⚠️  Analysis failed for {user}, but continuing...")
        time.sleep(1)  # Rate limiting
    
    print("\n🎉 Integration test completed!")
    print("\n💡 Next steps:")
    print("1. Open http://localhost:8081 in your browser")
    print("2. Enter a GitHub username and click 'Analyze'")
    print("3. See real ML-powered analysis results!")

if __name__ == "__main__":
    main()