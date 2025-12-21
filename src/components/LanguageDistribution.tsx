import { useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, AlertTriangle, Info } from "lucide-react";

interface Language {
  name: string;
  percentage: number;
  color: string;
  bytes: string;
}

const languages: Language[] = [
  { name: "JavaScript", percentage: 28, color: "#f1e05a", bytes: "1.2 MB" },
  { name: "TypeScript", percentage: 24, color: "#3178c6", bytes: "980 KB" },
  { name: "Python", percentage: 18, color: "#3572A5", bytes: "720 KB" },
  { name: "Go", percentage: 12, color: "#00ADD8", bytes: "480 KB" },
  { name: "Rust", percentage: 8, color: "#dea584", bytes: "320 KB" },
  { name: "C++", percentage: 6, color: "#f34b7d", bytes: "240 KB" },
  { name: "Other", percentage: 4, color: "#6b7280", bytes: "160 KB" },
];

const totalBytes = "4.1 MB";
const languageCount = languages.length;
const isDiverse = languageCount >= 5 && languages[0].percentage < 50;

export const LanguageDistribution = () => {
  const [hoveredLanguage, setHoveredLanguage] = useState<string | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="glass rounded-2xl p-6"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="text-lg font-semibold text-foreground">Language Distribution</h3>
          <p className="text-sm text-muted-foreground mt-1">
            {totalBytes} analyzed across {languageCount} languages
          </p>
        </div>
        
        {/* Insight badge */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.6 }}
          className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm ${
            isDiverse 
              ? 'bg-success/20 text-success' 
              : 'bg-warning/20 text-warning'
          }`}
        >
          {isDiverse ? (
            <>
              <CheckCircle2 className="w-4 h-4" />
              Diverse skill set
            </>
          ) : (
            <>
              <AlertTriangle className="w-4 h-4" />
              Limited diversity
            </>
          )}
        </motion.div>
      </div>
      
      {/* Stacked bar */}
      <div className="relative h-14 rounded-2xl overflow-hidden flex mb-6 shadow-inner bg-muted/30">
        {languages.map((lang, index) => {
          const isHovered = hoveredLanguage === lang.name;
          const isSelected = selectedLanguage === lang.name;
          const isActive = isHovered || isSelected;
          
          return (
            <motion.div
              key={lang.name}
              initial={{ width: 0 }}
              animate={{ width: `${lang.percentage}%` }}
              transition={{ delay: 0.5 + index * 0.08, duration: 0.6, ease: "easeOut" }}
              onMouseEnter={() => setHoveredLanguage(lang.name)}
              onMouseLeave={() => setHoveredLanguage(null)}
              onClick={() => setSelectedLanguage(isSelected ? null : lang.name)}
              className="h-full relative cursor-pointer transition-all duration-300"
              style={{ 
                backgroundColor: lang.color,
                filter: isActive ? 'brightness(1.2)' : 'brightness(1)',
                boxShadow: isActive ? `0 0 20px ${lang.color}` : 'none',
                zIndex: isActive ? 10 : 1,
              }}
            >
              {/* Hover overlay */}
              <div className={`absolute inset-0 bg-white/0 transition-colors ${isActive ? 'bg-white/20' : ''}`} />
              
              {/* Percentage label (only for segments >= 10%) */}
              {lang.percentage >= 10 && (
                <span className={`absolute inset-0 flex items-center justify-center text-sm font-medium transition-all ${
                  ['#f1e05a', '#dea584'].includes(lang.color) ? 'text-gray-900' : 'text-white'
                } ${isActive ? 'scale-110' : ''}`}>
                  {lang.percentage}%
                </span>
              )}

              {/* Tooltip */}
              {isHovered && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 px-3 py-2 rounded-lg bg-card border border-border shadow-xl whitespace-nowrap z-20"
                >
                  <div className="flex items-center gap-2 mb-1">
                    <div 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: lang.color }}
                    />
                    <span className="font-medium text-foreground">{lang.name}</span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {lang.percentage}% • {lang.bytes}
                  </div>
                  {/* Tooltip arrow */}
                  <div className="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-t-[6px] border-t-card" />
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        {languages.map((lang, index) => {
          const isSelected = selectedLanguage === lang.name;
          
          return (
            <motion.div
              key={lang.name}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 + index * 0.05 }}
              onMouseEnter={() => setHoveredLanguage(lang.name)}
              onMouseLeave={() => setHoveredLanguage(null)}
              onClick={() => setSelectedLanguage(isSelected ? null : lang.name)}
              className={`flex items-center gap-2 p-2 rounded-lg cursor-pointer transition-all ${
                isSelected || hoveredLanguage === lang.name
                  ? 'bg-muted/70 scale-105' 
                  : 'hover:bg-muted/30'
              }`}
            >
              <div 
                className="w-3 h-3 rounded-full flex-shrink-0 transition-all"
                style={{ 
                  backgroundColor: lang.color,
                  boxShadow: isSelected ? `0 0 10px ${lang.color}` : 'none'
                }}
              />
              <div className="min-w-0">
                <div className="text-sm font-medium text-foreground truncate">{lang.name}</div>
                <div className="text-xs text-muted-foreground">{lang.percentage}%</div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Selected language details */}
      {selectedLanguage && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="mt-6 p-4 rounded-xl bg-muted/30 border border-border/50"
        >
          <div className="flex items-center gap-2 mb-2">
            <Info className="w-4 h-4 text-primary" />
            <span className="font-medium text-foreground">{selectedLanguage} Details</span>
          </div>
          <p className="text-sm text-muted-foreground">
            {languages.find(l => l.name === selectedLanguage)?.bytes} of code analyzed. 
            Click on the bar or legend to highlight different languages.
          </p>
        </motion.div>
      )}
    </motion.div>
  );
};
