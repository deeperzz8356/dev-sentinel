import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Star, GitFork, ExternalLink, AlertTriangle, Search, ChevronDown, Github, Clock } from "lucide-react";
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
  lastUpdated: string;
  isSuspicious?: boolean;
}

const repositories: Repository[] = [
  {
    name: "awesome-react-components",
    description: "A curated list of awesome React components with modern patterns and best practices for building scalable applications",
    stars: 12453,
    forks: 2341,
    isOriginal: true,
    language: "TypeScript",
    languageColor: "#3178c6",
    authenticityScore: 94,
    activityData: [{ value: 30 }, { value: 45 }, { value: 32 }, { value: 67 }, { value: 89 }, { value: 78 }, { value: 92 }],
    lastUpdated: "2 days ago",
  },
  {
    name: "neural-style-transfer",
    description: "Implementation of neural style transfer algorithm using deep learning",
    stars: 8921,
    forks: 1892,
    isOriginal: true,
    language: "Python",
    languageColor: "#3572A5",
    authenticityScore: 87,
    activityData: [{ value: 50 }, { value: 65 }, { value: 48 }, { value: 72 }, { value: 56 }, { value: 84 }, { value: 71 }],
    lastUpdated: "1 week ago",
  },
  {
    name: "react-beautiful-dnd",
    description: "Beautiful and accessible drag and drop for lists with React",
    stars: 4523,
    forks: 892,
    isOriginal: false,
    language: "JavaScript",
    languageColor: "#f1e05a",
    authenticityScore: 32,
    activityData: [{ value: 10 }, { value: 15 }, { value: 8 }, { value: 22 }, { value: 18 }, { value: 12 }, { value: 9 }],
    lastUpdated: "3 months ago",
    isSuspicious: true,
  },
  {
    name: "ml-experiments",
    description: "Various machine learning experiments and models for research",
    stars: 3241,
    forks: 567,
    isOriginal: true,
    language: "Jupyter Notebook",
    languageColor: "#DA5B0B",
    authenticityScore: 91,
    activityData: [{ value: 40 }, { value: 55 }, { value: 62 }, { value: 78 }, { value: 85 }, { value: 91 }, { value: 88 }],
    lastUpdated: "5 days ago",
  },
  {
    name: "dotfiles",
    description: "My personal dotfiles configuration for development environment",
    stars: 234,
    forks: 45,
    isOriginal: true,
    language: "Shell",
    languageColor: "#89e051",
    authenticityScore: 98,
    activityData: [{ value: 20 }, { value: 25 }, { value: 30 }, { value: 28 }, { value: 35 }, { value: 32 }, { value: 38 }],
    lastUpdated: "1 day ago",
  },
  {
    name: "copied-algorithms",
    description: "Collection of algorithms copied from various sources",
    stars: 156,
    forks: 89,
    isOriginal: false,
    language: "C++",
    languageColor: "#f34b7d",
    authenticityScore: 28,
    activityData: [{ value: 5 }, { value: 8 }, { value: 3 }, { value: 12 }, { value: 6 }, { value: 4 }, { value: 2 }],
    lastUpdated: "6 months ago",
    isSuspicious: true,
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

const getSparklineColor = (score: number) => {
  if (score >= 70) return 'hsl(160 84% 39%)';
  if (score >= 40) return 'hsl(38 92% 50%)';
  return 'hsl(0 84% 60%)';
};

type FilterType = 'all' | 'original' | 'high-activity' | 'suspicious';
type SortType = 'activity' | 'stars' | 'authenticity';

export const RepositoryHealthTab = () => {
  const [filter, setFilter] = useState<FilterType>('all');
  const [sort, setSort] = useState<SortType>('activity');
  const [searchQuery, setSearchQuery] = useState('');
  const [hoveredRepo, setHoveredRepo] = useState<string | null>(null);

  const filteredRepos = repositories
    .filter(repo => {
      if (searchQuery && !repo.name.toLowerCase().includes(searchQuery.toLowerCase())) return false;
      switch (filter) {
        case 'original': return repo.isOriginal;
        case 'high-activity': return repo.activityData.reduce((a, b) => a + b.value, 0) > 300;
        case 'suspicious': return repo.isSuspicious || repo.authenticityScore < 40;
        default: return true;
      }
    })
    .sort((a, b) => {
      switch (sort) {
        case 'stars': return b.stars - a.stars;
        case 'authenticity': return b.authenticityScore - a.authenticityScore;
        default: return b.activityData.reduce((acc, d) => acc + d.value, 0) - a.activityData.reduce((acc, d) => acc + d.value, 0);
      }
    });

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="space-y-4"
    >
      {/* Filter/Sort bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        {/* Search */}
        <div className="relative flex-1 max-w-xs">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Filter repositories..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-secondary/50 border border-border/50 text-foreground text-sm placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
          />
        </div>

        {/* Filters */}
        <div className="flex items-center gap-2">
          {(['all', 'original', 'high-activity', 'suspicious'] as FilterType[]).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                filter === f 
                  ? f === 'suspicious' 
                    ? 'bg-destructive/20 text-destructive' 
                    : 'bg-primary/20 text-primary'
                  : 'text-muted-foreground hover:bg-muted/50'
              }`}
            >
              {f === 'all' ? 'All' : f === 'original' ? 'Original Only' : f === 'high-activity' ? 'High Activity' : 'Suspicious'}
            </button>
          ))}
        </div>

        {/* Sort dropdown */}
        <div className="relative group">
          <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-secondary/50 border border-border/50 text-sm text-foreground hover:border-primary/50 transition-colors">
            <span className="text-muted-foreground">Sort:</span>
            <span className="capitalize">{sort === 'activity' ? 'Recent Activity' : sort === 'stars' ? 'Stars' : 'Authenticity'}</span>
            <ChevronDown className="w-4 h-4 text-muted-foreground" />
          </button>
          <div className="absolute right-0 top-full mt-2 w-40 rounded-xl bg-card border border-border/50 shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
            {(['activity', 'stars', 'authenticity'] as SortType[]).map((s) => (
              <button
                key={s}
                onClick={() => setSort(s)}
                className={`w-full px-4 py-2 text-left text-sm first:rounded-t-xl last:rounded-b-xl hover:bg-muted/50 transition-colors ${
                  sort === s ? 'text-primary bg-primary/10' : 'text-foreground'
                }`}
              >
                {s === 'activity' ? 'Recent Activity' : s === 'stars' ? 'Stars' : 'Authenticity'}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Repository list */}
      <div className="space-y-3">
        <AnimatePresence mode="popLayout">
          {filteredRepos.map((repo, index) => (
            <motion.div
              key={repo.name}
              layout
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ delay: index * 0.05 }}
              onMouseEnter={() => setHoveredRepo(repo.name)}
              onMouseLeave={() => setHoveredRepo(null)}
              className={`group glass-hover rounded-xl p-5 transition-all ${
                repo.isSuspicious ? 'border-l-4 border-l-destructive bg-destructive/5' : ''
              }`}
            >
              <div className="flex items-start gap-4">
                {/* Left section - Repo info (60%) */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <Github className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                    <h4 className="font-semibold text-foreground hover:text-primary transition-colors cursor-pointer truncate">
                      {repo.name}
                    </h4>
                    <ExternalLink className="w-3.5 h-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
                    {repo.isSuspicious && (
                      <AlertTriangle className="w-4 h-4 text-destructive flex-shrink-0" />
                    )}
                  </div>

                  <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                    {repo.description}
                  </p>

                  {/* Badges row */}
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`px-2.5 py-1 rounded-md text-xs font-medium ${
                      repo.isOriginal 
                        ? 'bg-success/20 text-success border border-success/30' 
                        : 'bg-muted text-muted-foreground border border-border/50'
                    }`}>
                      {repo.isOriginal ? 'ORIGINAL' : 'FORK'}
                    </span>

                    <span className="flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-secondary/50 border border-border/50">
                      <span 
                        className="w-2.5 h-2.5 rounded-full"
                        style={{ backgroundColor: repo.languageColor }}
                      />
                      {repo.language}
                    </span>

                    <span className="flex items-center gap-1 px-2.5 py-1 rounded-md text-xs text-muted-foreground bg-secondary/50 border border-border/50">
                      <Star className="w-3 h-3" />
                      {repo.stars.toLocaleString()}
                    </span>

                    <span className="flex items-center gap-1 px-2.5 py-1 rounded-md text-xs text-muted-foreground bg-secondary/50 border border-border/50">
                      <GitFork className="w-3 h-3" />
                      {repo.forks.toLocaleString()}
                    </span>
                  </div>

                  {/* Last updated */}
                  <div className="flex items-center gap-1.5 mt-3 text-xs text-muted-foreground/70">
                    <Clock className="w-3 h-3" />
                    Updated {repo.lastUpdated}
                  </div>
                </div>

                {/* Right section (40%) */}
                <div className="flex items-center gap-4">
                  {/* Activity sparkline */}
                  <div className="w-28 h-14 hidden sm:block">
                    <div className="text-[10px] text-muted-foreground/70 mb-1 text-center">Last 30 days</div>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={repo.activityData}>
                        <Line 
                          type="monotone" 
                          dataKey="value" 
                          stroke={getSparklineColor(repo.authenticityScore)}
                          strokeWidth={2}
                          dot={false}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>

                  {/* Authenticity score */}
                  <div className={`relative px-5 py-3 rounded-xl ${getScoreBg(repo.authenticityScore)} text-center min-w-[90px] transition-all ${
                    repo.isSuspicious ? 'ring-2 ring-destructive/50' : ''
                  }`}>
                    {repo.isSuspicious && (
                      <AlertTriangle className="absolute -top-1 -right-1 w-4 h-4 text-destructive" />
                    )}
                    <div className={`text-2xl font-bold ${getScoreColor(repo.authenticityScore)}`}>
                      {repo.authenticityScore}
                    </div>
                    <div className="text-xs text-muted-foreground">Score</div>
                  </div>

                  {/* View Details button */}
                  <motion.button
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ 
                      opacity: hoveredRepo === repo.name ? 1 : 0, 
                      x: hoveredRepo === repo.name ? 0 : 10 
                    }}
                    className="px-4 py-2 rounded-lg bg-primary/20 text-primary text-sm font-medium hover:bg-primary/30 transition-colors whitespace-nowrap"
                  >
                    View Details
                  </motion.button>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Empty state */}
      {filteredRepos.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12"
        >
          <Search className="w-12 h-12 text-muted-foreground/50 mx-auto mb-4" />
          <p className="text-muted-foreground">No repositories match your filters</p>
        </motion.div>
      )}
    </motion.div>
  );
};
