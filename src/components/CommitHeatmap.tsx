import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";

interface CommitHeatmapProps {
  data: number[][];
  suspiciousPatterns?: { day: number; hour: number }[];
}

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const hours = Array.from({ length: 24 }, (_, i) => i);

const getIntensityColor = (commits: number, isSuspicious: boolean) => {
  if (isSuspicious) return 'bg-destructive/60 ring-2 ring-destructive';
  if (commits === 0) return 'bg-muted';
  if (commits <= 5) return 'bg-primary/30';
  if (commits <= 10) return 'bg-primary/50';
  if (commits <= 20) return 'bg-primary/70';
  return 'bg-primary';
};

export const CommitHeatmap = ({ data, suspiciousPatterns = [] }: CommitHeatmapProps) => {
  const isSuspicious = (day: number, hour: number) => {
    return suspiciousPatterns.some(p => p.day === day && p.hour === hour);
  };

  const totalSuspicious = suspiciousPatterns.length;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl p-6"
    >
      <h3 className="text-lg font-semibold text-foreground mb-4">Commit Activity Heatmap</h3>
      
      <div className="overflow-x-auto">
        <div className="min-w-[700px]">
          {/* Hour labels */}
          <div className="flex gap-1 mb-2 ml-12">
            {hours.filter((_, i) => i % 3 === 0).map(hour => (
              <div key={hour} className="w-8 text-center text-xs text-muted-foreground" style={{ marginLeft: hour === 0 ? 0 : '16px' }}>
                {hour.toString().padStart(2, '0')}
              </div>
            ))}
          </div>

          {/* Grid */}
          <div className="space-y-1">
            {days.map((day, dayIndex) => (
              <div key={day} className="flex items-center gap-1">
                <span className="w-10 text-xs text-muted-foreground text-right pr-2">{day}</span>
                <div className="flex gap-0.5">
                  {hours.map(hour => {
                    const commits = data[dayIndex]?.[hour] ?? 0;
                    const suspicious = isSuspicious(dayIndex, hour);
                    return (
                      <motion.div
                        key={hour}
                        initial={{ opacity: 0, scale: 0 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: (dayIndex * 24 + hour) * 0.002 }}
                        className={`w-3 h-3 rounded-sm cursor-pointer transition-transform hover:scale-150 ${getIntensityColor(commits, suspicious)}`}
                        title={`${day} ${hour}:00 - ${commits} commits${suspicious ? ' (suspicious)' : ''}`}
                      />
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Legend */}
          <div className="flex items-center justify-between mt-6 text-xs text-muted-foreground">
            <div className="flex items-center gap-4">
              <span>Less</span>
              <div className="flex gap-1">
                <div className="w-3 h-3 rounded-sm bg-muted" />
                <div className="w-3 h-3 rounded-sm bg-primary/30" />
                <div className="w-3 h-3 rounded-sm bg-primary/50" />
                <div className="w-3 h-3 rounded-sm bg-primary/70" />
                <div className="w-3 h-3 rounded-sm bg-primary" />
              </div>
              <span>More</span>
            </div>
            
            {totalSuspicious > 0 && (
              <div className="flex items-center gap-2 text-warning">
                <AlertTriangle className="w-4 h-4" />
                <span>{totalSuspicious} suspicious time slots detected</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
