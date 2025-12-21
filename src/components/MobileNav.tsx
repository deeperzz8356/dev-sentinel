import { motion } from "framer-motion";
import { Home, GitCompare, History, User, Plus } from "lucide-react";

interface MobileNavProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  onNewAnalysis: () => void;
}

const tabs = [
  { id: 'home', icon: Home, label: 'Home' },
  { id: 'compare', icon: GitCompare, label: 'Compare' },
  { id: 'history', icon: History, label: 'History' },
  { id: 'profile', icon: User, label: 'Profile' },
];

export const MobileNav = ({ activeTab, onTabChange, onNewAnalysis }: MobileNavProps) => {
  return (
    <>
      {/* Floating Action Button */}
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileTap={{ scale: 0.9 }}
        onClick={onNewAnalysis}
        className="fixed bottom-24 right-4 z-50 w-14 h-14 rounded-full bg-gradient-to-r from-primary to-pink-500 text-primary-foreground shadow-lg flex items-center justify-center md:hidden"
        style={{ boxShadow: '0 0 30px hsl(262 83% 58% / 0.4)' }}
      >
        <Plus className="w-6 h-6" />
      </motion.button>

      {/* Bottom Navigation */}
      <motion.nav
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        className="fixed bottom-0 left-0 right-0 z-40 glass border-t border-border/50 md:hidden safe-area-inset-bottom"
      >
        <div className="flex items-center justify-around px-2 py-2">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id;
            
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`relative flex flex-col items-center justify-center w-16 h-14 rounded-xl transition-all ${
                  isActive ? 'text-primary' : 'text-muted-foreground'
                }`}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute inset-0 bg-primary/10 rounded-xl"
                  />
                )}
                <tab.icon className={`w-5 h-5 mb-1 relative z-10 ${isActive ? 'scale-110' : ''} transition-transform`} />
                <span className="text-xs relative z-10">{tab.label}</span>
              </button>
            );
          })}
        </div>
      </motion.nav>

      {/* Safe area spacer */}
      <div className="h-20 md:hidden" />
    </>
  );
};
