#!/usr/bin/env python3
"""
Quick GitHub API Test
Simple tests you can run manually
"""

import requests
import json

def test_health():
    """Test API health"""
    print("🔍 Testing API health...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_analysis(username):
    """Test profile analysis"""
    print(f"\n🔍 Testing analysis for: {username}")
    try:
        response = requests.post(f"http://localhost:8000/analyze/{username}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis successful!")
            print(f"   Username: {data['username']}")
            print(f"   Authenticity Score: {data['authenticity_score']}/100")
            print(f"   Confidence: {data['confidence']}%")
            print(f"   Red Flags: {len(data['red_flags'])}")
            print(f"   Total Commits: {data['metrics']['total_commits']}")
            print(f"   Public Repos: {data['metrics']['public_repos']}")
            print(f"   Followers: {data['metrics']['followers']}")
            
            if data['red_flags']:
                print("   🚩 Red Flags:")
                for flag in data['red_flags']:
                    print(f"      • {flag['title']}: {flag['description']}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("⚡ Quick GitHub API Test")
    print("=" * 30)
    
    # Test health
    if not test_health():
        print("❌ API health check failed!")
        return
    
    # Test with different users
    test_users = ["octocat", "torvalds", "gaearon"]
    
    for user in test_users:
        success = test_analysis(user)
        if success:
            print(f"✅ {user} analysis successful")
        else:
            print(f"❌ {user} analysis failed")
        print("-" * 30)

if __name__ == "__main__":
    main()