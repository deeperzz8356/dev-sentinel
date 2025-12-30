#!/usr/bin/env python3
"""
Enhanced Red Flag Detection System
Provides more sophisticated and detailed red flag analysis
"""

from typing import Dict, List
from models.analysis_models import RedFlag
import numpy as np
from datetime import datetime, timedelta

class EnhancedRedFlagDetector:
    """Enhanced red flag detection with more sophisticated patterns"""
    
    def __init__(self):
        # Thresholds for different severity levels
        self.thresholds = {
            'weekend_commits': {'medium': 0.4, 'high': 0.6, 'critical': 0.8},
            'night_commits': {'medium': 0.3, 'high': 0.5, 'critical': 0.7},
            'original_ratio': {'medium': 0.4, 'high': 0.2, 'critical': 0.1},
            'activity_consistency': {'medium': 0.4, 'high': 0.2, 'critical': 0.1},
            'commit_frequency': {'low': 5, 'high': 100, 'extreme': 200},
            'burst_activity': {'medium': 0.6, 'high': 0.4, 'critical': 0.2},
            'language_diversity': {'low': 2, 'very_low': 1},
            'follower_ratio': {'low': 0.1, 'high': 5, 'extreme': 20}
        }
    
    def generate_enhanced_red_flags(self, features: Dict, github_data: Dict, ml_prediction: Dict = None) -> List[RedFlag]:
        """Generate comprehensive red flags with enhanced detection"""
        red_flags = []
        
        # 1. Temporal Pattern Analysis
        red_flags.extend(self._analyze_temporal_patterns(features, github_data))
        
        # 2. Repository Quality Analysis
        red_flags.extend(self._analyze_repository_quality(features, github_data))
        
        # 3. Social Behavior Analysis
        red_flags.extend(self._analyze_social_behavior(features, github_data))
        
        # 4. Commit Pattern Analysis
        red_flags.extend(self._analyze_commit_patterns(features, github_data))
        
        # 5. Account Maturity Analysis
        red_flags.extend(self._analyze_account_maturity(features, github_data))
        
        # 6. ML Model Insights (if available)
        if ml_prediction:
            red_flags.extend(self._analyze_ml_insights(ml_prediction, features))
        
        # 7. Cross-Pattern Analysis
        red_flags.extend(self._analyze_cross_patterns(features, github_data))
        
        return red_flags
    
    def _analyze_temporal_patterns(self, features: Dict, github_data: Dict) -> List[RedFlag]:
        """Analyze temporal patterns for suspicious behavior"""
        red_flags = []
        
        # Weekend activity analysis
        weekend_ratio = features.get('weekend_commit_ratio', 0)
        if weekend_ratio > self.thresholds['weekend_commits']['critical']:
            red_flags.append(RedFlag(
                id="extreme_weekend_activity",
                title="Extreme Weekend Activity",
                description=f"{weekend_ratio:.1%} of commits on weekends",
                severity="critical",
                details=f"This profile shows {weekend_ratio:.1%} weekend activity, which is extremely unusual for human developers. Typical developers commit <20% on weekends."
            ))
        elif weekend_ratio > self.thresholds['weekend_commits']['high']:
            red_flags.append(RedFlag(
                id="high_weekend_activity",
                title="High Weekend Activity",
                description=f"{weekend_ratio:.1%} of commits on weekends",
                severity="high",
                details=f"Weekend activity of {weekend_ratio:.1%} is significantly above normal patterns. May indicate automated or batch commits."
            ))
        elif weekend_ratio > self.thresholds['weekend_commits']['medium']:
            red_flags.append(RedFlag(
                id="elevated_weekend_activity",
                title="Elevated Weekend Activity",
                description=f"{weekend_ratio:.1%} of commits on weekends",
                severity="medium",
                details=f"Weekend activity is {weekend_ratio:.1%}, which is higher than typical developer patterns."
            ))
        
        # Night activity analysis
        night_ratio = features.get('night_commit_ratio', 0)
        if night_ratio > self.thresholds['night_commits']['critical']:
            red_flags.append(RedFlag(
                id="extreme_night_activity",
                title="Extreme Night Activity (10PM-6AM)",
                description=f"{night_ratio:.1%} of commits during night hours",
                severity="critical",
                details=f"Night activity of {night_ratio:.1%} is extremely high. Most authentic developers commit <15% during night hours."
            ))
        elif night_ratio > self.thresholds['night_commits']['high']:
            red_flags.append(RedFlag(
                id="high_night_activity",
                title="High Night Activity",
                description=f"{night_ratio:.1%} of commits between 10PM-6AM",
                severity="high",
                details=f"Excessive night commits ({night_ratio:.1%}) may indicate automated activity or unusual work patterns."
            ))
        
        # Timing entropy analysis
        timing_entropy = features.get('timing_entropy', 0.5)
        if timing_entropy < 0.3:
            red_flags.append(RedFlag(
                id="low_timing_entropy",
                title="Highly Predictable Commit Times",
                description="Commits show very regular timing patterns",
                severity="medium",
                details="Low timing entropy suggests commits happen at very predictable times, which may indicate automated activity."
            ))
        
        return red_flags
    
    def _analyze_repository_quality(self, features: Dict, github_data: Dict) -> List[RedFlag]:
        """Analyze repository quality indicators"""
        red_flags = []
        
        # Original content analysis
        original_ratio = features.get('original_repo_ratio', 0)
        if original_ratio < self.thresholds['original_ratio']['critical']:
            red_flags.append(RedFlag(
                id="minimal_original_content",
                title="Minimal Original Content",
                description=f"Only {original_ratio:.1%} of repositories are original",
                severity="critical",
                details=f"With only {original_ratio:.1%} original repositories, this profile shows very little creative work. Authentic developers typically have 60%+ original content."
            ))
        elif original_ratio < self.thresholds['original_ratio']['high']:
            red_flags.append(RedFlag(
                id="low_original_content",
                title="Low Original Content",
                description=f"Only {original_ratio:.1%} of repositories are original",
                severity="high",
                details=f"Original content ratio of {original_ratio:.1%} is below typical developer patterns."
            ))
        
        # Repository naming quality
        repo_naming_quality = features.get('repo_naming_quality', 0.5)
        if repo_naming_quality < 0.3:
            red_flags.append(RedFlag(
                id="poor_repo_naming",
                title="Poor Repository Naming",
                description="Repository names show low quality patterns",
                severity="medium",
                details="Repository names appear generic or poorly structured, which may indicate automated creation."
            ))
        
        # Repository maintenance
        maintenance_score = features.get('maintenance_score', 0.5)
        if maintenance_score < 0.2:
            red_flags.append(RedFlag(
                id="poor_maintenance",
                title="Poor Repository Maintenance",
                description="Repositories show signs of poor maintenance",
                severity="medium",
                details="Low maintenance score suggests repositories are not actively maintained, which is unusual for authentic developers."
            ))
        
        return red_flags
    
    def _analyze_social_behavior(self, features: Dict, github_data: Dict) -> List[RedFlag]:
        """Analyze social behavior patterns"""
        red_flags = []
        
        # Follower-to-repository ratio analysis
        follower_ratio = features.get('follower_repo_ratio', 1)
        if follower_ratio < self.thresholds['follower_ratio']['low']:
            red_flags.append(RedFlag(
                id="very_low_engagement",
                title="Very Low Social Engagement",
                description=f"Follower-to-repository ratio: {follower_ratio:.2f}",
                severity="medium",
                details=f"With a ratio of {follower_ratio:.2f}, this profile has unusually low social engagement for the number of repositories."
            ))
        elif follower_ratio > self.thresholds['follower_ratio']['extreme']:
            red_flags.append(RedFlag(
                id="extreme_social_engagement",
                title="Extreme Social Engagement",
                description=f"Follower-to-repository ratio: {follower_ratio:.2f}",
                severity="high",
                details=f"Ratio of {follower_ratio:.2f} is extremely high, which may indicate purchased followers or bot activity."
            ))
        
        # Profile completeness
        profile_completeness = features.get('profile_completeness', 0.5)
        if profile_completeness < 0.3:
            red_flags.append(RedFlag(
                id="incomplete_profile",
                title="Incomplete Profile Information",
                description="Profile lacks basic information",
                severity="low",
                details="Missing profile information (bio, location, etc.) is common in fake or hastily created accounts."
            ))
        
        return red_flags
    
    def _analyze_commit_patterns(self, features: Dict, github_data: Dict) -> List[RedFlag]:
        """Analyze commit behavior patterns"""
        red_flags = []
        
        # Commit frequency analysis
        commit_freq = features.get('commit_frequency', 0)
        if commit_freq > self.thresholds['commit_frequency']['extreme']:
            red_flags.append(RedFlag(
                id="extreme_commit_frequency",
                title="Extreme Commit Frequency",
                description=f"{commit_freq:.1f} commits per year",
                severity="critical",
                details=f"Committing {commit_freq:.1f} times per year is extremely high and may indicate automated activity."
            ))
        elif commit_freq > self.thresholds['commit_frequency']['high']:
            red_flags.append(RedFlag(
                id="high_commit_frequency",
                title="High Commit Frequency",
                description=f"{commit_freq:.1f} commits per year",
                severity="medium",
                details=f"Commit frequency of {commit_freq:.1f} per year is above typical developer patterns."
            ))
        elif commit_freq < self.thresholds['commit_frequency']['low']:
            red_flags.append(RedFlag(
                id="low_commit_frequency",
                title="Very Low Commit Activity",
                description=f"Only {commit_freq:.1f} commits per year",
                severity="low",
                details="Very low commit frequency may indicate an inactive or showcase-only account."
            ))
        
        # Commit message quality
        commit_msg_quality = features.get('commit_msg_quality', 0.5)
        if commit_msg_quality < 0.3:
            red_flags.append(RedFlag(
                id="poor_commit_messages",
                title="Poor Commit Message Quality",
                description="Commit messages show low quality patterns",
                severity="medium",
                details="Poor commit message quality may indicate automated commits or lack of professional development practices."
            ))
        
        # Burst activity patterns
        burst_score = features.get('burst_activity_score', 0.5)
        if burst_score < self.thresholds['burst_activity']['critical']:
            red_flags.append(RedFlag(
                id="extreme_burst_activity",
                title="Extreme Burst Activity Pattern",
                description="Commits show extreme clustering in time",
                severity="critical",
                details="Extreme burst patterns suggest batch commits or automated activity rather than natural development flow."
            ))
        elif burst_score < self.thresholds['burst_activity']['high']:
            red_flags.append(RedFlag(
                id="burst_activity_detected",
                title="Burst Activity Pattern",
                description="Commits show unusual clustering",
                severity="medium",
                details="Burst activity patterns may indicate batch commits or periods of automated activity."
            ))
        
        return red_flags
    
    def _analyze_account_maturity(self, features: Dict, github_data: Dict) -> List[RedFlag]:
        """Analyze account age and maturity indicators"""
        red_flags = []
        
        account_age_days = github_data.get('account_age_days', 0)
        account_maturity = features.get('account_maturity', 0)
        
        # Very new accounts with high activity
        if account_age_days < 30 and features.get('commit_frequency', 0) > 50:
            red_flags.append(RedFlag(
                id="new_account_high_activity",
                title="New Account with High Activity",
                description=f"Account is {account_age_days} days old with high commit frequency",
                severity="high",
                details="New accounts with immediately high activity may indicate purchased or artificially boosted profiles."
            ))
        
        # Account maturity vs. activity mismatch
        if account_maturity < 0.1 and features.get('public_repos', 0) > 20:
            red_flags.append(RedFlag(
                id="maturity_activity_mismatch",
                title="Account Maturity Mismatch",
                description="High repository count for account age",
                severity="medium",
                details="High repository count relative to account age may indicate bulk repository creation."
            ))
        
        return red_flags
    
    def _analyze_ml_insights(self, ml_prediction: Dict, features: Dict) -> List[RedFlag]:
        """Analyze ML model predictions for insights"""
        red_flags = []
        
        suspicious_prob = ml_prediction.get('suspicious_probability', 0)
        confidence = ml_prediction.get('confidence', 0)
        
        if suspicious_prob > 0.8 and confidence > 0.9:
            red_flags.append(RedFlag(
                id="ml_high_confidence_suspicious",
                title="ML Model: High Confidence Suspicious",
                description=f"ML model indicates {suspicious_prob:.1%} probability of suspicious activity",
                severity="critical",
                details=f"Our trained model shows {suspicious_prob:.1%} confidence that this profile exhibits inauthentic patterns with {confidence:.1%} certainty."
            ))
        elif suspicious_prob > 0.7:
            red_flags.append(RedFlag(
                id="ml_suspicious_patterns",
                title="ML Model: Suspicious Patterns Detected",
                description=f"ML model flags potential suspicious activity ({suspicious_prob:.1%})",
                severity="high",
                details=f"Machine learning analysis indicates {suspicious_prob:.1%} probability of inauthentic behavior patterns."
            ))
        
        return red_flags
    
    def _analyze_cross_patterns(self, features: Dict, github_data: Dict) -> List[RedFlag]:
        """Analyze combinations of patterns that together indicate suspicious behavior"""
        red_flags = []
        
        # High weekend + high night activity combination
        weekend_ratio = features.get('weekend_commit_ratio', 0)
        night_ratio = features.get('night_commit_ratio', 0)
        
        if weekend_ratio > 0.5 and night_ratio > 0.4:
            red_flags.append(RedFlag(
                id="combined_temporal_anomaly",
                title="Combined Temporal Anomaly",
                description="High weekend AND night activity detected",
                severity="critical",
                details=f"Combination of {weekend_ratio:.1%} weekend and {night_ratio:.1%} night activity is extremely unusual and strongly suggests automated behavior."
            ))
        
        # Low original content + high commit frequency
        original_ratio = features.get('original_repo_ratio', 0)
        commit_freq = features.get('commit_frequency', 0)
        
        if original_ratio < 0.3 and commit_freq > 100:
            red_flags.append(RedFlag(
                id="volume_vs_originality_mismatch",
                title="High Volume, Low Originality",
                description="High commit frequency with low original content",
                severity="high",
                details=f"High commit frequency ({commit_freq:.1f}/year) combined with low original content ({original_ratio:.1%}) suggests automated or copied activity."
            ))
        
        # Perfect consistency + other anomalies
        activity_consistency = features.get('activity_consistency', 0.5)
        if activity_consistency > 0.95 and (weekend_ratio > 0.4 or night_ratio > 0.3):
            red_flags.append(RedFlag(
                id="perfect_consistency_anomaly",
                title="Unnaturally Perfect Consistency",
                description="Perfect activity consistency with temporal anomalies",
                severity="high",
                details="Perfect consistency combined with unusual timing patterns strongly suggests automated activity."
            ))
        
        return red_flags
    
    def get_red_flag_summary(self, red_flags: List[RedFlag]) -> Dict:
        """Generate a summary of red flags by severity"""
        summary = {
            'total': len(red_flags),
            'critical': len([rf for rf in red_flags if rf.severity == 'critical']),
            'high': len([rf for rf in red_flags if rf.severity == 'high']),
            'medium': len([rf for rf in red_flags if rf.severity == 'medium']),
            'low': len([rf for rf in red_flags if rf.severity == 'low']),
            'categories': {}
        }
        
        # Categorize red flags
        for rf in red_flags:
            category = rf.id.split('_')[0]  # First part of ID as category
            if category not in summary['categories']:
                summary['categories'][category] = 0
            summary['categories'][category] += 1
        
        return summary