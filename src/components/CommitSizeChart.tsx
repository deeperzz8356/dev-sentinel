import { useState } from "react";
import { motion } from "framer-motion";
import { PieChart, Pie, Cell, ResponsiveContainer, Sector } from "recharts";
import { AlertTriangle } from "lucide-react";

interface CommitCategory {
  name: string;
  value: number;
  color: string;
  description: string;
}

const commitData: CommitCategory[] = [
  { name: "Trivial", value: 425, color: "#6b7280", description: "1-5 lines - potential padding" },
  { name: "Small", value: 189, color: "#3b82f6", description: "6-20 lines" },
  { name: "Medium", value: 156, color: "#8b5cf6", description: "21-100 lines" },
  { name: "Large", value: 78, color: "#10b981", description: "101-500 lines" },
  { name: "Massive", value: 23, color: "#f59e0b", description: "500+ lines - potentially suspicious" },
];

const totalCommits = commitData.reduce((sum, item) => sum + item.value, 0);
const trivialPercentage = Math.round((commitData[0].value / totalCommits) * 100);
const hasWarning = trivialPercentage > 40;

const renderActiveShape = (props: any) => {
  const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, fill, payload, percent } = props;

  return (
    <g>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius + 8}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
        style={{ filter: 'drop-shadow(0 0 8px ' + fill + ')' }}
      />
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius - 4}
        outerRadius={innerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
    </g>
  );
};

export const CommitSizeChart = () => {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);

  const onPieEnter = (_: any, index: number) => setActiveIndex(index);
  const onPieLeave = () => setActiveIndex(null);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl p-6"
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-foreground">Commit Size Distribution</h3>
        {hasWarning && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-destructive/20 text-destructive text-sm"
          >
            <AlertTriangle className="w-4 h-4" />
            High trivial commit ratio
          </motion.div>
        )}
      </div>

      <div className="flex flex-col md:flex-row items-center gap-8">
        {/* Donut Chart */}
        <div className="relative w-64 h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <defs>
                {commitData.map((entry, index) => (
                  <linearGradient key={`gradient-${index}`} id={`gradient-${index}`} x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stopColor={entry.color} stopOpacity={1} />
                    <stop offset="100%" stopColor={entry.color} stopOpacity={0.6} />
                  </linearGradient>
                ))}
              </defs>
              <Pie
                data={commitData}
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={100}
                paddingAngle={3}
                dataKey="value"
                activeIndex={activeIndex ?? undefined}
                activeShape={renderActiveShape}
                onMouseEnter={onPieEnter}
                onMouseLeave={onPieLeave}
                animationBegin={0}
                animationDuration={1000}
              >
                {commitData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={`url(#gradient-${index})`}
                    stroke="transparent"
                    style={{ cursor: 'pointer' }}
                  />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          
          {/* Center text */}
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <motion.div
              key={activeIndex}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="text-center"
            >
              {activeIndex !== null ? (
                <>
                  <div className="text-3xl font-bold text-foreground">
                    {commitData[activeIndex].value}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {commitData[activeIndex].name}
                  </div>
                </>
              ) : (
                <>
                  <div className="text-4xl font-bold text-foreground">{totalCommits}</div>
                  <div className="text-sm text-muted-foreground">Total Commits</div>
                </>
              )}
            </motion.div>
          </div>
        </div>

        {/* Legend */}
        <div className="flex-1 space-y-3">
          {commitData.map((item, index) => {
            const percentage = Math.round((item.value / totalCommits) * 100);
            const isActive = activeIndex === index;
            
            return (
              <motion.div
                key={item.name}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                onMouseEnter={() => setActiveIndex(index)}
                onMouseLeave={() => setActiveIndex(null)}
                className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all ${
                  isActive ? 'bg-muted/50 scale-[1.02]' : 'hover:bg-muted/30'
                }`}
              >
                <div 
                  className="w-4 h-4 rounded-full flex-shrink-0"
                  style={{ backgroundColor: item.color, boxShadow: isActive ? `0 0 12px ${item.color}` : 'none' }}
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-foreground">{item.name}</span>
                    <span className="text-sm text-muted-foreground">
                      {item.value} ({percentage}%)
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground/70 truncate">{item.description}</p>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Warning explanation */}
      {hasWarning && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mt-6 p-4 rounded-xl bg-destructive/10 border border-destructive/20"
        >
          <p className="text-sm text-destructive">
            <strong>{trivialPercentage}% of commits</strong> change fewer than 5 lines. 
            This could indicate commit padding or artificial inflation of contribution history.
          </p>
        </motion.div>
      )}
    </motion.div>
  );
};
