import { motion } from "framer-motion";
import { CheckCircle, AlertTriangle, XCircle } from "lucide-react";

interface ScoreGaugeProps {
  score: number;
  confidence: number;
}

export const ScoreGauge = ({ score, confidence }: ScoreGaugeProps) => {
  const getScoreColor = () => {
    if (score >= 70) return { start: "#10b981", end: "#059669", label: "success" };
    if (score >= 40) return { start: "#f59e0b", end: "#d97706", label: "warning" };
    return { start: "#ef4444", end: "#dc2626", label: "destructive" };
  };

  const getStatus = () => {
    if (score >= 70) return { text: "AUTHENTIC", icon: CheckCircle, color: "text-success" };
    if (score >= 40) return { text: "QUESTIONABLE", icon: AlertTriangle, color: "text-warning" };
    return { text: "SUSPICIOUS", icon: XCircle, color: "text-destructive" };
  };

  const colors = getScoreColor();
  const status = getStatus();
  const StatusIcon = status.icon;
  
  const circumference = 2 * Math.PI * 140;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="relative flex flex-col items-center justify-center p-8"
    >
      {/* Outer glow */}
      <div 
        className="absolute inset-0 rounded-full opacity-20 blur-3xl"
        style={{ background: `radial-gradient(circle, ${colors.start} 0%, transparent 70%)` }}
      />
      
      {/* SVG Gauge */}
      <div className="relative w-80 h-80">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 320 320">
          {/* Background circle */}
          <circle
            cx="160"
            cy="160"
            r="140"
            fill="none"
            stroke="hsl(230 25% 20%)"
            strokeWidth="16"
          />
          
          {/* Gradient definition */}
          <defs>
            <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={colors.start} />
              <stop offset="100%" stopColor={colors.end} />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          
          {/* Progress circle */}
          <motion.circle
            cx="160"
            cy="160"
            r="140"
            fill="none"
            stroke="url(#scoreGradient)"
            strokeWidth="16"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            filter="url(#glow)"
          />
        </svg>

        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.5 }}
            className="text-7xl font-display font-bold text-foreground"
          >
            {score}
          </motion.span>
          <span className="text-lg text-muted-foreground mt-1">Authenticity Score</span>
          <span className="text-sm text-muted-foreground/70 mt-1">{confidence}% confidence</span>
        </div>
      </div>

      {/* Status badge */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7, duration: 0.5 }}
        className={`flex items-center gap-2 px-6 py-2.5 rounded-full glass mt-6 ${
          score >= 70 ? 'glow-success' : score >= 40 ? 'glow-warning' : 'glow-destructive'
        }`}
      >
        <StatusIcon className={`w-5 h-5 ${status.color}`} />
        <span className={`font-semibold ${status.color}`}>{status.text}</span>
      </motion.div>
    </motion.div>
  );
};
