import { Github, Search, Bell, Settings, User } from "lucide-react";
import { motion } from "framer-motion";

interface HeaderProps {
  username: string;
  setUsername: (value: string) => void;
  onSearch: () => void;
}

export const Header = ({ username, setUsername, onSearch }: HeaderProps) => {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      onSearch();
    }
  };

  return (
    <motion.header 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex items-center justify-between px-6 py-4 glass border-b border-border/30"
    >
      {/* Logo */}
      <div className="flex items-center gap-3">
        <div className="relative">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-pink-500 flex items-center justify-center">
            <Github className="w-6 h-6 text-primary-foreground" />
          </div>
          <div className="absolute -inset-1 rounded-xl bg-gradient-to-br from-primary to-pink-500 opacity-30 blur-lg -z-10" />
        </div>
        <h1 className="text-2xl font-display font-bold text-gradient">DevDebt</h1>
      </div>

      {/* Search Bar */}
      <div className="flex-1 max-w-xl mx-8">
        <div className="relative group">
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter GitHub username..."
            className="w-full px-5 py-3 pl-12 rounded-xl bg-secondary/50 border border-border/50 text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-2 focus:ring-primary/20 transition-all duration-300"
          />
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
          <button 
            onClick={onSearch}
            className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-1.5 rounded-lg bg-gradient-to-r from-primary to-pink-500 text-primary-foreground font-medium text-sm hover:opacity-90 transition-opacity animate-glow-pulse"
          >
            Analyze
          </button>
        </div>
      </div>

      {/* User Controls */}
      <div className="flex items-center gap-4">
        <button 
          onClick={() => {
            setUsername("demo-user");
            onSearch();
          }}
          className="px-4 py-2 rounded-lg bg-gradient-to-r from-success to-emerald-500 text-white font-medium text-sm hover:opacity-90 transition-opacity"
        >
          Demo Analysis
        </button>
        <button className="p-2.5 rounded-xl glass-hover text-muted-foreground hover:text-foreground transition-colors">
          <Bell className="w-5 h-5" />
        </button>
        <button className="p-2.5 rounded-xl glass-hover text-muted-foreground hover:text-foreground transition-colors">
          <Settings className="w-5 h-5" />
        </button>
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary/30 to-pink-500/30 flex items-center justify-center border border-border/50">
          <User className="w-5 h-5 text-foreground" />
        </div>
      </div>
    </motion.header>
  );
};
