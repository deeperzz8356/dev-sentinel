import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const DemoBanner = () => {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://dev-sentinel-api.onrender.com';
  
  // Only show banner if explicitly in mock mode
  if (API_BASE_URL === 'MOCK_MODE') {
    return (
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 text-center text-sm">
        🎭 <strong>Demo Mode:</strong> Using mock data for demonstration. Deploy backend for real ML analysis.
      </div>
    );
  }
  
  return null;
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <DemoBanner />
        <Routes>
          <Route path="/" element={<Index />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
