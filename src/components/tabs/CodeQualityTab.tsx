import { motion } from "framer-motion";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ScatterChart, Scatter, ZAxis, PieChart, Pie, Cell } from "recharts";
import { Code, MessageSquare, FileText, Award } from "lucide-react";

const linesPerCommitData = [
  { range: '1-10', commits: 234 },
  { range: '11-25', commits: 189 },
  { range: '26-50', commits: 145 },
  { range: '51-100', commits: 89 },
  { range: '101-200', commits: 45 },
  { range: '200+', commits: 23 },
];

const scatterData = Array.from({ length: 50 }, () => ({
  size: Math.floor(Math.random() * 200) + 5,
  complexity: Math.floor(Math.random() * 100),
  z: Math.floor(Math.random() * 10) + 1,
}));

const codeRatioData = [
  { name: 'Code', value: 68, color: '#8b5cf6' },
  { name: 'Comments', value: 22, color: '#10b981' },
  { name: 'Whitespace', value: 10, color: '#6b7280' },
];

const qualityMetrics = [
  { label: 'Avg Commit Quality', value: 84, icon: Award, color: 'text-success' },
  { label: 'Code Coverage', value: 72, icon: Code, color: 'text-primary' },
  { label: 'Comment Ratio', value: 22, icon: MessageSquare, color: 'text-success' },
  { label: 'Avg File Size', value: 156, icon: FileText, color: 'text-warning' },
];

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="glass rounded-lg px-3 py-2 text-sm">
        <p className="text-foreground font-medium">{payload[0].value} commits</p>
      </div>
    );
  }
  return null;
};

export const CodeQualityTab = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="space-y-6"
    >
      {/* Metric cards */}
      <div className="grid grid-cols-4 gap-4">
        {qualityMetrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <motion.div
              key={metric.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="glass rounded-xl p-4 text-center"
            >
              <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center mx-auto mb-3">
                <Icon className={`w-5 h-5 ${metric.color}`} />
              </div>
              <div className="text-2xl font-bold text-foreground mb-1">
                {metric.value}{metric.label.includes('Ratio') || metric.label.includes('Coverage') || metric.label.includes('Quality') ? '%' : ''}
              </div>
              <div className="text-xs text-muted-foreground">{metric.label}</div>
            </motion.div>
          );
        })}
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Lines per commit */}
        <div className="glass rounded-xl p-5">
          <h4 className="text-base font-medium text-foreground mb-4">Average Lines per Commit</h4>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={linesPerCommitData} layout="vertical">
              <XAxis type="number" stroke="hsl(215 20% 65%)" fontSize={12} />
              <YAxis dataKey="range" type="category" stroke="hsl(215 20% 65%)" fontSize={12} width={60} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="commits" fill="hsl(262 83% 58%)" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Scatter plot */}
        <div className="glass rounded-xl p-5">
          <h4 className="text-base font-medium text-foreground mb-4">Commit Size vs Complexity</h4>
          <ResponsiveContainer width="100%" height={220}>
            <ScatterChart>
              <XAxis type="number" dataKey="size" name="Size" stroke="hsl(215 20% 65%)" fontSize={12} />
              <YAxis type="number" dataKey="complexity" name="Complexity" stroke="hsl(215 20% 65%)" fontSize={12} />
              <ZAxis type="number" dataKey="z" range={[20, 100]} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Scatter data={scatterData} fill="hsl(262 83% 58%)" fillOpacity={0.6} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Code ratio */}
      <div className="glass rounded-xl p-5">
        <h4 className="text-base font-medium text-foreground mb-4">Code vs Comments vs Whitespace Ratio</h4>
        <div className="flex items-center gap-8">
          <div className="w-48 h-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={codeRatioData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {codeRatioData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex-1 space-y-4">
            {codeRatioData.map((item) => (
              <div key={item.name} className="flex items-center gap-4">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="text-sm text-foreground flex-1">{item.name}</span>
                <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                  <div 
                    className="h-full rounded-full transition-all duration-500"
                    style={{ width: `${item.value}%`, backgroundColor: item.color }}
                  />
                </div>
                <span className="text-sm font-medium text-foreground w-12 text-right">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
