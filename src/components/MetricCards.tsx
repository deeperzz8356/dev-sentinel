import { motion } from "framer-motion";
import { GitCommit, FolderGit2, Users, Star, TrendingUp, TrendingDown } from "lucide-react";

interface Metric {
  label: string;
  value: string | number;
  icon: React.ElementType;
  trend?: number;
  trendLabel?: string;
}

interface MetricCardsProps {
  metrics: {
    totalCommits: number;
    publicRepos: number;
    followers: number;
    originalReposPercent: number;
  };
}

export const MetricCards = ({ metrics }: MetricCardsProps) => {
  const cards: Metric[] = [
    {
      label: "Total Commits",
      value: metrics.totalCommits.toLocaleString(),
      icon: GitCommit,
      trend: 12,
      trendLabel: "last month"
    },
    {
      label: "Public Repos",
      value: metrics.publicRepos,
      icon: FolderGit2,
      trend: 3,
      trendLabel: "new this month"
    },
    {
      label: "Followers",
      value: metrics.followers.toLocaleString(),
      icon: Users,
      trend: 8,
      trendLabel: "this week"
    },
    {
      label: "Original Repos",
      value: `${metrics.originalReposPercent}%`,
      icon: Star,
      trend: -2,
      trendLabel: "vs last month"
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-4">
      {cards.map((card, index) => {
        const Icon = card.icon;
        const isPositive = (card.trend ?? 0) >= 0;
        const TrendIcon = isPositive ? TrendingUp : TrendingDown;
        
        return (
          <motion.div
            key={card.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass-hover rounded-2xl p-5 gradient-border"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
                <Icon className="w-5 h-5 text-primary" />
              </div>
              {card.trend !== undefined && (
                <div className={`flex items-center gap-1 text-xs ${
                  isPositive ? 'text-success' : 'text-destructive'
                }`}>
                  <TrendIcon className="w-3 h-3" />
                  <span>{Math.abs(card.trend)}</span>
                </div>
              )}
            </div>
            
            <div className="text-3xl font-bold text-foreground mb-1">
              {card.value}
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">{card.label}</span>
              {card.trendLabel && (
                <span className="text-xs text-muted-foreground/70">{card.trendLabel}</span>
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};
