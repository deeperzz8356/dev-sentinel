import { useState } from "react";
import { motion } from "framer-motion";
import { Header } from "@/components/Header";
import { ScoreGauge } from "@/components/ScoreGauge";
import { RedFlagsPanel } from "@/components/RedFlagsPanel";
import { MetricCards } from "@/components/MetricCards";
import { ComprehensiveAnalysis } from "@/components/ComprehensiveAnalysis";
import { AnalysisLoading } from "@/components/LoadingStates";
import { useGitHubAnalysis, useHealthCheck } from "@/hooks/useGitHubAnalysis";
import { Github, ArrowRight, Sparkles, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [username, setUsername] = useState("");
  const { toast } = useToast();
  
  const { 
    analyzeProfile, 
    isAnalyzing, 
    analysisData, 
    analysisError, 
    isSuccess,
    reset 
  } = useGitHubAnalysis();
  
  const { data: healthData } = useHealthCheck();

  const handleSearch = () => {
    if (!username.trim()) {
      toast({
        title: "Username Required",
        description: "Please enter a GitHub username to analyze.",
        variant: "destructive",
      });
      return;
    }

    if (!healthData?.ml_model_loaded) {
      toast({
        title: "ML Model Not Ready",
        description: "The ML analysis model is still loading. Please try again in a moment.",
        variant: "destructive",
      });
      return;
    }

    reset(); // Reset previous analysis
    
    // Use mock data for demo or when rate limited
    if (username === "demo-user" || username.startsWith("demo-")) {
      toast({
        title: "Demo Mode",
        description: "Using comprehensive mock data to showcase all 23 features.",
        variant: "default",
      });
    }
    
    analyzeProfile(username);
  };

  return (
    <div className="min-h-screen">
      <Header username={username} setUsername={setUsername} onSearch={handleSearch} />
      
      {/* Health Status Indicator */}
      {healthData && (
        <div className="px-6 py-2">
          <div className={`flex items-center gap-2 text-sm ${
            healthData.ml_model_loaded ? 'text-green-400' : 'text-yellow-400'
          }`}>
            <div className={`w-2 h-2 rounded-full ${
              healthData.ml_model_loaded ? 'bg-green-400' : 'bg-yellow-400'
            }`} />
            ML Model: {healthData.ml_model_loaded ? 'Ready' : 'Loading...'}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isAnalyzing && (
        <div className="px-6 py-8">
          <AnalysisLoading />
        </div>
      )}

      {/* Error State */}
      {analysisError && (
        <div className="px-6 py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass rounded-2xl p-6 border-destructive/30"
          >
            <div className="flex items-center gap-3 text-destructive">
              <AlertCircle className="w-6 h-6" />
              <div>
                <h3 className="font-semibold">Analysis Failed</h3>
                <p className="text-sm text-muted-foreground">
                  {analysisError.message || 'Unable to analyze this profile. Please check the username and try again.'}
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      )}

      {/* Analysis Results */}
      {isSuccess && analysisData && (
        <div className="px-6 py-8 space-y-8">
          {/* Score and Red Flags Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <ScoreGauge 
              score={analysisData.authenticity_score} 
              confidence={analysisData.confidence} 
            />
            <RedFlagsPanel flags={analysisData.red_flags} />
          </div>

          {/* Metrics */}
          <MetricCards metrics={analysisData.metrics} />

          {/* Comprehensive Analysis */}
          <ComprehensiveAnalysis 
            features={analysisData.features}
            repositoryHealth={analysisData.repository_health}
            activityPatterns={analysisData.activity_patterns}
            username={analysisData.username}
          />
        </div>
      )}

      {/* Welcome State */}
      {!isAnalyzing && !isSuccess && !analysisError && (
        <div className="flex flex-col items-center justify-center min-h-[60vh] px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center max-w-2xl"
          >
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary to-pink-500 flex items-center justify-center mx-auto mb-6">
              <Github className="w-10 h-10 text-primary-foreground" />
            </div>
            
            <h1 className="text-4xl font-display font-bold text-gradient mb-4">
              Analyze GitHub Authenticity
            </h1>
            
            <p className="text-xl text-muted-foreground mb-8">
              Enter a GitHub username above to analyze profile authenticity using our advanced ML model
            </p>
            
            <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-primary" />
                <span>ML-Powered Analysis</span>
              </div>
              <div className="flex items-center gap-2">
                <ArrowRight className="w-4 h-4 text-primary" />
                <span>Real-time Results</span>
              </div>
            </div>

            {/* Demo Button */}
            <div className="mt-8">
              <button 
                onClick={() => {
                  setUsername("demo-user");
                  handleSearch();
                }}
                className="group inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-success to-emerald-500 text-white font-semibold text-lg hover:opacity-90 transition-all animate-glow-pulse"
              >
                Try Demo Analysis
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <p className="text-sm text-muted-foreground mt-3">
                Experience all 23 features with realistic mock data
              </p>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default Index;
