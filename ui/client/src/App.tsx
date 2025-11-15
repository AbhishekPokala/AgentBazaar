import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { ThemeToggle } from "@/components/theme-toggle";
import { Coins } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import Marketplace from "@/pages/marketplace";
import HubChat from "@/pages/hubchat";
import Tasks from "@/pages/tasks";
import Payments from "@/pages/payments";
import Settings from "@/pages/settings";
import NotFound from "@/pages/not-found";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Marketplace} />
      <Route path="/hubchat" component={HubChat} />
      <Route path="/tasks" component={Tasks} />
      <Route path="/payments" component={Payments} />
      <Route path="/settings" component={Settings} />
      <Route component={NotFound} />
    </Switch>
  );
}

export default function App() {
  const style = {
    "--sidebar-width": "16rem",
    "--sidebar-width-icon": "4rem",
  };

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <SidebarProvider style={style as React.CSSProperties}>
          <div className="flex h-screen w-full">
            <AppSidebar />
            <div className="flex flex-col flex-1">
              <header className="flex items-center justify-between gap-4 p-4 border-b">
                <SidebarTrigger data-testid="button-sidebar-toggle" />
                <div className="flex items-center gap-4">
                  <Badge variant="outline" className="gap-2 px-3 py-1.5" data-testid="badge-balance">
                    <Coins className="h-4 w-4 text-chart-4" />
                    <span className="font-mono">100 BB</span>
                  </Badge>
                  <ThemeToggle />
                </div>
              </header>
              <main className="flex-1 overflow-hidden">
                <Router />
              </main>
            </div>
          </div>
        </SidebarProvider>
        <Toaster />
      </TooltipProvider>
    </QueryClientProvider>
  );
}
