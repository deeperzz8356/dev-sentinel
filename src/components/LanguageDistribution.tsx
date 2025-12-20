import { motion } from "framer-motion";

interface Language {
  name: string;
  percentage: number;
  color: string;
}

const languages: Language[] = [
  { name: "TypeScript", percentage: 38, color: "#3178c6" },
  { name: "Python", percentage: 24, color: "#3572A5" },
  { name: "JavaScript", percentage: 18, color: "#f1e05a" },
  { name: "Go", percentage: 12, color: "#00ADD8" },
  { name: "Other", percentage: 8, color: "#6b7280" },
];

export const LanguageDistribution = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="glass rounded-2xl p-6"
    >
      <h3 className="text-lg font-semibold text-foreground mb-6">Language Distribution</h3>
      
      {/* Stacked bar */}
      <div className="h-8 rounded-full overflow-hidden flex mb-6">
        {languages.map((lang, index) => (
          <motion.div
            key={lang.name}
            initial={{ width: 0 }}
            animate={{ width: `${lang.percentage}%` }}
            transition={{ delay: 0.5 + index * 0.1, duration: 0.5 }}
            className="h-full relative group cursor-pointer"
            style={{ backgroundColor: lang.color }}
          >
            <div className="absolute inset-0 bg-white/0 group-hover:bg-white/20 transition-colors" />
            {lang.percentage >= 10 && (
              <span className="absolute inset-0 flex items-center justify-center text-xs font-medium text-white">
                {lang.percentage}%
              </span>
            )}
          </motion.div>
        ))}
      </div>

      {/* Legend */}
      <div className="grid grid-cols-5 gap-4">
        {languages.map((lang, index) => (
          <motion.div
            key={lang.name}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 + index * 0.05 }}
            className="flex items-center gap-2"
          >
            <div 
              className="w-3 h-3 rounded-full flex-shrink-0"
              style={{ backgroundColor: lang.color }}
            />
            <div className="min-w-0">
              <div className="text-sm font-medium text-foreground truncate">{lang.name}</div>
              <div className="text-xs text-muted-foreground">{lang.percentage}%</div>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};
