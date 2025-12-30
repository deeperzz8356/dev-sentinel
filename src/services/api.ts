const API_BASE_URL = 'http://localhost:8003';

export interface AnalysisResponse {
  username: string;
  authenticity_score: number;
  confidence: number;
  red_flags: RedFlag[];
  metrics: MetricData;
  features: ComprehensiveFeatures;
  repository_health: RepositoryHealth;
  activity_patterns: ActivityPatterns;
  analysis_timestamp: string;
}

export interface RedFlag {
  id: string;
  title: string;
  description: string;
  severity: 'high' | 'medium' | 'low';
  details?: string;
}

export interface MetricData {
  total_commits: number;
  public_repos: number;
  followers: number;
  original_repos_percent: number;
  activity_consistency: number;
  language_diversity: number;
}

export interface ComprehensiveFeatures {
  // Core activity metrics
  commit_frequency: number;
  weekend_commit_ratio: number;
  night_commit_ratio: number;
  original_repo_ratio: number;
  commit_size_variance: number;
  activity_consistency: number;
  
  // Social & engagement metrics
  follower_repo_ratio: number;
  follower_following_ratio: number;
  language_diversity: number;
  avg_stars_per_repo: number;
  avg_forks_per_repo: number;
  
  // Repository health metrics
  repo_activity_ratio: number;
  commit_msg_quality: number;
  repo_size_variance: number;
  issue_engagement: number;
  account_maturity: number;
  
  // Advanced pattern analysis
  timing_entropy: number;
  repo_naming_quality: number;
  contribution_diversity: number;
  profile_completeness: number;
  collaboration_score: number;
  code_quality_score: number;
  burst_activity_score: number;
  maintenance_score: number;
}

export interface RepositoryHealth {
  total_repositories: number;
  active_repositories: number;
  forked_repositories: number;
  original_repositories: number;
  starred_repositories: number;
  average_repo_size: number;
  languages_used: string[];
  top_repositories: Array<{
    name: string;
    stars: number;
    forks: number;
    language: string;
    last_updated: string;
  }>;
}

export interface ActivityPatterns {
  hourly_distribution: number[];
  daily_distribution: number[];
  monthly_distribution: number[];
  commit_size_distribution: number[];
  language_distribution: Record<string, number>;
  contribution_types: Record<string, number>;
}

class ApiService {
  async analyzeProfile(username: string): Promise<AnalysisResponse> {
    const response = await fetch(`${API_BASE_URL}/analyze/${username}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      // If regular analysis fails, try mock data
      console.log('Regular analysis failed, trying mock data...');
      return this.analyzeMockProfile(username);
    }

    return response.json();
  }

  async analyzeMockProfile(username: string): Promise<AnalysisResponse> {
    const response = await fetch(`${API_BASE_URL}/test-mock/${username}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Mock analysis failed: ${response.statusText}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<{ status: string; ml_model_loaded: boolean }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    
    if (!response.ok) {
      throw new Error('Health check failed');
    }

    return response.json();
  }
}

export const apiService = new ApiService();