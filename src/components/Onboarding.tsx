import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Github, Zap, Brain, BarChart3, ArrowRight, Play, CheckCircle2, X } from "lucide-react";

interface OnboardingProps {
  onComplete: (username?: string) => void;
  onSkip: () => void;
}

const steps = [
  {
    id: 1,
    title: "Welcome to DevDebt",
    subtitle: "Detect GitHub profile authenticity with ML-powered analysis",
    features: [
      { icon: Zap, text: "Instant analysis in seconds" },
      { icon: Brain, text: "AI-powered behavioral detection" },
      { icon: BarChart3, text: "Detailed insights and reports" },
    ],
  },
  {
    id: 2,
    title: "How It Works",
    subtitle: "Three simple steps to uncover the truth",
    steps: [
      { num: 1, text: "Enter any GitHub username" },
      { num: 2, text: "AI analyzes 15+ behavioral metrics" },
      { num: 3, text: "Get authenticity score + detailed insights" },
    ],
  },
  {
    id: 3,
    title: "Try It Now",
    subtitle: "Start with a sample analysis",
    sampleUser: "torvalds",
  },
];

export const Onboarding = ({ onComplete, onSkip }: OnboardingProps) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [customUsername, setCustomUsername] = useState("");

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleAnalyze = (username: string) => {
    onComplete(username);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur-sm"
    >
      {/* Skip button */}
      <button
        onClick={onSkip}
        className="absolute top-6 right-6 flex items-center gap-2 px-4 py-2 rounded-lg text-muted-foreground hover:text-foreground transition-colors"
      >
        Skip
        <X className="w-4 h-4" />
      </button>

      {/* Progress indicator */}
      <div className="absolute top-6 left-1/2 -translate-x-1/2 flex items-center gap-2">
        {steps.map((_, index) => (
          <div
            key={index}
            className={`w-8 h-1 rounded-full transition-colors ${
              index <= currentStep ? 'bg-primary' : 'bg-muted'
            }`}
          />
        ))}
      </div>

      <div className="w-full max-w-2xl px-6">
        <AnimatePresence mode="wait">
          {currentStep === 0 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="text-center"
            >
              {/* Illustration */}
              <motion.div
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2 }}
                className="w-32 h-32 rounded-3xl bg-gradient-to-br from-primary to-pink-500 flex items-center justify-center mx-auto mb-8 shadow-lg glow-primary"
              >
                <Github className="w-16 h-16 text-primary-foreground" />
              </motion.div>

              <motion.h1
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="text-4xl font-bold text-foreground mb-4"
              >
                {steps[0].title}
              </motion.h1>

              <motion.p
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="text-lg text-muted-foreground mb-12"
              >
                {steps[0].subtitle}
              </motion.p>

              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="grid grid-cols-3 gap-4 mb-12"
              >
                {steps[0].features?.map((feature, i) => (
                  <div key={i} className="glass rounded-xl p-4 text-center">
                    <feature.icon className="w-8 h-8 text-primary mx-auto mb-3" />
                    <p className="text-sm text-foreground">{feature.text}</p>
                  </div>
                ))}
              </motion.div>

              <motion.button
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
                onClick={handleNext}
                className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-primary to-pink-500 text-primary-foreground font-semibold text-lg hover:opacity-90 transition-all"
              >
                Get Started
                <ArrowRight className="w-5 h-5" />
              </motion.button>
            </motion.div>
          )}

          {currentStep === 1 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="text-center"
            >
              <motion.h1
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="text-4xl font-bold text-foreground mb-4"
              >
                {steps[1].title}
              </motion.h1>

              <motion.p
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="text-lg text-muted-foreground mb-12"
              >
                {steps[1].subtitle}
              </motion.p>

              {/* Animated diagram */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="flex items-center justify-center gap-4 mb-12"
              >
                {steps[1].steps?.map((step, i) => (
                  <motion.div
                    key={i}
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ delay: 0.3 + i * 0.2 }}
                    className="flex items-center gap-4"
                  >
                    <div className="glass rounded-xl p-6 text-center w-48">
                      <div className="w-10 h-10 rounded-full bg-primary/20 text-primary font-bold flex items-center justify-center mx-auto mb-3">
                        {step.num}
                      </div>
                      <p className="text-sm text-foreground">{step.text}</p>
                    </div>
                    {i < 2 && (
                      <ArrowRight className="w-6 h-6 text-primary" />
                    )}
                  </motion.div>
                ))}
              </motion.div>

              {/* Video preview placeholder */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.8 }}
                className="w-full max-w-md mx-auto aspect-video rounded-xl bg-muted/50 border border-border/50 flex items-center justify-center mb-12 cursor-pointer group hover:border-primary/50 transition-colors"
              >
                <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center group-hover:bg-primary/30 transition-colors">
                  <Play className="w-8 h-8 text-primary ml-1" />
                </div>
              </motion.div>

              <div className="flex items-center justify-center gap-4">
                <button
                  onClick={handleBack}
                  className="px-6 py-3 rounded-xl bg-muted text-foreground font-medium hover:bg-muted/80 transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={handleNext}
                  className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-gradient-to-r from-primary to-pink-500 text-primary-foreground font-semibold hover:opacity-90 transition-all"
                >
                  Next
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </motion.div>
          )}

          {currentStep === 2 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="text-center"
            >
              <motion.h1
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="text-4xl font-bold text-foreground mb-4"
              >
                {steps[2].title}
              </motion.h1>

              <motion.p
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="text-lg text-muted-foreground mb-8"
              >
                {steps[2].subtitle}
              </motion.p>

              {/* Sample analysis option */}
              <motion.button
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
                onClick={() => handleAnalyze(steps[2].sampleUser || 'torvalds')}
                className="w-full max-w-md mx-auto glass rounded-xl p-6 text-left hover:border-primary/50 transition-all group mb-4"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
                      <Github className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <div className="font-semibold text-foreground">Analyze Sample Profile</div>
                      <div className="text-sm text-muted-foreground">@{steps[2].sampleUser}</div>
                    </div>
                  </div>
                  <ArrowRight className="w-5 h-5 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all" />
                </div>
              </motion.button>

              {/* Or divider */}
              <div className="flex items-center gap-4 my-6 max-w-md mx-auto">
                <div className="flex-1 h-px bg-border/50" />
                <span className="text-sm text-muted-foreground">or</span>
                <div className="flex-1 h-px bg-border/50" />
              </div>

              {/* Custom username input */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="w-full max-w-md mx-auto"
              >
                <div className="flex items-center gap-2">
                  <div className="relative flex-1">
                    <Github className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <input
                      type="text"
                      placeholder="Enter your GitHub username"
                      value={customUsername}
                      onChange={(e) => setCustomUsername(e.target.value)}
                      className="w-full pl-12 pr-4 py-4 rounded-xl bg-secondary/50 border border-border/50 text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
                    />
                  </div>
                  <button
                    onClick={() => customUsername && handleAnalyze(customUsername)}
                    disabled={!customUsername}
                    className="px-6 py-4 rounded-xl bg-primary text-primary-foreground font-semibold hover:opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Analyze
                  </button>
                </div>
              </motion.div>

              {/* Quick results preview */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="mt-8 max-w-md mx-auto"
              >
                <p className="text-sm text-muted-foreground mb-4">What you'll see:</p>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    "Authenticity Score",
                    "Commit Patterns",
                    "Red Flags",
                    "Detailed Metrics",
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-2 text-sm text-foreground">
                      <CheckCircle2 className="w-4 h-4 text-success" />
                      {item}
                    </div>
                  ))}
                </div>
              </motion.div>

              <div className="flex items-center justify-center gap-4 mt-8">
                <button
                  onClick={handleBack}
                  className="px-6 py-3 rounded-xl bg-muted text-foreground font-medium hover:bg-muted/80 transition-colors"
                >
                  Back
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};
