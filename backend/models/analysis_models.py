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

class LanguageStats(BaseModel):
    name: str
    percentage: float
    color: str

class CommitPattern(BaseModel):
    hour: int
    day: int
    commits: int

class ProfileAnalysis(BaseModel):
    username: str
    authenticity_score: int  # 0-100
    confidence: int  # 0-100
    red_flags: List[RedFlag]
    metrics: MetricData
    analysis_timestamp: str
    
    # Additional analysis data
    language_distribution: Optional[List[LanguageStats]] = None
    commit_patterns: Optional[List[CommitPattern]] = None
    repository_health: Optional[Dict] = None
    activity_timeline: Optional[List[Dict]] = None

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