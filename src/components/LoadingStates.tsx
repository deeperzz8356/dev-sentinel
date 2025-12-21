import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Github, Search, ArrowRight, Clock, RefreshCw, AlertCircle, Sparkles, Zap, BarChart3, Brain } from "lucide-react";

interface LoadingStateProps {
  onComplete?: () => void;
}

const funFacts = [
  "Did you know? 73% of developers inflate their GitHub profiles",
  "The average developer makes 3.7 commits per week",
  "Most authentic commits happen between 10 AM - 6 PM",
  "Over 50% of GitHub accounts have less than 5 original repos",
  "Genuine developers typically have consistent commit patterns",
];

const steps = [
  { label: "Fetching profile...", range: [0, 25], icon: Github },
  { label: "Analyzing commits...", range: [25, 60], icon: BarChart3 },
  { label: "Running ML model...", range: [60, 85], icon: Brain },
  { label: "Calculating score...", range: [85, 100], icon: Zap },
];

export const AnalysisLoading = ({ onComplete }: LoadingStateProps) => {
  const [progress, setProgress] = useState(0);
  const [currentFact, setCurrentFact] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          onComplete?.();
          return 100;
        }
        return prev + 2;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [onComplete]);

  useEffect(() => {
    const factInterval = setInterval(() => {
      setCurrentFact(prev => (prev + 1) % funFacts.length);
    }, 3000);

    return () => clearInterval(factInterval);
  }, []);

  const currentStep = steps.findIndex(step => progress <= step.range[1]) || steps.length - 1;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col items-center justify-center min-h-[60vh] px-6"
    >
      {/* Animated GitHub icon */}
      <motion.div
        animate={{ 
          scale: [1, 1.1, 1],
          rotate: [0, 5, -5, 0],
        }}
        transition={{ 
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="w-24 h-24 rounded-3xl bg-gradient-to-br from-primary to-pink-500 flex items-center justify-center mb-8 shadow-lg glow-primary"
      >
        <Github className="w-12 h-12 text-primary-foreground" />
      </motion.div>

      {/* Progress steps */}
      <div className="w-full max-w-md mb-8">
        <div className="flex items-center justify-between mb-4">
          {steps.map((step, index) => {
            const StepIcon = step.icon;
            const isActive = index === currentStep;
            const isComplete = index < currentStep;
            
            return (
              <motion.div
                key={step.label}
                initial={{ scale: 0.8, opacity: 0.5 }}
                animate={{ 
                  scale: isActive ? 1.1 : 1,
                  opacity: isActive || isComplete ? 1 : 0.5
                }}
                className={`flex flex-col items-center ${
                  isActive ? 'text-primary' : isComplete ? 'text-success' : 'text-muted-foreground'
                }`}
              >
                <div className={`w-10 h-10 rounded-full flex items-center justify-center mb-2 transition-colors ${
                  isActive 
                    ? 'bg-primary/20 ring-2 ring-primary' 
                    : isComplete 
                      ? 'bg-success/20' 
                      : 'bg-muted/50'
                }`}>
                  <StepIcon className="w-5 h-5" />
                </div>
                <span className="text-xs text-center hidden sm:block">{step.label.replace('...', '')}</span>
              </motion.div>
            );
          })}
        </div>

        {/* Progress bar */}
        <div className="h-2 rounded-full bg-muted/50 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            className="h-full bg-gradient-to-r from-primary to-pink-500 rounded-full"
            style={{ 
              boxShadow: '0 0 20px hsl(262 83% 58% / 0.5)'
            }}
          />
        </div>

        {/* Current step label */}
        <div className="flex items-center justify-between mt-3">
          <span className="text-sm text-primary font-medium">
            {steps[currentStep]?.label}
          </span>
          <span className="text-sm text-muted-foreground">
            ~{Math.ceil((100 - progress) / 20)} seconds
          </span>
        </div>
      </div>

      {/* Animated particles/code effect */}
      <div className="relative w-full max-w-md h-16 overflow-hidden mb-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentFact}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <p className="text-sm text-muted-foreground text-center italic">
              "{funFacts[currentFact]}"
            </p>
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export const EmptyState = ({ onAnalyze }: { onAnalyze: (username: string) => void }) => {
  const exampleUsers = ["torvalds", "gvanrossum", "dhh"];

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] px-6"
    >
      {/* Illustration */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="relative mb-8"
      >
        <div className="w-32 h-32 rounded-3xl bg-gradient-to-br from-primary/20 to-pink-500/20 flex items-center justify-center animate-float">
          <Github className="w-16 h-16 text-primary" />
        </div>
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
          className="absolute -top-2 -right-2 w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center"
        >
          <Search className="w-6 h-6 text-primary" />
        </motion.div>
      </motion.div>

      <motion.h1
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-4xl md:text-5xl font-display font-bold text-foreground mb-4 text-center"
      >
        Discover GitHub Profile
        <span className="text-gradient block">Authenticity</span>
      </motion.h1>

      <motion.p
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="text-lg text-muted-foreground mb-8 text-center max-w-xl"
      >
        Enter any GitHub username to analyze activity patterns and detect suspicious behavior
      </motion.p>

      {/* CTA */}
      <motion.button
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.4 }}
        onClick={() => onAnalyze("octocat")}
        className="group inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-primary to-pink-500 text-primary-foreground font-semibold text-lg hover:opacity-90 transition-all mb-8 animate-glow-pulse"
      >
        Analyze Your First Profile
        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
      </motion.button>

      {/* Example users */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="flex items-center gap-2 mb-12"
      >
        <span className="text-sm text-muted-foreground">Try:</span>
        {exampleUsers.map((user) => (
          <button
            key={user}
            onClick={() => onAnalyze(user)}
            className="px-3 py-1 rounded-lg bg-muted/50 text-primary text-sm hover:bg-muted transition-colors"
          >
            {user}
          </button>
        ))}
      </motion.div>

      {/* Benefits */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl"
      >
        {[
          { icon: Zap, text: "Instant analysis in <10 seconds" },
          { icon: BarChart3, text: "15+ behavioral metrics" },
          { icon: Brain, text: "ML-powered detection" },
        ].map((benefit, i) => (
          <div key={i} className="flex items-center gap-3 p-3 rounded-xl glass">
            <benefit.icon className="w-5 h-5 text-success flex-shrink-0" />
            <span className="text-sm text-foreground">{benefit.text}</span>
          </div>
        ))}
      </motion.div>
    </motion.div>
  );
};

export const ErrorState = ({ 
  type = 'not-found',
  onRetry,
  onBack
}: { 
  type?: 'not-found' | 'rate-limit';
  onRetry?: () => void;
  onBack?: () => void;
}) => {
  const [countdown, setCountdown] = useState(932); // 15:32 in seconds

  useEffect(() => {
    if (type !== 'rate-limit') return;
    
    const interval = setInterval(() => {
      setCountdown(prev => Math.max(0, prev - 1));
    }, 1000);

    return () => clearInterval(interval);
  }, [type]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (type === 'rate-limit') {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex flex-col items-center justify-center min-h-[60vh] px-6"
      >
        <motion.div
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="w-20 h-20 rounded-full bg-warning/20 flex items-center justify-center mb-6"
        >
          <Clock className="w-10 h-10 text-warning" />
        </motion.div>

        <h2 className="text-2xl font-bold text-foreground mb-2">Rate Limit Reached</h2>
        <p className="text-muted-foreground mb-6 text-center max-w-md">
          You've made too many requests. Please wait before trying again.
        </p>

        <div className="text-4xl font-mono font-bold text-warning mb-6">
          {formatTime(countdown)}
        </div>

        <div className="glass rounded-xl p-4 mb-6">
          <p className="text-sm text-muted-foreground">
            Rate limiting helps protect our service. Upgrade to Pro for unlimited analyses.
          </p>
        </div>

        <button className="px-6 py-3 rounded-xl bg-gradient-to-r from-primary to-pink-500 text-primary-foreground font-semibold hover:opacity-90 transition-all">
          Upgrade to Pro
        </button>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center min-h-[60vh] px-6"
    >
      <motion.div
        animate={{ y: [0, -5, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
        className="w-20 h-20 rounded-full bg-destructive/20 flex items-center justify-center mb-6"
      >
        <AlertCircle className="w-10 h-10 text-destructive" />
      </motion.div>

      <h2 className="text-2xl font-bold text-foreground mb-2">Profile Not Found</h2>
      <p className="text-muted-foreground mb-8 text-center max-w-md">
        We couldn't find this GitHub profile. Please check the username and try again.
      </p>

      <div className="glass rounded-xl p-4 mb-8 max-w-sm">
        <h4 className="font-medium text-foreground mb-3">Helpful suggestions:</h4>
        <ul className="space-y-2 text-sm text-muted-foreground">
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-primary" />
            Check the username spelling
          </li>
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-primary" />
            Make sure the profile is public
          </li>
          <li className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-primary" />
            GitHub might be experiencing issues
          </li>
        </ul>
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={onBack}
          className="px-6 py-3 rounded-xl bg-muted text-foreground font-medium hover:bg-muted/80 transition-colors"
        >
          Go Back
        </button>
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-primary text-primary-foreground font-medium hover:opacity-90 transition-all"
        >
          <RefreshCw className="w-4 h-4" />
          Retry
        </button>
      </div>
    </motion.div>
  );
};
