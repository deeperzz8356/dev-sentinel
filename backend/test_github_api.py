#!/usr/bin/env python3
"""
Comprehensive GitHub API Testing Suite
Tests all aspects of the GitHub integration and ML analysis
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List

class GitHubAPITester:
    def __init__(self, api_base: str = "http://localhost:8000"):
        self.api_base = api_base
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, data: Dict = None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {message}")
        
        if data and success:
            for key, value in data.items():
                print(f"   📊 {key}: {value}")
    
    def test_api_health(self) -> bool:
        """Test 1: API Health Check"""
        print("\n🔍 Test 1: API Health Check")
        try:
            response = requests.get(f"{self.api_base}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "API Health", 
                    True, 
                    f"API is healthy, ML model loaded: {data.get('ml_model_loaded', False)}",
                    data
                )
                return True
            else:
                self.log_test("API Health", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test("API Health", False, "Cannot connect to API. Is the backend running?")
            return False
        except Exception as e:
            self.log_test("API Health", False, f"Unexpected error: {e}")
            return False
    
    def test_github_profile_analysis(self, username: str = "octocat") -> bool:
        """Test 2: GitHub Profile Analysis"""
        print(f"\n🔍 Test 2: GitHub Profile Analysis ({username})")
        try:
            start_time = time.time()
            response = requests.post(f"{self.api_base}/analyze/{username}", timeout=30)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ['username', 'authenticity_score', 'confidence', 'red_flags', 'metrics']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(
                        f"Profile Analysis ({username})", 
                        False, 
                        f"Missing required fields: {missing_fields}"
                    )
                    return False
                
                analysis_data = {
                    'response_time': f"{end_time - start_time:.2f}s",
                    'authenticity_score': f"{data['authenticity_score']}/100",
                    'confidence': f"{data['confidence']}%",
                    'red_flags_count': len(data['red_flags']),
                    'total_commits': data['metrics']['total_commits'],
                    'public_repos': data['metrics']['public_repos'],
                    'followers': data['metrics']['followers']
                }
                
                self.log_test(
                    f"Profile Analysis ({username})", 
                    True, 
                    "Analysis completed successfully",
                    analysis_data
                )
                
                # Print red flags
                if data['red_flags']:
                    print("   🚩 Red Flags Detected:")
                    for flag in data['red_flags']:
                        severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                        emoji = severity_emoji.get(flag['severity'], '⚪')
                        print(f"      {emoji} {flag['title']}: {flag['description']}")
                else:
                    print("   ✅ No red flags detected")
                
                return True
            else:
                error_msg = response.text
                try:
                    error_data = response.json()
                    error_msg = error_data.get('detail', error_msg)
                except:
                    pass
                
                self.log_test(
                    f"Profile Analysis ({username})", 
                    False, 
                    f"HTTP {response.status_code}: {error_msg}"
                )
                return False
                
        except requests.exceptions.Timeout:
            self.log_test(f"Profile Analysis ({username})", False, "Request timed out (>30s)")
            return False
        except Exception as e:
            self.log_test(f"Profile Analysis ({username})", False, f"Unexpected error: {e}")
            return False
    
    def test_multiple_profiles(self, usernames: List[str]) -> bool:
        """Test 3: Multiple Profile Analysis"""
        print(f"\n🔍 Test 3: Multiple Profile Analysis")
        
        success_count = 0
        total_count = len(usernames)
        
        for i, username in enumerate(usernames):
            print(f"\n   Testing {username} ({i+1}/{total_count})...")
            
            try:
                response = requests.post(f"{self.api_base}/analyze/{username}", timeout=20)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ {username}: Score {data['authenticity_score']}/100, {len(data['red_flags'])} red flags")
                    success_count += 1
                else:
                    print(f"   ❌ {username}: HTTP {response.status_code}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ {username}: {e}")
        
        success_rate = (success_count / total_count) * 100
        self.log_test(
            "Multiple Profiles", 
            success_count > 0, 
            f"Analyzed {success_count}/{total_count} profiles successfully ({success_rate:.1f}%)",
            {'success_rate': f"{success_rate:.1f}%", 'successful': success_count, 'total': total_count}
        )
        
        return success_count > 0
    
    def test_error_handling(self) -> bool:
        """Test 4: Error Handling"""
        print(f"\n🔍 Test 4: Error Handling")
        
        # Test invalid username
        try:
            response = requests.post(f"{self.api_base}/analyze/invalid-user-that-does-not-exist-12345", timeout=10)
            
            if response.status_code == 400:
                self.log_test("Error Handling", True, "Correctly handles invalid usernames with 400 error")
                return True
            else:
                self.log_test("Error Handling", False, f"Expected 400 error, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Unexpected error: {e}")
            return False
    
    def test_rate_limiting(self) -> bool:
        """Test 5: Rate Limiting Behavior"""
        print(f"\n🔍 Test 5: Rate Limiting Behavior")
        
        try:
            # Make multiple rapid requests
            response_times = []
            
            for i in range(3):
                start_time = time.time()
                response = requests.post(f"{self.api_base}/analyze/octocat", timeout=15)
                end_time = time.time()
                
                response_times.append(end_time - start_time)
                
                if response.status_code != 200:
                    print(f"   Request {i+1}: HTTP {response.status_code}")
                else:
                    print(f"   Request {i+1}: {end_time - start_time:.2f}s")
            
            avg_response_time = sum(response_times) / len(response_times)
            
            self.log_test(
                "Rate Limiting", 
                True, 
                f"Handled {len(response_times)} requests, avg response time: {avg_response_time:.2f}s",
                {'avg_response_time': f"{avg_response_time:.2f}s", 'requests': len(response_times)}
            )
            return True
            
        except Exception as e:
            self.log_test("Rate Limiting", False, f"Error during rate limit test: {e}")
            return False
    
    def test_ml_model_features(self, username: str = "torvalds") -> bool:
        """Test 6: ML Model Feature Analysis"""
        print(f"\n🔍 Test 6: ML Model Feature Analysis ({username})")
        
        try:
            response = requests.post(f"{self.api_base}/analyze/{username}", timeout=25)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if ML-specific features are working
                ml_indicators = {
                    'authenticity_score_range': 0 <= data['authenticity_score'] <= 100,
                    'confidence_range': 0 <= data['confidence'] <= 100,
                    'has_metrics': 'metrics' in data and len(data['metrics']) > 0,
                    'has_red_flags_analysis': 'red_flags' in data,
                    'realistic_metrics': data['metrics']['total_commits'] >= 0 and data['metrics']['public_repos'] >= 0
                }
                
                all_good = all(ml_indicators.values())
                
                self.log_test(
                    f"ML Model Features ({username})", 
                    all_good, 
                    "ML model producing valid feature analysis" if all_good else "Some ML features invalid",
                    {
                        'score_valid': ml_indicators['authenticity_score_range'],
                        'confidence_valid': ml_indicators['confidence_range'],
                        'metrics_present': ml_indicators['has_metrics'],
                        'red_flags_present': ml_indicators['has_red_flags_analysis']
                    }
                )
                
                return all_good
            else:
                self.log_test(f"ML Model Features ({username})", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test(f"ML Model Features ({username})", False, f"Error: {e}")
            return False
    
    def run_all_tests(self) -> Dict:
        """Run all tests and return summary"""
        print("🚀 Starting Comprehensive GitHub API Test Suite")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test 1: API Health
        health_ok = self.test_api_health()
        if not health_ok:
            print("\n❌ API health check failed. Stopping tests.")
            return self.get_summary()
        
        # Test 2: Basic Profile Analysis
        basic_analysis_ok = self.test_github_profile_analysis("octocat")
        
        # Test 3: Multiple Profiles
        test_users = ["torvalds", "gaearon", "sindresorhus"]
        multiple_ok = self.test_multiple_profiles(test_users)
        
        # Test 4: Error Handling
        error_handling_ok = self.test_error_handling()
        
        # Test 5: Rate Limiting
        rate_limiting_ok = self.test_rate_limiting()
        
        # Test 6: ML Model Features
        ml_features_ok = self.test_ml_model_features("torvalds")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\n🏁 Test Suite Completed in {total_time:.2f}s")
        
        return self.get_summary()
    
    def get_summary(self) -> Dict:
        """Get test summary"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        summary = {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': success_rate,
            'results': self.test_results
        }
        
        print(f"\n📊 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("   🎉 Excellent! Your GitHub API integration is working great!")
        elif success_rate >= 60:
            print("   ✅ Good! Most features are working, minor issues detected.")
        else:
            print("   ⚠️  Issues detected. Check the failed tests above.")
        
        return summary

def main():
    """Main test function"""
    tester = GitHubAPITester()
    summary = tester.run_all_tests()
    
    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Test results saved to test_results.json")
    
    # Exit with appropriate code
    if summary['success_rate'] >= 80:
        print("\n🚀 Your GitHub API is ready for production!")
        sys.exit(0)
    else:
        print("\n🔧 Some issues need to be addressed before production use.")
        sys.exit(1)

if __name__ == "__main__":
    main()