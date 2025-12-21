import { useState } from "react";
import { motion } from "framer-motion";
import { 
  User, Palette, Bell, Lock, CreditCard, Settings, HelpCircle,
  Sun, Moon, Monitor, Check, Trash2, Download, Key, Webhook,
  Sliders, Bug, ChevronRight
} from "lucide-react";

type SettingsSection = 'profile' | 'appearance' | 'notifications' | 'privacy' | 'billing' | 'advanced' | 'help';
type Theme = 'dark' | 'light' | 'auto';
type Density = 'comfortable' | 'compact' | 'spacious';
type DataViz = 'modern' | 'minimal' | 'detailed';
type FontSize = 'small' | 'medium' | 'large';

const sections = [
  { id: 'profile' as SettingsSection, icon: User, label: 'Profile' },
  { id: 'appearance' as SettingsSection, icon: Palette, label: 'Appearance' },
  { id: 'notifications' as SettingsSection, icon: Bell, label: 'Notifications' },
  { id: 'privacy' as SettingsSection, icon: Lock, label: 'Privacy' },
  { id: 'billing' as SettingsSection, icon: CreditCard, label: 'Billing' },
  { id: 'advanced' as SettingsSection, icon: Settings, label: 'Advanced' },
  { id: 'help' as SettingsSection, icon: HelpCircle, label: 'Help & Support' },
];

const accentColors = [
  { id: 'purple', color: '#8b5cf6' },
  { id: 'blue', color: '#3b82f6' },
  { id: 'green', color: '#10b981' },
  { id: 'red', color: '#ef4444' },
  { id: 'orange', color: '#f59e0b' },
  { id: 'pink', color: '#ec4899' },
];

export const SettingsPage = () => {
  const [activeSection, setActiveSection] = useState<SettingsSection>('appearance');
  const [theme, setTheme] = useState<Theme>('dark');
  const [accentColor, setAccentColor] = useState('purple');
  const [density, setDensity] = useState<Density>('comfortable');
  const [dataViz, setDataViz] = useState<DataViz>('modern');
  const [fontSize, setFontSize] = useState<FontSize>('medium');
  const [notifications, setNotifications] = useState({
    email: true,
    analysisComplete: true,
    weeklySummary: false,
    newFeatures: true,
    security: true,
  });
  const [privacy, setPrivacy] = useState({
    publicProfile: false,
    anonymousMode: false,
    dataRetention: '90',
  });
  const [advanced, setAdvanced] = useState({
    debugMode: false,
    sensitivity: 50,
  });

  const renderSection = () => {
    switch (activeSection) {
      case 'appearance':
        return (
          <div className="space-y-8">
            {/* Theme */}
            <div>
              <h4 className="text-sm font-medium text-foreground mb-4">Theme</h4>
              <div className="flex items-center gap-3">
                {[
                  { id: 'dark' as Theme, icon: Moon, label: 'Dark' },
                  { id: 'light' as Theme, icon: Sun, label: 'Light' },
                  { id: 'auto' as Theme, icon: Monitor, label: 'Auto' },
                ].map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setTheme(t.id)}
                    className={`flex-1 flex items-center justify-center gap-2 p-4 rounded-xl border transition-all ${
                      theme === t.id
                        ? 'border-primary bg-primary/10 text-primary'
                        : 'border-border/50 text-muted-foreground hover:border-primary/50'
                    }`}
                  >
                    <t.icon className="w-5 h-5" />
                    <span>{t.label}</span>
                    {theme === t.id && <Check className="w-4 h-4 ml-auto" />}
                  </button>
                ))}
              </div>
            </div>

            {/* Accent Color */}
            <div>
              <h4 className="text-sm font-medium text-foreground mb-4">Accent Color</h4>
              <div className="flex items-center gap-3">
                {accentColors.map((c) => (
                  <button
                    key={c.id}
                    onClick={() => setAccentColor(c.id)}
                    className={`w-10 h-10 rounded-full transition-all ${
                      accentColor === c.id ? 'ring-2 ring-offset-2 ring-offset-background ring-primary' : ''
                    }`}
                    style={{ backgroundColor: c.color }}
                  >
                    {accentColor === c.id && (
                      <Check className="w-5 h-5 mx-auto text-white" />
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Density */}
            <div>
              <h4 className="text-sm font-medium text-foreground mb-4">Dashboard Density</h4>
              <div className="flex items-center gap-3">
                {(['comfortable', 'compact', 'spacious'] as Density[]).map((d) => (
                  <button
                    key={d}
                    onClick={() => setDensity(d)}
                    className={`flex-1 p-3 rounded-xl border transition-all capitalize ${
                      density === d
                        ? 'border-primary bg-primary/10 text-primary'
                        : 'border-border/50 text-muted-foreground hover:border-primary/50'
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>
            </div>

            {/* Data Viz Style */}
            <div>
              <h4 className="text-sm font-medium text-foreground mb-4">Data Visualization Style</h4>
              <div className="flex items-center gap-3">
                {(['modern', 'minimal', 'detailed'] as DataViz[]).map((v) => (
                  <button
                    key={v}
                    onClick={() => setDataViz(v)}
                    className={`flex-1 p-3 rounded-xl border transition-all capitalize ${
                      dataViz === v
                        ? 'border-primary bg-primary/10 text-primary'
                        : 'border-border/50 text-muted-foreground hover:border-primary/50'
                    }`}
                  >
                    {v}
                  </button>
                ))}
              </div>
            </div>

            {/* Font Size */}
            <div>
              <h4 className="text-sm font-medium text-foreground mb-4">Font Size</h4>
              <div className="flex items-center gap-3">
                {(['small', 'medium', 'large'] as FontSize[]).map((f) => (
                  <button
                    key={f}
                    onClick={() => setFontSize(f)}
                    className={`flex-1 p-3 rounded-xl border transition-all capitalize ${
                      fontSize === f
                        ? 'border-primary bg-primary/10 text-primary'
                        : 'border-border/50 text-muted-foreground hover:border-primary/50'
                    }`}
                  >
                    {f}
                  </button>
                ))}
              </div>
            </div>
          </div>
        );

      case 'notifications':
        return (
          <div className="space-y-4">
            {[
              { key: 'email', label: 'Email Notifications', desc: 'Receive notifications via email' },
              { key: 'analysisComplete', label: 'Analysis Complete', desc: 'Get notified when analysis finishes' },
              { key: 'weeklySummary', label: 'Weekly Summary', desc: 'Receive weekly activity digest' },
              { key: 'newFeatures', label: 'New Features', desc: 'Learn about new features and updates' },
              { key: 'security', label: 'Security Alerts', desc: 'Important security notifications' },
            ].map((item) => (
              <div key={item.key} className="flex items-center justify-between p-4 rounded-xl border border-border/50">
                <div>
                  <div className="font-medium text-foreground">{item.label}</div>
                  <div className="text-sm text-muted-foreground">{item.desc}</div>
                </div>
                <button
                  onClick={() => setNotifications(prev => ({ ...prev, [item.key]: !prev[item.key as keyof typeof prev] }))}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    notifications[item.key as keyof typeof notifications] ? 'bg-primary' : 'bg-muted'
                  }`}
                >
                  <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
                    notifications[item.key as keyof typeof notifications] ? 'left-7' : 'left-1'
                  }`} />
                </button>
              </div>
            ))}
          </div>
        );

      case 'privacy':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between p-4 rounded-xl border border-border/50">
              <div>
                <div className="font-medium text-foreground">Public Profile</div>
                <div className="text-sm text-muted-foreground">Show your analyses publicly</div>
              </div>
              <button
                onClick={() => setPrivacy(prev => ({ ...prev, publicProfile: !prev.publicProfile }))}
                className={`relative w-12 h-6 rounded-full transition-colors ${
                  privacy.publicProfile ? 'bg-primary' : 'bg-muted'
                }`}
              >
                <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
                  privacy.publicProfile ? 'left-7' : 'left-1'
                }`} />
              </button>
            </div>

            <div className="flex items-center justify-between p-4 rounded-xl border border-border/50">
              <div>
                <div className="font-medium text-foreground">Anonymous Mode</div>
                <div className="text-sm text-muted-foreground">Don't save analysis history</div>
              </div>
              <button
                onClick={() => setPrivacy(prev => ({ ...prev, anonymousMode: !prev.anonymousMode }))}
                className={`relative w-12 h-6 rounded-full transition-colors ${
                  privacy.anonymousMode ? 'bg-primary' : 'bg-muted'
                }`}
              >
                <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
                  privacy.anonymousMode ? 'left-7' : 'left-1'
                }`} />
              </button>
            </div>

            <div className="p-4 rounded-xl border border-border/50">
              <div className="font-medium text-foreground mb-2">Data Retention</div>
              <select
                value={privacy.dataRetention}
                onChange={(e) => setPrivacy(prev => ({ ...prev, dataRetention: e.target.value }))}
                className="w-full px-4 py-3 rounded-xl bg-muted/50 border border-border/50 text-foreground text-sm focus:outline-none focus:border-primary/50"
              >
                <option value="30">30 days</option>
                <option value="90">90 days</option>
                <option value="365">1 year</option>
                <option value="forever">Forever</option>
              </select>
            </div>

            <div className="flex items-center gap-4">
              <button className="flex items-center gap-2 px-4 py-3 rounded-xl bg-muted text-foreground hover:bg-muted/80 transition-colors">
                <Download className="w-4 h-4" />
                Export My Data
              </button>
              <button className="flex items-center gap-2 px-4 py-3 rounded-xl bg-destructive/20 text-destructive hover:bg-destructive/30 transition-colors">
                <Trash2 className="w-4 h-4" />
                Delete All Data
              </button>
            </div>
          </div>
        );

      case 'advanced':
        return (
          <div className="space-y-6">
            <div className="p-4 rounded-xl border border-border/50">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <Key className="w-5 h-5 text-muted-foreground" />
                  <div>
                    <div className="font-medium text-foreground">API Key</div>
                    <div className="text-sm text-muted-foreground">For developer access</div>
                  </div>
                </div>
                <button className="px-4 py-2 rounded-lg bg-primary/20 text-primary text-sm hover:bg-primary/30 transition-colors">
                  Generate
                </button>
              </div>
            </div>

            <div className="p-4 rounded-xl border border-border/50">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <Webhook className="w-5 h-5 text-muted-foreground" />
                  <div>
                    <div className="font-medium text-foreground">Webhooks</div>
                    <div className="text-sm text-muted-foreground">Configure event webhooks</div>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-muted-foreground" />
              </div>
            </div>

            <div className="p-4 rounded-xl border border-border/50">
              <div className="flex items-center gap-3 mb-4">
                <Sliders className="w-5 h-5 text-muted-foreground" />
                <div>
                  <div className="font-medium text-foreground">ML Model Sensitivity</div>
                  <div className="text-sm text-muted-foreground">Adjust detection threshold</div>
                </div>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={advanced.sensitivity}
                onChange={(e) => setAdvanced(prev => ({ ...prev, sensitivity: parseInt(e.target.value) }))}
                className="w-full h-2 rounded-full bg-muted appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs text-muted-foreground mt-2">
                <span>Less Sensitive</span>
                <span>{advanced.sensitivity}%</span>
                <span>More Sensitive</span>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 rounded-xl border border-border/50">
              <div className="flex items-center gap-3">
                <Bug className="w-5 h-5 text-muted-foreground" />
                <div>
                  <div className="font-medium text-foreground">Debug Mode</div>
                  <div className="text-sm text-muted-foreground">Show technical details</div>
                </div>
              </div>
              <button
                onClick={() => setAdvanced(prev => ({ ...prev, debugMode: !prev.debugMode }))}
                className={`relative w-12 h-6 rounded-full transition-colors ${
                  advanced.debugMode ? 'bg-primary' : 'bg-muted'
                }`}
              >
                <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-transform ${
                  advanced.debugMode ? 'left-7' : 'left-1'
                }`} />
              </button>
            </div>
          </div>
        );

      default:
        return (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Settings section coming soon...</p>
          </div>
        );
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen p-6"
    >
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-foreground mb-8">Settings</h1>

        <div className="flex gap-6">
          {/* Sidebar */}
          <div className="w-56 flex-shrink-0">
            <nav className="space-y-1">
              {sections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                    activeSection === section.id
                      ? 'bg-primary/10 text-primary'
                      : 'text-muted-foreground hover:bg-muted/50 hover:text-foreground'
                  }`}
                >
                  <section.icon className="w-5 h-5" />
                  <span>{section.label}</span>
                </button>
              ))}
            </nav>
          </div>

          {/* Content */}
          <div className="flex-1 glass rounded-2xl p-6">
            <h2 className="text-lg font-semibold text-foreground mb-6 capitalize">
              {sections.find(s => s.id === activeSection)?.label}
            </h2>
            {renderSection()}
          </div>
        </div>
      </div>
    </motion.div>
  );
};
