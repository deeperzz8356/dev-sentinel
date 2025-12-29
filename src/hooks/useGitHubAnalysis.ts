import { useQuery, useMutation } from '@tanstack/react-query';
import { apiService, AnalysisResponse } from '@/services/api';

export const useGitHubAnalysis = () => {
  const analyzeMutation = useMutation({
    mutationFn: (username: string) => apiService.analyzeProfile(username),
    onError: (error) => {
      console.error('Analysis failed:', error);
    },
  });

  return {
    analyzeProfile: analyzeMutation.mutate,
    isAnalyzing: analyzeMutation.isPending,
    analysisData: analyzeMutation.data,
    analysisError: analyzeMutation.error,
    isSuccess: analyzeMutation.isSuccess,
    reset: analyzeMutation.reset,
  };
};

export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => apiService.healthCheck(),
    refetchInterval: 30000, // Check every 30 seconds
  });
};