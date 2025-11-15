import { Star, Activity, Clock, TrendingUp } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import type { Agent } from "@shared/schema";

interface AgentDetailDialogProps {
  agent: Agent;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AgentDetailDialog({ agent, open, onOpenChange }: AgentDetailDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto" data-testid="dialog-agent-detail">
        <DialogHeader className="pb-6 border-b">
          <div className="flex items-start gap-4">
            <Avatar className="h-24 w-24">
              <AvatarFallback className="bg-primary text-primary-foreground text-2xl">
                {agent.name.slice(0, 2).toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 min-w-0">
              <DialogTitle className="text-2xl mb-2" data-testid="text-agent-detail-name">
                {agent.name}
              </DialogTitle>
              <p className="text-sm text-muted-foreground mb-4">
                {agent.description}
              </p>
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2">
                  <Star className="h-4 w-4 fill-chart-4 text-chart-4" />
                  <span className="font-medium">{agent.rating.toFixed(1)}/5.0</span>
                </div>
                <div className="flex items-center gap-2">
                  <Activity className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{agent.jobsCompleted} jobs</span>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{agent.avgResponseTime}ms avg</span>
                </div>
              </div>
            </div>
            <Button data-testid="button-invoke-agent">Invoke Agent</Button>
          </div>
        </DialogHeader>

        <Tabs defaultValue="capabilities" className="mt-6">
          <TabsList className="w-full justify-start">
            <TabsTrigger value="capabilities" data-testid="tab-capabilities">Capabilities</TabsTrigger>
            <TabsTrigger value="pricing" data-testid="tab-pricing">Pricing</TabsTrigger>
            <TabsTrigger value="performance" data-testid="tab-performance">Performance</TabsTrigger>
          </TabsList>

          <TabsContent value="capabilities" className="space-y-6 pt-6">
            <div>
              <h3 className="text-base font-semibold mb-3">Core Skills</h3>
              <div className="flex flex-wrap gap-2">
                {agent.skills.map((skill) => (
                  <Badge key={skill} variant="secondary">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-base font-semibold mb-3">Capabilities</h3>
              <ul className="space-y-2">
                {agent.capabilities.map((capability, idx) => (
                  <li key={idx} className="text-sm flex items-start gap-2">
                    <span className="text-primary mt-1">•</span>
                    <span>{capability}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-base font-semibold mb-3">Availability</h3>
              <div className="flex items-center gap-2">
                <Badge variant={agent.availability ? "default" : "secondary"} className={agent.availability ? "bg-status-online" : ""}>
                  {agent.availability ? "Available Now" : "Currently Offline"}
                </Badge>
                <span className="text-sm text-muted-foreground">
                  Current load: {agent.load}/10
                </span>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="pricing" className="space-y-6 pt-6">
            <div className="grid grid-cols-2 gap-6">
              <div className="p-4 border rounded-md">
                <div className="text-xs uppercase tracking-wide font-medium text-muted-foreground mb-2">
                  Base Rate
                </div>
                <div className="text-2xl font-mono font-semibold">
                  ${agent.basePrice.toFixed(2)}
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  Standard pricing per execution
                </p>
              </div>
              <div className="p-4 border rounded-md">
                <div className="text-xs uppercase tracking-wide font-medium text-muted-foreground mb-2">
                  Current Rate
                </div>
                <div className="text-2xl font-mono font-semibold flex items-center gap-2">
                  ${agent.dynamicPrice.toFixed(2)}
                  {agent.dynamicPrice > agent.basePrice && (
                    <TrendingUp className="h-4 w-4 text-destructive" />
                  )}
                </div>
                <p className="text-xs text-muted-foreground mt-2">
                  Adjusted based on load
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-base font-semibold mb-3">Load-Based Pricing</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Dynamic pricing adjusts automatically based on current demand. Higher load results in higher prices to manage capacity.
              </p>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Low Load (0-3)</span>
                  <span className="font-mono">Base rate</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Medium Load (4-7)</span>
                  <span className="font-mono">+15% surcharge</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">High Load (8-10)</span>
                  <span className="font-mono">+30% surcharge</span>
                </div>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="performance" className="space-y-6 pt-6">
            <div className="grid grid-cols-3 gap-4">
              <div className="p-4 bg-muted/30 rounded-md">
                <div className="text-xs uppercase tracking-wide font-medium text-muted-foreground mb-1">
                  Jobs Completed
                </div>
                <div className="text-2xl font-semibold">{agent.jobsCompleted}</div>
              </div>
              <div className="p-4 bg-muted/30 rounded-md">
                <div className="text-xs uppercase tracking-wide font-medium text-muted-foreground mb-1">
                  Avg Response
                </div>
                <div className="text-2xl font-semibold">{agent.avgResponseTime}ms</div>
              </div>
              <div className="p-4 bg-muted/30 rounded-md">
                <div className="text-xs uppercase tracking-wide font-medium text-muted-foreground mb-1">
                  Rating
                </div>
                <div className="text-2xl font-semibold flex items-center gap-1">
                  {agent.rating.toFixed(1)}
                  <Star className="h-4 w-4 fill-chart-4 text-chart-4" />
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-base font-semibold mb-3">Current Load</h3>
              <Progress value={agent.load * 10} className="h-3 mb-2" />
              <p className="text-sm text-muted-foreground">
                {agent.load} out of 10 concurrent tasks
              </p>
            </div>

            <div>
              <h3 className="text-base font-semibold mb-3">Historical Performance</h3>
              <p className="text-sm text-muted-foreground">
                This agent has maintained a {agent.rating.toFixed(1)}/5.0 rating across {agent.jobsCompleted} completed tasks,
                with an average response time of {agent.avgResponseTime}ms.
              </p>
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
