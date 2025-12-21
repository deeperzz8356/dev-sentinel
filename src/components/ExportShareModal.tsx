import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  X, Download, Share2, FileText, FileJson, FileSpreadsheet, 
  Image, Copy, Check, Link, QrCode, Twitter, Linkedin, Mail,
  Lock, Globe, Users, Sparkles
} from "lucide-react";

interface ExportShareModalProps {
  isOpen: boolean;
  onClose: () => void;
  mode: 'export' | 'share';
  username: string;
  score: number;
}

type ExportFormat = 'pdf' | 'json' | 'csv' | 'png';
type SharePrivacy = 'public' | 'password' | 'private';

const exportFormats = [
  { id: 'pdf' as ExportFormat, label: 'PDF Report', desc: 'Full detailed analysis', icon: FileText },
  { id: 'json' as ExportFormat, label: 'JSON', desc: 'Raw data for developers', icon: FileJson },
  { id: 'csv' as ExportFormat, label: 'CSV', desc: 'Metrics only', icon: FileSpreadsheet },
  { id: 'png' as ExportFormat, label: 'PNG', desc: 'Score card image', icon: Image },
];

const includeOptions = [
  { id: 'charts', label: 'Include all charts' },
  { id: 'flags', label: 'Include red flags' },
  { id: 'recommendations', label: 'Include recommendations' },
  { id: 'branding', label: 'Add company branding', isPro: true },
];

export const ExportShareModal = ({ isOpen, onClose, mode, username, score }: ExportShareModalProps) => {
  const [format, setFormat] = useState<ExportFormat>('pdf');
  const [includes, setIncludes] = useState<string[]>(['charts', 'flags', 'recommendations']);
  const [isGenerating, setIsGenerating] = useState(false);
  const [copied, setCopied] = useState(false);
  const [privacy, setPrivacy] = useState<SharePrivacy>('public');
  const [expiry, setExpiry] = useState('7');

  const shareLink = `https://devdebt.app/report/${username}/${Date.now()}`;

  const toggleInclude = (id: string) => {
    setIncludes(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setIsGenerating(false);
      // Trigger download
    }, 2000);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(shareLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getScoreColor = (s: number) => {
    if (s >= 70) return 'text-success';
    if (s >= 40) return 'text-warning';
    return 'text-destructive';
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.95, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="w-full max-w-lg glass rounded-2xl p-6 shadow-xl"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              {mode === 'export' ? (
                <Download className="w-6 h-6 text-primary" />
              ) : (
                <Share2 className="w-6 h-6 text-primary" />
              )}
              <h2 className="text-xl font-semibold text-foreground">
                {mode === 'export' ? 'Export Analysis Report' : 'Share Analysis'}
              </h2>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-muted/50 transition-colors"
            >
              <X className="w-5 h-5 text-muted-foreground" />
            </button>
          </div>

          {mode === 'export' ? (
            <>
              {/* Format options */}
              <div className="space-y-3 mb-6">
                <label className="text-sm font-medium text-foreground">Export Format</label>
                <div className="grid grid-cols-2 gap-3">
                  {exportFormats.map((f) => (
                    <button
                      key={f.id}
                      onClick={() => setFormat(f.id)}
                      className={`flex items-center gap-3 p-3 rounded-xl border transition-all ${
                        format === f.id
                          ? 'border-primary bg-primary/10'
                          : 'border-border/50 hover:border-primary/50'
                      }`}
                    >
                      <f.icon className={`w-5 h-5 ${format === f.id ? 'text-primary' : 'text-muted-foreground'}`} />
                      <div className="text-left">
                        <div className="text-sm font-medium text-foreground">{f.label}</div>
                        <div className="text-xs text-muted-foreground">{f.desc}</div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Include options */}
              <div className="space-y-3 mb-6">
                <label className="text-sm font-medium text-foreground">Customize Report</label>
                <div className="space-y-2">
                  {includeOptions.map((opt) => (
                    <label
                      key={opt.id}
                      className={`flex items-center gap-3 p-3 rounded-xl border border-border/50 cursor-pointer hover:border-primary/50 transition-all ${
                        opt.isPro ? 'opacity-50' : ''
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={includes.includes(opt.id)}
                        onChange={() => !opt.isPro && toggleInclude(opt.id)}
                        disabled={opt.isPro}
                        className="w-4 h-4 rounded border-border text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-foreground flex-1">{opt.label}</span>
                      {opt.isPro && (
                        <span className="px-2 py-0.5 rounded text-xs bg-primary/20 text-primary">Pro</span>
                      )}
                    </label>
                  ))}
                </div>
              </div>

              {/* Preview */}
              <div className="mb-6 p-4 rounded-xl bg-muted/30 border border-border/50">
                <div className="text-xs text-muted-foreground mb-2">Preview</div>
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-lg bg-gradient-to-br from-primary/20 to-pink-500/20 flex items-center justify-center">
                    <span className={`text-2xl font-bold ${getScoreColor(score)}`}>{score}</span>
                  </div>
                  <div>
                    <div className="font-medium text-foreground">@{username}</div>
                    <div className="text-sm text-muted-foreground">Authenticity Score Report</div>
                  </div>
                </div>
              </div>

              {/* Generate button */}
              <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-primary to-pink-500 text-primary-foreground font-semibold hover:opacity-90 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isGenerating ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    >
                      <Sparkles className="w-5 h-5" />
                    </motion.div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Download className="w-5 h-5" />
                    Generate Report
                  </>
                )}
              </button>
            </>
          ) : (
            <>
              {/* Share link */}
              <div className="space-y-3 mb-6">
                <label className="text-sm font-medium text-foreground">Share Link</label>
                <div className="flex items-center gap-2">
                  <div className="flex-1 px-4 py-3 rounded-xl bg-muted/50 border border-border/50 text-sm text-muted-foreground truncate">
                    {shareLink}
                  </div>
                  <button
                    onClick={handleCopy}
                    className={`p-3 rounded-xl transition-all ${
                      copied 
                        ? 'bg-success/20 text-success' 
                        : 'bg-primary/20 text-primary hover:bg-primary/30'
                    }`}
                  >
                    {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* QR Code placeholder */}
              <div className="mb-6 flex justify-center">
                <div className="w-32 h-32 rounded-xl bg-muted/50 border border-border/50 flex items-center justify-center">
                  <QrCode className="w-16 h-16 text-muted-foreground/50" />
                </div>
              </div>

              {/* Social sharing */}
              <div className="space-y-3 mb-6">
                <label className="text-sm font-medium text-foreground">Share on Social</label>
                <div className="flex items-center gap-3">
                  <button className="flex-1 flex items-center justify-center gap-2 p-3 rounded-xl bg-[#1DA1F2]/20 text-[#1DA1F2] hover:bg-[#1DA1F2]/30 transition-colors">
                    <Twitter className="w-5 h-5" />
                    Twitter
                  </button>
                  <button className="flex-1 flex items-center justify-center gap-2 p-3 rounded-xl bg-[#0A66C2]/20 text-[#0A66C2] hover:bg-[#0A66C2]/30 transition-colors">
                    <Linkedin className="w-5 h-5" />
                    LinkedIn
                  </button>
                  <button className="flex-1 flex items-center justify-center gap-2 p-3 rounded-xl bg-muted text-foreground hover:bg-muted/80 transition-colors">
                    <Mail className="w-5 h-5" />
                    Email
                  </button>
                </div>
              </div>

              {/* Privacy settings */}
              <div className="space-y-3 mb-6">
                <label className="text-sm font-medium text-foreground">Privacy</label>
                <div className="flex items-center gap-2">
                  {[
                    { id: 'public' as SharePrivacy, icon: Globe, label: 'Public' },
                    { id: 'password' as SharePrivacy, icon: Lock, label: 'Password' },
                    { id: 'private' as SharePrivacy, icon: Users, label: 'Invite Only' },
                  ].map((p) => (
                    <button
                      key={p.id}
                      onClick={() => setPrivacy(p.id)}
                      className={`flex-1 flex items-center justify-center gap-2 p-3 rounded-xl border transition-all ${
                        privacy === p.id
                          ? 'border-primary bg-primary/10 text-primary'
                          : 'border-border/50 text-muted-foreground hover:border-primary/50'
                      }`}
                    >
                      <p.icon className="w-4 h-4" />
                      <span className="text-sm">{p.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Expiry */}
              <div className="space-y-3 mb-6">
                <label className="text-sm font-medium text-foreground">Link expires in</label>
                <select
                  value={expiry}
                  onChange={(e) => setExpiry(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl bg-muted/50 border border-border/50 text-foreground text-sm focus:outline-none focus:border-primary/50"
                >
                  <option value="1">1 day</option>
                  <option value="7">7 days</option>
                  <option value="30">30 days</option>
                  <option value="never">Never</option>
                </select>
              </div>

              {/* Create link button */}
              <button
                className="w-full py-3 rounded-xl bg-gradient-to-r from-primary to-pink-500 text-primary-foreground font-semibold hover:opacity-90 transition-all flex items-center justify-center gap-2"
              >
                <Link className="w-5 h-5" />
                Create Shareable Link
              </button>
            </>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};
