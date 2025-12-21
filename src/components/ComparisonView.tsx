import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowLeftRight, Download, Share2, Plus, Github, Trophy, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { ScoreGauge } from "./ScoreGauge";

interface ProfileData {
  username: string;
  avatar: string;
  score: number;
  confidence: number;
  metrics: {
    commits: number;
    repos: number;
    followers: number;
    originalPercent: number;
  };
}

const profileA: ProfileData = {
  username: "developer-a",
  avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=developer-a",
  score: 94,
  confidence: 91,
  metrics: {
    commits: 2341,
    repos: 45,
    followers: 1892,
    originalPercent: 89,
  },
};

const profileB: ProfileData = {
  username: "developer-b",
  avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=developer-b",
  score: 52,
  confidence: 78,
  metrics: {
    commits: 5678,
    repos: 123,
    followers: 4521,
    originalPercent: 23,
  },
};

interface MetricComparisonProps {
  label: string;
  valueA: number;
  valueB: number;
  format?: (v: number) => string;
  higherIsBetter?: boolean;
}

const MetricComparison = ({ 
  label, 
  valueA, 
  valueB, 
  format = (v) => v.toLocaleString(),
  higherIsBetter = true 
}: MetricComparisonProps) => {
  const diff = valueA - valueB;
  const aWins = higherIsBetter ? diff > 0 : diff < 0;
  const bWins = higherIsBetter ? diff < 0 : diff > 0;
  const tie = diff === 0;

  return (
    <div className="flex items-center gap-4 p-3 rounded-xl bg-muted/30">
      <div className={`flex-1 text-right ${aWins ? 'text-success' : tie ? 'text-muted-foreground' : ''}`}>
        <span className="text-lg font-semibold">{format(valueA)}</span>
        {aWins && <TrendingUp className="w-4 h-4 inline ml-2 text-success" />}
        {bWins && <TrendingDown className="w-4 h-4 inline ml-2 text-destructive" />}
      </div>
      
      <div className="w-24 text-center">
        <span className="text-sm text-muted-foreground">{label}</span>
      </div>
      
      <div className={`flex-1 text-left ${bWins ? 'text-success' : tie ? 'text-muted-foreground' : ''}`}>
        {bWins && <TrendingUp className="w-4 h-4 inline mr-2 text-success" />}
        {aWins && <TrendingDown className="w-4 h-4 inline mr-2 text-destructive" />}
        <span className="text-lg font-semibold">{format(valueB)}</span>
      </div>
    </div>
  );
};

export const ComparisonView = () => {
  const [profiles] = useState<[ProfileData, ProfileData]>([profileA, profileB]);
  const [swapped, setSwapped] = useState(false);

  const [left, right] = swapped ? [profiles[1], profiles[0]] : profiles;

  const getWinner = () => {
    if (left.score > right.score) return 'left';
    if (right.score > left.score) return 'right';
    return 'tie';
  };

  const winner = getWinner();

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen"
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border/50">
        <h2 className="text-xl font-semibold text-foreground">Profile Comparison</h2>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSwapped(!swapped)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-secondary/50 border border-border/50 text-sm text-foreground hover:border-primary/50 transition-colors"
          >
            <ArrowLeftRight className="w-4 h-4" />
            Swap
          </button>
          <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-secondary/50 border border-border/50 text-sm text-foreground hover:border-primary/50 transition-colors">
            <Download className="w-4 h-4" />
            Export
          </button>
          <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-secondary/50 border border-border/50 text-sm text-foreground hover:border-primary/50 transition-colors">
            <Share2 className="w-4 h-4" />
            Share
          </button>
          <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary/20 border border-primary/50 text-sm text-primary hover:bg-primary/30 transition-colors">
            <Plus className="w-4 h-4" />
            Add Profile
          </button>
        </div>
      </div>

      {/* VS Badge */}
      <div className="absolute left-1/2 top-32 -translate-x-1/2 z-10">
        <div className="w-16 h-16 rounded-full bg-gradient-to-r from-primary to-pink-500 flex items-center justify-center shadow-lg">
          <span className="text-xl font-bold text-primary-foreground">VS</span>
        </div>
      </div>

      {/* Comparison Grid */}
      <div className="grid grid-cols-2 gap-0">
        {/* Left Profile */}
        <motion.div
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className={`p-6 border-r border-border/50 ${winner === 'left' ? 'bg-success/5' : ''}`}
        >
          <div className="text-center mb-6">
            <div className="relative inline-block mb-4">
              <img
                src={left.avatar}
                alt={left.username}
                className="w-20 h-20 rounded-full bg-muted"
              />
              {winner === 'left' && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-success flex items-center justify-center"
                >
                  <Trophy className="w-4 h-4 text-success-foreground" />
                </motion.div>
              )}
            </div>
            <div className="flex items-center justify-center gap-2 mb-2">
              <Github className="w-4 h-4 text-muted-foreground" />
              <span className="font-semibold text-foreground">@{left.username}</span>
            </div>
          </div>

          <div className="flex justify-center mb-6">
            <div className="transform scale-75">
              <ScoreGauge score={left.score} confidence={left.confidence} />
            </div>
          </div>
        </motion.div>

        {/* Right Profile */}
        <motion.div
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          className={`p-6 ${winner === 'right' ? 'bg-success/5' : ''}`}
        >
          <div className="text-center mb-6">
            <div className="relative inline-block mb-4">
              <img
                src={right.avatar}
                alt={right.username}
                className="w-20 h-20 rounded-full bg-muted"
              />
              {winner === 'right' && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-success flex items-center justify-center"
                >
                  <Trophy className="w-4 h-4 text-success-foreground" />
                </motion.div>
              )}
            </div>
            <div className="flex items-center justify-center gap-2 mb-2">
              <Github className="w-4 h-4 text-muted-foreground" />
              <span className="font-semibold text-foreground">@{right.username}</span>
            </div>
          </div>

          <div className="flex justify-center mb-6">
            <div className="transform scale-75">
              <ScoreGauge score={right.score} confidence={right.confidence} />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Metrics Comparison */}
      <div className="p-6 space-y-3">
        <h3 className="text-lg font-semibold text-foreground text-center mb-4">Key Metrics</h3>
        
        <MetricComparison 
          label="Authenticity" 
          valueA={left.score} 
          valueB={right.score}
          format={(v) => `${v}%`}
        />
        <MetricComparison 
          label="Commits" 
          valueA={left.metrics.commits} 
          valueB={right.metrics.commits}
        />
        <MetricComparison 
          label="Repositories" 
          valueA={left.metrics.repos} 
          valueB={right.metrics.repos}
        />
        <MetricComparison 
          label="Followers" 
          valueA={left.metrics.followers} 
          valueB={right.metrics.followers}
        />
        <MetricComparison 
          label="Original Repos" 
          valueA={left.metrics.originalPercent} 
          valueB={right.metrics.originalPercent}
          format={(v) => `${v}%`}
        />
      </div>

      {/* Summary */}
      <div className="p-6">
        <div className={`rounded-xl p-4 ${
          winner === 'left' 
            ? 'bg-success/10 border border-success/30' 
            : winner === 'right'
              ? 'bg-success/10 border border-success/30'
              : 'bg-muted/30 border border-border/50'
        }`}>
          <div className="flex items-center gap-2 mb-2">
            <Trophy className={`w-5 h-5 ${winner !== 'tie' ? 'text-success' : 'text-muted-foreground'}`} />
            <span className="font-semibold text-foreground">Analysis Summary</span>
          </div>
          <p className="text-sm text-muted-foreground">
            {winner === 'left' && (
              <>
                <strong className="text-success">@{left.username}</strong> shows more authentic activity patterns 
                with a {left.score}% authenticity score. Higher original repository ratio and consistent commit patterns.
              </>
            )}
            {winner === 'right' && (
              <>
                <strong className="text-success">@{right.username}</strong> shows more authentic activity patterns 
                with a {right.score}% authenticity score. Higher original repository ratio and consistent commit patterns.
              </>
            )}
            {winner === 'tie' && (
              <>Both profiles show similar authenticity levels. Review individual metrics for detailed comparison.</>
            )}
          </p>
        </div>
      </div>
    </motion.div>
  );
};
