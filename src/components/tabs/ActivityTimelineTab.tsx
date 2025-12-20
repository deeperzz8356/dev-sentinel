import { motion } from "framer-motion";
import { Calendar, GitCommit, Rocket, Star, Users, Zap, Award } from "lucide-react";

interface TimelineEvent {
  id: string;
  date: string;
  title: string;
  description: string;
  type: "account" | "commit" | "project" | "milestone" | "contribution";
  icon: React.ElementType;
}

const timelineEvents: TimelineEvent[] = [
  {
    id: "1",
    date: "2019-03-15",
    title: "Account Created",
    description: "GitHub account was created and initialized",
    type: "account",
    icon: Calendar,
  },
  {
    id: "2",
    date: "2019-03-18",
    title: "First Commit",
    description: "Initial commit to personal dotfiles repository",
    type: "commit",
    icon: GitCommit,
  },
  {
    id: "3",
    date: "2019-08-22",
    title: "First Major Project",
    description: "Started awesome-react-components repository",
    type: "project",
    icon: Rocket,
  },
  {
    id: "4",
    date: "2020-02-10",
    title: "1,000 Stars Milestone",
    description: "awesome-react-components reached 1,000 stars",
    type: "milestone",
    icon: Star,
  },
  {
    id: "5",
    date: "2020-06-15",
    title: "Major Contribution Spike",
    description: "500+ commits in a single month during Hacktoberfest",
    type: "contribution",
    icon: Zap,
  },
  {
    id: "6",
    date: "2021-01-20",
    title: "1,000 Followers",
    description: "Reached 1,000 GitHub followers",
    type: "milestone",
    icon: Users,
  },
  {
    id: "7",
    date: "2021-09-05",
    title: "10,000 Stars Milestone",
    description: "awesome-react-components reached 10,000 stars",
    type: "milestone",
    icon: Award,
  },
  {
    id: "8",
    date: "2022-03-15",
    title: "3 Year Anniversary",
    description: "3 years on GitHub with consistent contributions",
    type: "account",
    icon: Calendar,
  },
];

const typeColors = {
  account: "bg-primary/20 text-primary border-primary/30",
  commit: "bg-success/20 text-success border-success/30",
  project: "bg-blue-500/20 text-blue-400 border-blue-500/30",
  milestone: "bg-warning/20 text-warning border-warning/30",
  contribution: "bg-pink-500/20 text-pink-400 border-pink-500/30",
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};

export const ActivityTimelineTab = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative"
    >
      {/* Vertical line */}
      <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-primary via-primary/50 to-transparent" />

      <div className="space-y-1">
        {timelineEvents.map((event, index) => {
          const Icon = event.icon;
          
          return (
            <motion.div
              key={event.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="relative pl-16 py-4"
            >
              {/* Icon dot */}
              <div className={`absolute left-0 w-12 h-12 rounded-xl flex items-center justify-center border ${typeColors[event.type]}`}>
                <Icon className="w-5 h-5" />
              </div>

              {/* Connector dot */}
              <div className="absolute left-[22px] top-7 w-3 h-3 rounded-full bg-primary ring-4 ring-background" />

              {/* Content */}
              <div className="glass-hover rounded-xl p-4 ml-2">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-xs text-muted-foreground font-mono">
                    {formatDate(event.date)}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium capitalize ${typeColors[event.type]}`}>
                    {event.type}
                  </span>
                </div>
                <h4 className="font-medium text-foreground mb-1">{event.title}</h4>
                <p className="text-sm text-muted-foreground">{event.description}</p>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Summary stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="mt-8 grid grid-cols-4 gap-4"
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
