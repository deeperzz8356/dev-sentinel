// Force production URL for now - Vercel env var issue
const API_BASE_URL = 'https://devdebt.onrender.com';

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
    // Try production API first
    try {
      const response = await fetch(`${API_BASE_URL}/analyze/${username}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        return response.json();
      }
    } catch (error) {
      console.log('Production API unavailable, using mock data...');
    }

    // Fallback to mock data for demo
    return this.getMockAnalysis(username);
  }

  private getMockAnalysis(username: string): AnalysisResponse {
    // Generate realistic mock data based on username
    const isKnownDev = ['torvalds', 'gaearon', 'tj', 'sindresorhus'].includes(username.toLowerCase());
    const baseScore = isKnownDev ? 85 : Math.floor(Math.random() * 30) + 60;
    
    return {
      username,
      authenticity_score: baseScore,
      confidence: Math.floor(Math.random() * 15) + 85,
      red_flags: [
        {
          id: "demo_mode",
          title: "🎭 Demo Mode Active",
          description: "Using mock data - deploy backend for real ML analysis",
          severity: "low" as const
        },
        ...(baseScore < 75 ? [{
          id: "mock_suspicious",
          title: "Simulated Red Flag",
          description: "This is demo data showing how red flags appear",
          severity: "medium" as const
        }] : [])
      ],
      metrics: {
        total_commits: Math.floor(Math.random() * 2000) + 100,
        public_repos: Math.floor(Math.random() * 25) + 5,
        followers: Math.floor(Math.random() * 1000) + 50,
        original_repos_percent: Math.floor(Math.random() * 40) + 60,
        activity_consistency: Math.floor(Math.random() * 30) + 70,
        language_diversity: Math.floor(Math.random() * 8) + 3
      },
      features: {
        commit_frequency: Math.random() * 50 + 10,
        weekend_commit_ratio: Math.random() * 0.3 + 0.1,
        night_commit_ratio: Math.random() * 0.2 + 0.05,
        original_repo_ratio: Math.random() * 0.4 + 0.6,
        commit_size_variance: Math.random() * 0.5 + 0.2,
        activity_consistency: Math.random() * 0.3 + 0.7,
        follower_repo_ratio: Math.random() * 3 + 0.5,
        follower_following_ratio: Math.random() * 2 + 0.3,
        language_diversity: Math.floor(Math.random() * 8) + 3,
        avg_stars_per_repo: Math.random() * 10 + 1,
        avg_forks_per_repo: Math.random() * 3 + 0.5,
        repo_activity_ratio: Math.random() * 0.4 + 0.6,
        commit_msg_quality: Math.random() * 0.3 + 0.7,
        repo_size_variance: Math.random() * 0.4 + 0.3,
        issue_engagement: Math.random() * 5 + 1,
        account_maturity: Math.random() * 0.5 + 0.5,
        timing_entropy: Math.random() * 0.4 + 0.6,
        repo_naming_quality: Math.random() * 0.3 + 0.7,
        contribution_diversity: Math.random() * 0.4 + 0.6,
        profile_completeness: Math.random() * 0.3 + 0.7,
        collaboration_score: Math.random() * 0.4 + 0.6,
        code_quality_score: Math.random() * 0.3 + 0.7,
        burst_activity_score: Math.random() * 0.4 + 0.6,
        maintenance_score: Math.random() * 0.3 + 0.7
      } as ComprehensiveFeatures,
      repository_health: {
        total_repositories: Math.floor(Math.random() * 25) + 5,
        active_repositories: Math.floor(Math.random() * 15) + 3,
        forked_repositories: Math.floor(Math.random() * 10) + 2,
        original_repositories: Math.floor(Math.random() * 15) + 5,
        starred_repositories: Math.floor(Math.random() * 20) + 3,
        average_repo_size: Math.floor(Math.random() * 5000) + 500,
        languages_used: ['JavaScript', 'TypeScript', 'Python', 'Go'].slice(0, Math.floor(Math.random() * 4) + 2),
        top_repositories: [
          {
            name: `${username}-project-1`,
            stars: Math.floor(Math.random() * 100) + 10,
            forks: Math.floor(Math.random() * 20) + 2,
            language: 'JavaScript',
            last_updated: new Date(Date.now() - Math.random() * 90 * 24 * 60 * 60 * 1000).toISOString()
          }
        ]
      } as RepositoryHealth,
      activity_patterns: {
        hourly_distribution: Array.from({length: 24}, () => Math.floor(Math.random() * 50)),
        daily_distribution: Array.from({length: 7}, () => Math.floor(Math.random() * 100)),
        monthly_distribution: Array.from({length: 12}, () => Math.floor(Math.random() * 200)),
        commit_size_distribution: Array.from({length: 10}, () => Math.floor(Math.random() * 30)),
        language_distribution: {
          'JavaScript': Math.floor(Math.random() * 50) + 20,
          'TypeScript': Math.floor(Math.random() * 30) + 10,
          'Python': Math.floor(Math.random() * 40) + 15
        },
        contribution_types: {
          'features': Math.floor(Math.random() * 100) + 50,
          'fixes': Math.floor(Math.random() * 80) + 30,
          'refactoring': Math.floor(Math.random() * 40) + 10,
          'documentation': Math.floor(Math.random() * 30) + 5,
          'testing': Math.floor(Math.random() * 25) + 5,
          'other': Math.floor(Math.random() * 20) + 5
        }
      } as ActivityPatterns,
      analysis_timestamp: new Date().toISOString()
    };
  }

  async healthCheck(): Promise<{ status: string; ml_model_loaded: boolean }> {
    try {
      console.log('🔍 Checking backend health at:', API_BASE_URL);
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      console.log('📡 Backend response status:', response.status);
      
      if (!response.ok) {
        console.error('❌ Backend health check failed:', response.statusText);
        throw new Error(`Health check failed: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      console.log('✅ Backend health check result:', result);
      return result;
    } catch (error) {
      console.error('❌ Backend connection error:', error);
      return {
        status: "offline",
        ml_model_loaded: false
      };
    }
  }
}

export const apiService = new ApiService();