const API_BASE_URL = 'http://localhost:8000';

export interface AnalysisResponse {
  username: string;
  authenticity_score: number;
  confidence: number;
  red_flags: RedFlag[];
  metrics: MetricData;
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

class ApiService {
  async analyzeProfile(username: string): Promise<AnalysisResponse> {
    const response = await fetch(`${API_BASE_URL}/analyze/${username}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
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