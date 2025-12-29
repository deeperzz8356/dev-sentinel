from github import Github
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.github = Github(token) if token else Github()
        self.token = token
        
    async def get_profile_data(self, username: str) -> Dict:
        """
        Fetch comprehensive GitHub profile data for analysis
        """
        try:
            user = self.github.get_user(username)
            
            # Basic user data
            user_data = {
                'username': username,
                'name': user.name,
                'bio': user.bio,
                'location': user.location,
                'company': user.company,
                'blog': user.blog,
                'email': user.email,
                'followers': user.followers,
                'following': user.following,
                'public_repos': user.public_repos,
                'public_gists': user.public_gists,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None,
                'avatar_url': user.avatar_url
            }
            
            # Calculate account age
            if user.created_at:
                # Make both datetimes timezone-aware
                now = datetime.now(user.created_at.tzinfo)
                account_age = now - user.created_at
                account_age_days = account_age.days
            else:
                account_age_days = 0
            
            # Fetch repositories
            repositories = self._get_repositories(user)
            
            # Fetch commits from recent repositories
            commits = self._get_recent_commits(user, repositories[:5])  # Limit to 5 repos
            
            # Fetch language statistics
            languages = self._get_language_stats(repositories)
            
            return {
                'user': user_data,
                'account_age_days': account_age_days,
                'repositories': repositories,
                'commits': commits,
                'languages': languages,
                'username': username
            }
            
        except Exception as e:
            raise Exception(f"Error fetching GitHub data for {username}: {str(e)}")
    
    def _get_repositories(self, user) -> List[Dict]:
        """Fetch repository data"""
        repositories = []
        
        try:
            repos = user.get_repos(sort='updated', direction='desc')
            
            for repo in repos[:30]:  # Limit to 30 most recent repos
                repo_data = {
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description,
                    'private': repo.private,
                    'fork': repo.fork,
                    'created_at': repo.created_at.isoformat() if repo.created_at else None,
                    'updated_at': repo.updated_at.isoformat() if repo.updated_at else None,
                    'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None,
                    'size': repo.size,
                    'stargazers_count': repo.stargazers_count,
                    'watchers_count': repo.watchers_count,
                    'forks_count': repo.forks_count,
                    'language': repo.language,
                    'has_issues': repo.has_issues,
                    'has_projects': repo.has_projects,
                    'has_wiki': repo.has_wiki,
                    'has_pages': repo.has_pages,
                    'open_issues_count': repo.open_issues_count,
                    'default_branch': repo.default_branch,
                    'archived': repo.archived,
                    'disabled': repo.disabled
                }
                repositories.append(repo_data)
                
        except Exception as e:
            print(f"Error fetching repositories: {e}")
            
        return repositories
    
    def _get_recent_commits(self, user, repositories: List[Dict]) -> List[Dict]:
        """Fetch recent commits from repositories"""
        commits = []
        
        try:
            for repo_data in repositories[:3]:  # Limit to 3 repos to avoid rate limits
                try:
                    repo = self.github.get_repo(repo_data['full_name'])
                    repo_commits = repo.get_commits(author=user, since=datetime.now(user.created_at.tzinfo) - timedelta(days=365))
                    
                    for commit in repo_commits[:15]:  # Limit commits per repo
                        commit_data = {
                            'sha': commit.sha,
                            'message': commit.commit.message,
                            'date': commit.commit.author.date.isoformat() if commit.commit.author.date else None,
                            'author_name': commit.commit.author.name,
                            'author_email': commit.commit.author.email,
                            'repository': repo_data['name'],
                            'additions': commit.stats.additions if commit.stats else 0,
                            'deletions': commit.stats.deletions if commit.stats else 0,
                            'total_changes': commit.stats.total if commit.stats else 0
                        }
                        commits.append(commit_data)
                        
                except Exception as e:
                    print(f"Error fetching commits from {repo_data['name']}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching commits: {e}")
            
        return commits
    
    def _get_language_stats(self, repositories: List[Dict]) -> Dict[str, int]:
        """Calculate language distribution from repositories"""
        languages = {}
        
        for repo in repositories:
            if repo.get('language'):
                lang = repo['language']
                languages[lang] = languages.get(lang, 0) + 1
                
        return languages
    
    def get_rate_limit_info(self) -> Dict:
        """Get current rate limit information"""
        rate_limit = self.github.get_rate_limit()
        return {
            'core': {
                'limit': rate_limit.core.limit,
                'remaining': rate_limit.core.remaining,
                'reset': rate_limit.core.reset.isoformat() if rate_limit.core.reset else None
            },
            'search': {
                'limit': rate_limit.search.limit,
                'remaining': rate_limit.search.remaining,
                'reset': rate_limit.search.reset.isoformat() if rate_limit.search.reset else None
            }
        }