import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Calendar, GitCommit, Rocket, Star, Users, Zap, Award, AlertTriangle, Filter, Search, ZoomIn, ZoomOut, ChevronDown } from "lucide-react";

interface TimelineEvent {
  id: string;
  date: string;
  title: string;
  description: string;
  type: "account" | "commit" | "project" | "milestone" | "contribution" | "suspicious";
  icon: React.ElementType;
  metric?: string;
  details?: string;
}

const timelineEvents: TimelineEvent[] = [
  {
    id: "1",
    date: "2019-03-15",
    title: "Account Created",
    description: "GitHub account was created and initialized",
    type: "account",
    icon: Calendar,
    metric: "Day 1",
  },
  {
    id: "2",
    date: "2019-03-18",
    title: "First Commit",
    description: "Initial commit to personal dotfiles repository",
    type: "commit",
    icon: GitCommit,
    metric: "1 file changed",
  },
  {
    id: "3",
    date: "2019-08-22",
    title: "First Major Project",
    description: "Started awesome-react-components repository",
    type: "project",
    icon: Rocket,
    metric: "New repo",
  },
  {
    id: "4",
    date: "2020-02-10",
    title: "1,000 Stars Milestone",
    description: "awesome-react-components reached 1,000 stars",
    type: "milestone",
    icon: Star,
    metric: "1,000 ⭐",
  },
  {
    id: "5",
    date: "2020-05-03",
    title: "Suspicious Activity Detected",
    description: "50 commits in 1 hour at 3 AM on a Sunday",
    type: "suspicious",
    icon: AlertTriangle,
    metric: "50 commits/hr",
    details: "Unusual burst of activity detected. This pattern is often associated with automated or batch commits.",
  },
  {
    id: "6",
    date: "2020-06-15",
    title: "Major Contribution Spike",
    description: "500+ commits in a single month during Hacktoberfest",
    type: "contribution",
    icon: Zap,
    metric: "500+ commits",
  },
  {
    id: "7",
    date: "2021-01-20",
    title: "1,000 Followers",
    description: "Reached 1,000 GitHub followers",
    type: "milestone",
    icon: Users,
    metric: "1,000 followers",
  },
  {
    id: "8",
    date: "2021-09-05",
    title: "10,000 Stars Milestone",
    description: "awesome-react-components reached 10,000 stars",
    type: "milestone",
    icon: Award,
    metric: "10,000 ⭐",
  },
  {
    id: "9",
    date: "2022-03-15",
    title: "3 Year Anniversary",
    description: "3 years on GitHub with consistent contributions",
    type: "account",
    icon: Calendar,
    metric: "3 years",
  },
];

const typeColors: Record<string, string> = {
  account: "bg-primary/20 text-primary border-primary/30",
  commit: "bg-success/20 text-success border-success/30",
  project: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  milestone: "bg-warning/20 text-warning border-warning/30",
  contribution: "bg-pink-500/20 text-pink-400 border-pink-500/30",
  suspicious: "bg-destructive/20 text-destructive border-destructive/30",
};

const typeDotColors: Record<string, string> = {
  account: "bg-primary",
  commit: "bg-success",
  project: "bg-blue-500",
  milestone: "bg-warning",
  contribution: "bg-pink-500",
  suspicious: "bg-destructive",
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

type EventType = TimelineEvent['type'] | 'all';

export const ActivityTimelineTab = () => {
  const [filter, setFilter] = useState<EventType>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedEvent, setExpandedEvent] = useState<string | null>(null);
  const [zoom, setZoom] = useState(1);

  const filteredEvents = timelineEvents
    .filter(event => filter === 'all' || event.type === filter)
    .filter(event => 
      !searchQuery || 
      event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative"
    >
      {/* Controls */}
      <div className="flex flex-wrap items-center gap-4 mb-6">
        {/* Search */}
        <div className="relative flex-1 min-w-[200px] max-w-xs">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search events..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-secondary/50 border border-border/50 text-foreground text-sm placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
          />
        </div>

        {/* Filter dropdown */}
        <div className="relative group">
          <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-secondary/50 border border-border/50 text-sm text-foreground hover:border-primary/50 transition-colors">
            <Filter className="w-4 h-4" />
            <span className="capitalize">{filter === 'all' ? 'All Events' : filter}</span>
            <ChevronDown className="w-4 h-4 text-muted-foreground" />
          </button>
          <div className="absolute left-0 top-full mt-2 w-44 rounded-xl bg-card border border-border/50 shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-10">
            {(['all', 'account', 'commit', 'project', 'milestone', 'contribution', 'suspicious'] as EventType[]).map((t) => (
              <button
                key={t}
                onClick={() => setFilter(t)}
                className={`w-full px-4 py-2 text-left text-sm first:rounded-t-xl last:rounded-b-xl hover:bg-muted/50 transition-colors capitalize ${
                  filter === t ? 'text-primary bg-primary/10' : 'text-foreground'
                }`}
              >
                {t === 'all' ? 'All Events' : t}
              </button>
            ))}
          </div>
        </div>

        {/* Zoom controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setZoom(Math.max(0.5, zoom - 0.25))}
            className="p-2 rounded-lg bg-secondary/50 border border-border/50 text-muted-foreground hover:text-foreground hover:border-primary/50 transition-colors"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="text-sm text-muted-foreground w-12 text-center">{Math.round(zoom * 100)}%</span>
          <button
            onClick={() => setZoom(Math.min(2, zoom + 0.25))}
            className="p-2 rounded-lg bg-secondary/50 border border-border/50 text-muted-foreground hover:text-foreground hover:border-primary/50 transition-colors"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Timeline */}
      <div 
        className="relative"
        style={{ transform: `scale(${zoom})`, transformOrigin: 'top left' }}
      >
        {/* Vertical line */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary via-primary/50 to-transparent" />

        <div className="space-y-1">
          <AnimatePresence mode="popLayout">
            {filteredEvents.map((event, index) => {
              const Icon = event.icon;
              const isExpanded = expandedEvent === event.id;
              const isSuspicious = event.type === 'suspicious';
              
              return (
                <motion.div
                  key={event.id}
                  layout
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ delay: index * 0.05 }}
                  className="relative pl-16 py-4"
                >
                  {/* Icon dot */}
                  <div className={`absolute left-0 w-12 h-12 rounded-xl flex items-center justify-center border transition-all ${typeColors[event.type]} ${
                    isSuspicious ? 'animate-pulse' : ''
                  }`}>
                    <Icon className="w-5 h-5" />
                  </div>

                  {/* Connector dot */}
                  <div className={`absolute left-[22px] top-7 w-3 h-3 rounded-full ring-4 ring-background ${typeDotColors[event.type]}`} />

                  {/* Content */}
                  <motion.div 
                    onClick={() => setExpandedEvent(isExpanded ? null : event.id)}
                    className={`glass-hover rounded-xl p-4 ml-2 cursor-pointer transition-all ${
                      isSuspicious ? 'border-l-4 border-l-destructive bg-destructive/5' : ''
                    } ${isExpanded ? 'ring-2 ring-primary/50' : ''}`}
                  >
                    <div className="flex items-center justify-between gap-3 mb-2">
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className="text-xs text-muted-foreground font-mono">
                          {formatDate(event.date)}
                        </span>
                        <span className={`px-2 py-0.5 rounded text-xs font-medium capitalize ${typeColors[event.type]}`}>
                          {event.type}
                        </span>
                        {isSuspicious && (
                          <span className="px-2 py-0.5 rounded text-xs font-medium bg-destructive text-destructive-foreground">
                            ⚠️ Unusual Pattern
                          </span>
                        )}
                      </div>
                      {event.metric && (
                        <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-1 rounded-md">
                          {event.metric}
                        </span>
                      )}
                    </div>
                    <h4 className="font-medium text-foreground mb-1">{event.title}</h4>
                    <p className="text-sm text-muted-foreground">{event.description}</p>

                    {/* Expanded details */}
                    <AnimatePresence>
                      {isExpanded && event.details && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          exit={{ opacity: 0, height: 0 }}
                          className="mt-3 pt-3 border-t border-border/50"
                        >
                          <p className="text-sm text-muted-foreground">{event.details}</p>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      </div>

      {/* Empty state */}
      {filteredEvents.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12"
        >
          <Calendar className="w-12 h-12 text-muted-foreground/50 mx-auto mb-4" />
          <p className="text-muted-foreground">No events match your filters</p>
        </motion.div>
      )}

      {/* Summary stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        <div className="glass rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-foreground">4+</div>
          <div className="text-xs text-muted-foreground">Years Active</div>
        </div>
        <div className="glass rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-foreground">1,247</div>
          <div className="text-xs text-muted-foreground">Total Commits</div>
        </div>
        <div className="glass rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-foreground">23</div>
          <div className="text-xs text-muted-foreground">Repositories</div>
        </div>
        <div className="glass rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-success">94%</div>
          <div className="text-xs text-muted-foreground">Authenticity</div>
        </div>
      </motion.div>
    </motion.div>
  );
};
