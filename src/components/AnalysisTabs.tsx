import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CommitPatternsTab } from "./tabs/CommitPatternsTab";
import { CodeQualityTab } from "./tabs/CodeQualityTab";
import { RepositoryHealthTab } from "./tabs/RepositoryHealthTab";
import { ActivityTimelineTab } from "./tabs/ActivityTimelineTab";

export const AnalysisTabs = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="glass rounded-2xl p-6"
    >
      <Tabs defaultValue="commits" className="w-full">
        <TabsList className="w-full bg-secondary/50 p-1 rounded-xl mb-6 grid grid-cols-4">
          <TabsTrigger 
            value="commits"
            className="rounded-lg data-[state=active]:bg-primary data-[state=active]:text-primary-foreground transition-all"
          >
            Commit Patterns
          </TabsTrigger>
          <TabsTrigger 
            value="quality"
            className="rounded-lg data-[state=active]:bg-primary data-[state=active]:text-primary-foreground transition-all"
          >
            Code Quality
          </TabsTrigger>
          <TabsTrigger 
            value="repos"
            className="rounded-lg data-[state=active]:bg-primary data-[state=active]:text-primary-foreground transition-all"
          >
            Repository Health
          </TabsTrigger>
          <TabsTrigger 
            value="timeline"
            className="rounded-lg data-[state=active]:bg-primary data-[state=active]:text-primary-foreground transition-all"
          >
            Activity Timeline
          </TabsTrigger>
        </TabsList>

        <AnimatePresence mode="wait">
          <TabsContent value="commits" className="mt-0">
            <CommitPatternsTab />
          </TabsContent>

          <TabsContent value="quality" className="mt-0">
            <CodeQualityTab />
          </TabsContent>

          <TabsContent value="repos" className="mt-0">
            <RepositoryHealthTab />
          </TabsContent>

          <TabsContent value="timeline" className="mt-0">
            <ActivityTimelineTab />
          </TabsContent>
        </AnimatePresence>
      </Tabs>
    </motion.div>
  );
};
