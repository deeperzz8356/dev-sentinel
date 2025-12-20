import { motion } from "framer-motion";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from "recharts";
import { CommitHeatmap } from "../CommitHeatmap";

const commitOverTimeData = [
  { month: 'Jan', commits: 45 },
  { month: 'Feb', commits: 62 },
  { month: 'Mar', commits: 38 },
  { month: 'Apr', commits: 91 },
  { month: 'May', commits: 124 },
  { month: 'Jun', commits: 78 },
  { month: 'Jul', commits: 156 },
  { month: 'Aug', commits: 89 },
  { month: 'Sep', commits: 112 },
  { month: 'Oct', commits: 95 },
  { month: 'Nov', commits: 143 },
  { month: 'Dec', commits: 167 },
];

const commitsByDay = [
  { day: 'Mon', commits: 156 },
  { day: 'Tue', commits: 189 },
  { day: 'Wed', commits: 201 },
  { day: 'Thu', commits: 178 },
  { day: 'Fri', commits: 134 },
  { day: 'Sat', commits: 67 },
  { day: 'Sun', commits: 89 },
];

const commitSizeData = [
  { name: 'Small (<10 lines)', value: 45, color: '#10b981' },
  { name: 'Medium (10-50 lines)', value: 35, color: '#8b5cf6' },
  { name: 'Large (50-200 lines)', value: 15, color: '#f59e0b' },
  { name: 'Very Large (>200 lines)', value: 5, color: '#ef4444' },
];

// Generate heatmap data (7 days x 24 hours)
const heatmapData = Array.from({ length: 7 }, () =>
  Array.from({ length: 24 }, () => Math.floor(Math.random() * 25))
);

const suspiciousPatterns = [
  { day: 0, hour: 2 },
  { day: 0, hour: 3 },
  { day: 6, hour: 2 },
  { day: 6, hour: 3 },
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="glass rounded-lg px-3 py-2 text-sm">
        <p className="text-foreground font-medium">{label}</p>
        <p className="text-primary">{payload[0].value} commits</p>
      </div>
    );
  }
  return null;
};

export const CommitPatternsTab = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="space-y-6"
    >
      {/* Commits over time */}
      <div className="glass rounded-xl p-5">
        <h4 className="text-base font-medium text-foreground mb-4">Commits Over Time (Last 12 Months)</h4>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={commitOverTimeData}>
            <XAxis dataKey="month" stroke="hsl(215 20% 65%)" fontSize={12} />
            <YAxis stroke="hsl(215 20% 65%)" fontSize={12} />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey="commits" 
              stroke="hsl(262 83% 58%)" 
              strokeWidth={2}
              dot={{ fill: 'hsl(262 83% 58%)', strokeWidth: 0 }}
              activeDot={{ r: 6, fill: 'hsl(262 83% 65%)' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Heatmap */}
      <CommitHeatmap data={heatmapData} suspiciousPatterns={suspiciousPatterns} />

      <div className="grid grid-cols-2 gap-6">
        {/* Commits by day */}
        <div className="glass rounded-xl p-5">
          <h4 className="text-base font-medium text-foreground mb-4">Commits by Day of Week</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={commitsByDay}>
              <XAxis dataKey="day" stroke="hsl(215 20% 65%)" fontSize={12} />
              <YAxis stroke="hsl(215 20% 65%)" fontSize={12} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="commits" fill="hsl(262 83% 58%)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Commit size distribution */}
        <div className="glass rounded-xl p-5">
          <h4 className="text-base font-medium text-foreground mb-4">Commit Size Distribution</h4>
          <div className="flex items-center justify-center">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={commitSizeData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {commitSizeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-2">
            {commitSizeData.map((item, index) => (
              <div key={index} className="flex items-center gap-2 text-xs text-muted-foreground">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
                <span>{item.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
