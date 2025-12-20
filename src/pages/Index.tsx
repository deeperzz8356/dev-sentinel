import { useState } from "react";
import { motion } from "framer-motion";
import { Header } from "@/components/Header";
import { ScoreGauge } from "@/components/ScoreGauge";
import { RedFlagsPanel } from "@/components/RedFlagsPanel";
import { MetricCards } from "@/components/MetricCards";
import { AnalysisTabs } from "@/components/AnalysisTabs";
import { LanguageDistribution } from "@/components/LanguageDistribution";
import { Github, ArrowRight, Sparkles } from "lucide-react";

const mockRedFlags = [
  {
    id: "1",
    title: "Suspicious Commit Timing",
    description: "85% of commits between 2-3 AM on Sundays",
    severity: "high" as const,
    details: "Most developers commit during regular working hours. An unusual concentration of commits during late-night hours on weekends could indicate automated or batch commits, which is a common pattern in purchased or fabricated GitHub profiles.",
  },
  {
    id: "2",
    title: "Low Original Content Ratio",
    description: "Only 23% of repositories are original work",
    severity: "medium" as const,
    details: "While forking repositories is normal, having a high ratio of forked to original repositories suggests limited original contribution. Authentic developers typically have a mix of original projects showcasing their skills.",
  },
];

const mockMetrics = {
  totalCommits: 1247,
  publicRepos: 23,
  followers: 892,
  originalReposPercent: 78,
};

const Index = () => {
  const [username, setUsername] = useState("");
  const [isAnalyzed, setIsAnalyzed] = useState(false);
  const [score] = useState(78);
  const [confidence] = useState(87);

  const handleSearch = () => {
    if (username.trim()) {
      setIsAnalyzed(true);
    }
  };

  return (
    <div className="min-h-screen">
      <Header username={username} setUsername={setUsername} onSearch={handleSearch} />
      
      {!isAnalyzed ? (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] px-6"
        >
          {/* Hero */}
          <div className="text-center max-w-3xl">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="w-24 h-24 rounded-3xl bg-gradient-to-br from-primary to-pink-500 flex items-center justify-center mx-auto mb-8 animate-float"
            >
              <Github className="w-12 h-12 text-primary-foreground" />
            </motion.div>

            <motion.h1
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-5xl md:text-6xl font-display font-bold text-foreground mb-6"
            >
              Analyze GitHub
              <span className="text-gradient block mt-2">Authenticity</span>
            </motion.h1>

            <motion.p
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-xl text-muted-foreground mb-12 max-w-xl mx-auto"
            >
              Detect suspicious patterns, verify developer authenticity, and make informed hiring decisions with AI-powered analysis.
            </motion.p>

            {/* Features */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="grid grid-cols-3 gap-6 max-w-2xl mx-auto"
            >
              {[
                { title: "Pattern Detection", desc: "AI analyzes commit patterns" },
                { title: "Red Flag Alerts", desc: "Identify suspicious activity" },
                { title: "Detailed Reports", desc: "Comprehensive insights" },
              ].map((feature, i) => (
                <div key={i} className="glass rounded-xl p-4 text-center">
                  <Sparkles className="w-6 h-6 text-primary mx-auto mb-2" />
                  <h3 className="font-medium text-foreground text-sm mb-1">{feature.title}</h3>
                  <p className="text-xs text-muted-foreground">{feature.desc}</p>
                </div>
              ))}
            </motion.div>

            {/* CTA */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="mt-12"
            >
              <button 
                onClick={() => {
                  setUsername("octocat");
                  setIsAnalyzed(true);
                }}
                className="group inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-primary to-pink-500 text-primary-foreground font-semibold text-lg hover:opacity-90 transition-all animate-glow-pulse"
              >
                Try Demo Analysis
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
            </motion.div>
          </div>
        </motion.div>
      ) : (
        <motion.main 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="container mx-auto px-6 py-8 max-w-7xl"
        >
          {/* Hero section with score */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Red Flags - Left */}
            <div className="lg:col-span-1">
              <RedFlagsPanel flags={mockRedFlags} />
            </div>

            {/* Score Gauge - Center */}
            <div className="lg:col-span-1">
              <div className="glass rounded-2xl">
                <ScoreGauge score={score} confidence={confidence} />
              </div>
            </div>

            {/* Metrics - Right */}
            <div className="lg:col-span-1">
              <MetricCards metrics={mockMetrics} />
            </div>
          </div>

          {/* Analysis Tabs */}
          <div className="mb-8">
            <AnalysisTabs />
          </div>

          {/* Language Distribution */}
          <LanguageDistribution />
        </motion.main>
      )}
    </div>
  );
};

export default Index;
