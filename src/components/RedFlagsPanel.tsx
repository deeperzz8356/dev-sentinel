import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle, CheckCircle2, ChevronDown, ExternalLink } from "lucide-react";
import { useState } from "react";

interface RedFlag {
  id: string;
  title: string;
  description: string;
  severity: "high" | "medium" | "low";
  details?: string;
}

interface RedFlagsPanelProps {
  flags: RedFlag[];
}

const severityColors = {
  high: "bg-destructive/20 text-destructive border-destructive/30",
  medium: "bg-warning/20 text-warning border-warning/30",
  low: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
};

const severityLabels = {
  high: "HIGH",
  medium: "MEDIUM",
  low: "LOW",
};

export const RedFlagsPanel = ({ flags }: RedFlagsPanelProps) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (flags.length === 0) {
    return (
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="glass rounded-2xl p-6 glow-success"
      >
        <div className="flex flex-col items-center justify-center py-8 text-center">
          <div className="w-16 h-16 rounded-full bg-success/20 flex items-center justify-center mb-4">
            <CheckCircle2 className="w-8 h-8 text-success" />
          </div>
          <h3 className="text-xl font-semibold text-foreground mb-2">No Red Flags Detected</h3>
          <p className="text-muted-foreground text-sm">This profile shows authentic activity patterns</p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div 
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="glass rounded-2xl p-6 border-destructive/20"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-destructive/20 flex items-center justify-center">
          <AlertTriangle className="w-5 h-5 text-destructive" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-foreground">Red Flags Detected</h3>
          <p className="text-sm text-muted-foreground">{flags.length} warning{flags.length > 1 ? 's' : ''} found</p>
        </div>
      </div>

      <div className="space-y-3">
        <AnimatePresence>
          {flags.map((flag, index) => (
            <motion.div
              key={flag.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="glass-hover rounded-xl overflow-hidden"
            >
              <button
                onClick={() => setExpandedId(expandedId === flag.id ? null : flag.id)}
                className="w-full p-4 flex items-start gap-4 text-left"
              >
                <div className="w-8 h-8 rounded-lg bg-destructive/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <AlertTriangle className="w-4 h-4 text-destructive" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <h4 className="font-medium text-foreground">{flag.title}</h4>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium border ${severityColors[flag.severity]}`}>
                      {severityLabels[flag.severity]}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground">{flag.description}</p>
                </div>

                <ChevronDown 
                  className={`w-5 h-5 text-muted-foreground transition-transform flex-shrink-0 ${
                    expandedId === flag.id ? 'rotate-180' : ''
                  }`}
                />
              </button>

              <AnimatePresence>
                {expandedId === flag.id && flag.details && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="border-t border-border/50"
                  >
                    <div className="p-4 bg-secondary/30">
                      <p className="text-sm text-muted-foreground mb-3">{flag.details}</p>
                      <button className="flex items-center gap-1.5 text-primary text-sm hover:underline">
                        Learn why this matters <ExternalLink className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};
