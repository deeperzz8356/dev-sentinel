import { useState } from "react";
import { motion } from "framer-motion";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  PieChart, Pie, Cell, LineChart, Line, Area, AreaChart
} from "recharts";
import { 
  Activity, Clock, Code, GitBranch, Star, Users, 
  Calendar, TrendingUp, Shield, AlertTriangle 
} from "lucide-react";
import { ComprehensiveFeatures, RepositoryHealth, ActivityPatterns } from "@/services/api";

interface ComprehensiveAnalysisProps {
  features: ComprehensiveFeatures;
  repositoryHealth: RepositoryHealth;
  activityPatterns: ActivityPatterns;
  username: string;
}

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#00ff00', '#ff00ff'];

export const ComprehensiveAnalysis = ({ 
  features, 
  repositoryHealth, 
  activityPatterns, 
  username 
}: ComprehensiveAnalysisProps) => {
  const [activeTab, setActiveTab] = useState("overview");

  // Prepare data for different visualizations
  const coreMetricsData = [
    { name: 'Commit Frequency', value: Math.min(100, features.commit_frequency), color: '#8884d8' },
    { name: 'Activity Consistency', value: features.activity_consistency * 100, color: '#82ca9d' },
    { name: 'Original Repos', value: features.original_repo_ratio * 100, color: '#ffc658' },
    { name: 'Language Diversity', value: Math.min(100, features.language_diversity * 10), color: '#ff7300' },
    { name: 'Profile Completeness', value: features.profile_completeness * 100, color: '#00ff00' },
    { name: 'Code Quality', value: features.code_quality_score * 100, color: '#ff00ff' }
  ];

  const timePatternData = [
    { name: 'Weekend Commits', value: features.weekend_commit_ratio * 100, threshold: 40 },
    { name: 'Night Commits', value: features.night_commit_ratio * 100, threshold: 30 },
    { name: 'Timing Entropy', value: features.timing_entropy * 100, threshold: 50 },
    { name: 'Burst Activity', value: features.burst_activity_score * 100, threshold: 70 }
  ];

  const socialMetricsData = [
    { name: 'Follower/Repo Ratio', value: Math.min(100, features.follower_repo_ratio * 20), color: '#8884d8' },
    { name: 'Collaboration Score', value: features.collaboration_score * 100, color: '#82ca9d' },
    { name: 'Avg Stars/Repo', value: Math.min(100, features.avg_stars_per_repo * 10), color: '#ffc658' },
    { name: 'Issue Engagement', value: Math.min(100, features.issue_engagement * 5), color: '#ff7300' }
  ];

  const hourlyData = activityPatterns.hourly_distribution.map((count, hour) => ({
    hour: `${hour}:00`,
    commits: count,
    isNight: hour >= 22 || hour <= 6
  }));

  const dailyData = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, index) => ({
    day,
    commits: activityPatterns.daily_distribution[index],
    isWeekend: index >= 5
  }));

  const languageData = Object.entries(activityPatterns.language_distribution)
    .map(([name, count]) => ({ name, value: count }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 8);

  const contributionData = Object.entries(activityPatterns.contribution_types)
    .map(([name, count]) => ({ name: name.charAt(0).toUpperCase() + name.slice(1), value: count }));

  const radarData = [
    { subject: 'Activity', A: features.activity_consistency * 100, fullMark: 100 },
    { subject: 'Quality', A: features.code_quality_score * 100, fullMark: 100 },
    { subject: 'Social', A: Math.min(100, features.collaboration_score * 100), fullMark: 100 },
    { subject: 'Diversity', A: Math.min(100, features.language_diversity * 10), fullMark: 100 },
    { subject: 'Maintenance', A: features.maintenance_score * 100, fullMark: 100 },
    { subject: 'Originality', A: features.original_repo_ratio * 100, fullMark: 100 }
  ];

  return (
    <div className="w-full space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">
          Comprehensive Analysis for @{username}
        </h2>
        <Badge variant="outline" className="text-primary">
          23 Features Analyzed
        </Badge>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="activity">Activity Patterns</TabsTrigger>
          <TabsTrigger value="repositories">Repository Health</TabsTrigger>
          <TabsTrigger value="social">Social Metrics</TabsTrigger>
          <TabsTrigger value="advanced">Advanced Analysis</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Core Metrics Radar Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  Authenticity Profile
                </CardTitle>
                <CardDescription>
                  Overall profile assessment across key dimensions
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} />
                    <Radar
                      name="Score"
                      dataKey="A"
                      stroke="#8884d8"
                      fill="#8884d8"
                      fillOpacity={0.3}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Core Metrics Bar Chart */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  Core Metrics
                </CardTitle>
                <CardDescription>
                  Key authenticity indicators (0-100 scale)
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={coreMetricsData} layout="horizontal">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" domain={[0, 100]} />
                    <YAxis dataKey="name" type="category" width={120} />
                    <Tooltip />
                    <Bar dataKey="value" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Feature Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(features).map(([key, value]) => {
              const displayValue = typeof value === 'number' ? 
                (value < 1 ? `${(value * 100).toFixed(1)}%` : value.toFixed(1)) : 
                String(value);
              
              const isGood = key.includes('quality') || key.includes('consistency') || 
                           key.includes('completeness') || key.includes('diversity');
              const isBad = key.includes('weekend') || key.includes('night') || 
                          key.includes('burst') || key.includes('variance');
              
              return (
                <Card key={key} className="p-4">
                  <div className="space-y-2">
                    <p className="text-sm text-muted-foreground">
                      {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </p>
                    <p className={`text-lg font-semibold ${
                      isGood ? 'text-success' : isBad ? 'text-destructive' : 'text-foreground'
                    }`}>
                      {displayValue}
                    </p>
                  </div>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        <TabsContent value="activity" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Hourly Activity */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="w-5 h-5" />
                  Hourly Activity Pattern
                </CardTitle>
                <CardDescription>
                  Commit distribution across 24 hours
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <AreaChart data={hourlyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hour" />
                    <YAxis />
                    <Tooltip />
                    <Area 
                      type="monotone" 
                      dataKey="commits" 
                      stroke="#8884d8" 
                      fill="#8884d8" 
                      fillOpacity={0.3}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Daily Activity */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5" />
                  Daily Activity Pattern
                </CardTitle>
                <CardDescription>
                  Commit distribution across weekdays
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={dailyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Bar 
                      dataKey="commits" 
                      fill={(entry: any) => entry.isWeekend ? '#ff7300' : '#8884d8'}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Time Pattern Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                Time Pattern Analysis
              </CardTitle>
              <CardDescription>
                Suspicious timing patterns (red flags when above threshold)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {timePatternData.map((item) => (
                  <div key={item.name} className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium">{item.name}</span>
                      <span className={`text-sm ${
                        item.value > item.threshold ? 'text-destructive' : 'text-success'
                      }`}>
                        {item.value.toFixed(1)}%
                      </span>
                    </div>
                    <Progress 
                      value={item.value} 
                      className={`h-2 ${
                        item.value > item.threshold ? 'bg-destructive/20' : 'bg-success/20'
                      }`}
                    />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="repositories" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <GitBranch className="w-5 h-5" />
                  Repository Overview
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between">
                  <span>Total Repositories</span>
                  <span className="font-semibold">{repositoryHealth.total_repositories}</span>
                </div>
                <div className="flex justify-between">
                  <span>Active Repositories</span>
                  <span className="font-semibold text-success">{repositoryHealth.active_repositories}</span>
                </div>
                <div className="flex justify-between">
                  <span>Original Repositories</span>
                  <span className="font-semibold text-primary">{repositoryHealth.original_repositories}</span>
                </div>
                <div className="flex justify-between">
                  <span>Forked Repositories</span>
                  <span className="font-semibold text-muted-foreground">{repositoryHealth.forked_repositories}</span>
                </div>
              </CardContent>
            </Card>

            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Code className="w-5 h-5" />
                  Language Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie
                      data={languageData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {languageData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Top Repositories */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Star className="w-5 h-5" />
                Top Repositories
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {repositoryHealth.top_repositories.slice(0, 5).map((repo, index) => (
                  <div key={repo.name} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                    <div>
                      <p className="font-medium">{repo.name}</p>
                      <p className="text-sm text-muted-foreground">{repo.language || 'No language'}</p>
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="flex items-center gap-1">
                        <Star className="w-4 h-4" />
                        {repo.stars}
                      </span>
                      <span className="flex items-center gap-1">
                        <GitBranch className="w-4 h-4" />
                        {repo.forks}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="social" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  Social Engagement Metrics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={socialMetricsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#82ca9d" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="w-5 h-5" />
                  Contribution Types
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={contributionData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {contributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="advanced" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Advanced metrics cards */}
            {[
              { key: 'commit_msg_quality', label: 'Commit Message Quality', icon: Code },
              { key: 'repo_naming_quality', label: 'Repository Naming', icon: GitBranch },
              { key: 'contribution_diversity', label: 'Contribution Diversity', icon: Activity },
              { key: 'maintenance_score', label: 'Maintenance Score', icon: TrendingUp },
              { key: 'account_maturity', label: 'Account Maturity', icon: Calendar },
              { key: 'timing_entropy', label: 'Timing Entropy', icon: Clock }
            ].map(({ key, label, icon: Icon }) => {
              const value = features[key as keyof ComprehensiveFeatures] as number;
              const percentage = Math.round(value * 100);
              
              return (
                <Card key={key}>
                  <CardHeader className="pb-2">
                    <CardTitle className="flex items-center gap-2 text-sm">
                      <Icon className="w-4 h-4" />
                      {label}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-2xl font-bold">{percentage}%</span>
                        <Badge variant={percentage > 70 ? "default" : percentage > 40 ? "secondary" : "destructive"}>
                          {percentage > 70 ? "Good" : percentage > 40 ? "Fair" : "Poor"}
                        </Badge>
                      </div>
                      <Progress value={percentage} className="h-2" />
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};