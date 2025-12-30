from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class RedFlag(BaseModel):
    id: str
    title: str
    description: str
    severity: str  # "high", "medium", "low"
    details: Optional[str] = None

class MetricData(BaseModel):
    total_commits: int
    public_repos: int
    followers: int
    original_repos_percent: int
    activity_consistency: int
    language_diversity: int

class ComprehensiveFeatures(BaseModel):
    # Core activity metrics
    commit_frequency: float
    weekend_commit_ratio: float
    night_commit_ratio: float
    original_repo_ratio: float
    commit_size_variance: float
    activity_consistency: float
    
    # Social & engagement metrics
    follower_repo_ratio: float
    follower_following_ratio: float
    language_diversity: float
    avg_stars_per_repo: float
    avg_forks_per_repo: float
    
    # Repository health metrics
    repo_activity_ratio: float
    commit_msg_quality: float
    repo_size_variance: float
    issue_engagement: float
    account_maturity: float
    
    # Advanced pattern analysis
    timing_entropy: float
    repo_naming_quality: float
    contribution_diversity: float
    profile_completeness: float
    collaboration_score: float
    code_quality_score: float
    burst_activity_score: float
    maintenance_score: float

class RepositoryInfo(BaseModel):
    name: str
    stars: int
    forks: int
    language: Optional[str]
    last_updated: str

class RepositoryHealth(BaseModel):
    total_repositories: int
    active_repositories: int
    forked_repositories: int
    original_repositories: int
    starred_repositories: int
    average_repo_size: float
    languages_used: List[str]
    top_repositories: List[RepositoryInfo]

class ActivityPatterns(BaseModel):
    hourly_distribution: List[int]
    daily_distribution: List[int]
    monthly_distribution: List[int]
    commit_size_distribution: List[int]
    language_distribution: Dict[str, int]
    contribution_types: Dict[str, int]

class ProfileAnalysis(BaseModel):
    username: str
    authenticity_score: int  # 0-100
    confidence: int  # 0-100
    red_flags: List[RedFlag]
    metrics: MetricData
    features: ComprehensiveFeatures
    repository_health: RepositoryHealth
    activity_patterns: ActivityPatterns
    analysis_timestamp: str

class GitHubUser(BaseModel):
    username: str
    name: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    company: Optional[str]
    blog: Optional[str]
    email: Optional[str]
    followers: int
    following: int
    public_repos: int
    public_gists: int
    created_at: Optional[str]
    updated_at: Optional[str]
    avatar_url: Optional[str]

class Repository(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    private: bool
    fork: bool
    created_at: Optional[str]
    updated_at: Optional[str]
    pushed_at: Optional[str]
    size: int
    stargazers_count: int
    watchers_count: int
    forks_count: int
    language: Optional[str]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    open_issues_count: int
    default_branch: str
    archived: bool
    disabled: bool

class Commit(BaseModel):
    sha: str
    message: str
    date: Optional[str]
    author_name: Optional[str]
    author_email: Optional[str]
    repository: str
    additions: int
    deletions: int
    total_changes: int