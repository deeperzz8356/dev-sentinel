import { motion } from "framer-motion";
import { Star, GitFork, ExternalLink, TrendingUp } from "lucide-react";
import { LineChart, Line, ResponsiveContainer } from "recharts";

interface Repository {
  name: string;
  description: string;
  stars: number;
  forks: number;
  isOriginal: boolean;
  language: string;
  languageColor: string;
  authenticityScore: number;
  activityData: { value: number }[];
}

const repositories: Repository[] = [
  {
    name: "awesome-react-components",
    description: "A curated list of awesome React components",
    stars: 12453,
    forks: 2341,
    isOriginal: true,
    language: "TypeScript",
    languageColor: "#3178c6",
    authenticityScore: 94,
    activityData: [{ value: 30 }, { value: 45 }, { value: 32 }, { value: 67 }, { value: 89 }, { value: 78 }, { value: 92 }],
  },
  {
    name: "neural-style-transfer",
    description: "Implementation of neural style transfer algorithm",
    stars: 8921,
    forks: 1892,
    isOriginal: true,
    language: "Python",
    languageColor: "#3572A5",
    authenticityScore: 87,
    activityData: [{ value: 50 }, { value: 65 }, { value: 48 }, { value: 72 }, { value: 56 }, { value: 84 }, { value: 71 }],
  },
  {
    name: "react-beautiful-dnd",
    description: "Beautiful and accessible drag and drop for lists",
    stars: 4523,
    forks: 892,
    isOriginal: false,
    language: "JavaScript",
    languageColor: "#f1e05a",
    authenticityScore: 45,
    activityData: [{ value: 10 }, { value: 15 }, { value: 8 }, { value: 22 }, { value: 18 }, { value: 12 }, { value: 9 }],
  },
  {
    name: "ml-experiments",
    description: "Various machine learning experiments and models",
    stars: 3241,
    forks: 567,
    isOriginal: true,
    language: "Jupyter Notebook",
    languageColor: "#DA5B0B",
    authenticityScore: 91,
    activityData: [{ value: 40 }, { value: 55 }, { value: 62 }, { value: 78 }, { value: 85 }, { value: 91 }, { value: 88 }],
  },
  {
    name: "dotfiles",
    description: "My personal dotfiles configuration",
    stars: 234,
    forks: 45,
    isOriginal: true,
    language: "Shell",
    languageColor: "#89e051",
    authenticityScore: 98,
    activityData: [{ value: 20 }, { value: 25 }, { value: 30 }, { value: 28 }, { value: 35 }, { value: 32 }, { value: 38 }],
  },
];

const getScoreColor = (score: number) => {
  if (score >= 70) return 'text-success';
  if (score >= 40) return 'text-warning';
  return 'text-destructive';
};

const getScoreBg = (score: number) => {
  if (score >= 70) return 'bg-success/20';
  if (score >= 40) return 'bg-warning/20';
  return 'bg-destructive/20';
};

export const RepositoryHealthTab = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="space-y-4"
    >
      {/* Filter/Sort bar */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-sm text-muted-foreground">Sort by:</span>
          <button className="px-3 py-1.5 rounded-lg bg-primary/20 text-primary text-sm font-medium">Stars</button>
          <button className="px-3 py-1.5 rounded-lg text-muted-foreground text-sm hover:bg-muted/50 transition-colors">Activity</button>
          <button className="px-3 py-1.5 rounded-lg text-muted-foreground text-sm hover:bg-muted/50 transition-colors">Score</button>
        </div>
        <div className="flex items-center gap-3">
          <button className="px-3 py-1.5 rounded-lg text-muted-foreground text-sm hover:bg-muted/50 transition-colors">All</button>
          <button className="px-3 py-1.5 rounded-lg text-muted-foreground text-sm hover:bg-muted/50 transition-colors">Original</button>
          <button className="px-3 py-1.5 rounded-lg text-muted-foreground text-sm hover:bg-muted/50 transition-colors">Forked</button>
        </div>
      </div>

      {/* Repository list */}
      <div className="space-y-3">
        {repositories.map((repo, index) => (
          <motion.div
            key={repo.name}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="glass-hover rounded-xl p-4 flex items-center gap-4"
          >
            {/* Repo info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <h4 className="font-medium text-foreground hover:text-primary transition-colors cursor-pointer flex items-center gap-1">
                  {repo.name}
                  <ExternalLink className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100" />
                </h4>
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                  repo.isOriginal 
                    ? 'bg-success/20 text-success' 
                    : 'bg-muted text-muted-foreground'
                }`}>
                  {repo.isOriginal ? 'Original' : 'Fork'}
                </span>
              </div>
              <p className="text-sm text-muted-foreground truncate">{repo.description}</p>
              
              {/* Stats */}
              <div className="flex items-center gap-4 mt-2">
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <Star className="w-4 h-4" />
                  <span>{repo.stars.toLocaleString()}</span>
                </div>
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <GitFork className="w-4 h-4" />
                  <span>{repo.forks.toLocaleString()}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div 
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: repo.languageColor }}
                  />
                  <span className="text-sm text-muted-foreground">{repo.language}</span>
                </div>
              </div>
            </div>

            {/* Activity sparkline */}
            <div className="w-24 h-10">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={repo.activityData}>
                  <Line 
                    type="monotone" 
                    dataKey="value" 
                    stroke="hsl(262 83% 58%)" 
                    strokeWidth={1.5}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Authenticity score */}
            <div className={`px-4 py-2 rounded-lg ${getScoreBg(repo.authenticityScore)} text-center min-w-[80px]`}>
              <div className={`text-xl font-bold ${getScoreColor(repo.authenticityScore)}`}>
                {repo.authenticityScore}
              </div>
              <div className="text-xs text-muted-foreground">Score</div>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};
