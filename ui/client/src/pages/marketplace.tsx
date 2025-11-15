import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search, Star, TrendingUp, Activity, Bot } from "lucide-react";
import { Card, CardContent, CardHeader, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Skeleton } from "@/components/ui/skeleton";
import { AgentDetailDialog } from "@/components/agent-detail-dialog";
import type { Agent } from "@shared/schema";

export default function Marketplace() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  const { data: agents, isLoading, isError, refetch } = useQuery<Agent[]>({
    queryKey: ["/api/agents"],
  });

  const filteredAgents = agents?.filter((agent) =>
    agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    agent.skills.some((skill) => skill.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="h-full overflow-auto">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-semibold mb-2" data-testid="text-page-title">
            Agent Marketplace
          </h1>
          <p className="text-sm text-muted-foreground">
            Browse and select from our collection of specialized AI agents
          </p>
        </div>

        <div className="mb-6 relative max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search agents by name or skill..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
            data-testid="input-search-agents"
          />
        </div>

        {isError ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Bot className="h-12 w-12 text-destructive mb-4" />
              <h3 className="text-lg font-medium mb-2">Failed to load agents</h3>
              <p className="text-sm text-muted-foreground mb-4">
                There was an error loading the agent marketplace
              </p>
              <Button onClick={() => refetch()} data-testid="button-retry-agents">
                Retry
              </Button>
            </CardContent>
          </Card>
        ) : isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Card key={i}>
                <CardHeader className="gap-4">
                  <div className="flex items-center gap-3">
                    <Skeleton className="h-12 w-12 rounded-full" />
                    <div className="flex-1">
                      <Skeleton className="h-5 w-32 mb-2" />
                      <Skeleton className="h-4 w-24" />
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Skeleton className="h-16 w-full" />
                  <Skeleton className="h-8 w-full" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAgents?.map((agent) => (
              <Card key={agent.id} className="hover-elevate active-elevate-2 transition-all" data-testid={`card-agent-${agent.id}`}>
                <CardHeader className="gap-4">
                  <div className="flex items-center gap-3">
                    <Avatar className="h-12 w-12">
                      <AvatarFallback className="bg-primary text-primary-foreground">
                        {agent.name.slice(0, 2).toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-semibold truncate" data-testid={`text-agent-name-${agent.id}`}>
                        {agent.name}
                      </h3>
                      <div className="flex items-center gap-1 text-sm text-muted-foreground">
                        <Star className="h-3 w-3 fill-chart-4 text-chart-4" />
                        <span data-testid={`text-agent-rating-${agent.id}`}>{agent.rating.toFixed(1)}</span>
                      </div>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    {agent.skills.map((skill) => (
                      <Badge key={skill} variant="secondary" className="text-xs" data-testid={`badge-skill-${skill}`}>
                        {skill}
                      </Badge>
                    ))}
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-xs uppercase tracking-wide font-medium text-muted-foreground mb-1">
                        Base Price
                      </div>
                      <div className="font-mono font-medium" data-testid={`text-base-price-${agent.id}`}>
                        ${agent.basePrice.toFixed(2)}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs uppercase tracking-wide font-medium text-muted-foreground mb-1">
                        Dynamic Price
                      </div>
                      <div className="font-mono font-medium flex items-center gap-1">
                        <span data-testid={`text-dynamic-price-${agent.id}`}>${agent.dynamicPrice.toFixed(2)}</span>
                        {agent.dynamicPrice > agent.basePrice && (
                          <TrendingUp className="h-3 w-3 text-destructive" />
                        )}
                      </div>
                    </div>
                  </div>

                  <div>
                    <div className="flex items-center justify-between text-xs mb-2">
                      <span className="text-muted-foreground uppercase tracking-wide font-medium">
                        Current Load
                      </span>
                      <span className="font-medium" data-testid={`text-load-${agent.id}`}>{agent.load}/10</span>
                    </div>
                    <Progress value={agent.load * 10} className="h-2" />
                  </div>

                  <div className="flex items-center justify-between text-sm pt-2 border-t">
                    <div className="flex items-center gap-1 text-muted-foreground">
                      <Activity className="h-3 w-3" />
                      <span className="text-xs">{agent.jobsCompleted} jobs</span>
                    </div>
                    <Badge variant="outline" className={agent.availability ? "text-status-online" : "text-status-offline"}>
                      {agent.availability ? "Available" : "Offline"}
                    </Badge>
                  </div>
                </CardContent>

                <CardFooter>
                  <Button
                    className="w-full"
                    onClick={() => setSelectedAgent(agent)}
                    data-testid={`button-view-details-${agent.id}`}
                  >
                    View Details
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}

        {!isLoading && filteredAgents?.length === 0 && (
          <div className="text-center py-12">
            <Bot className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No agents found</h3>
            <p className="text-sm text-muted-foreground">
              Try adjusting your search query
            </p>
          </div>
        )}
      </div>

      {selectedAgent && (
        <AgentDetailDialog
          agent={selectedAgent}
          open={!!selectedAgent}
          onOpenChange={(open: boolean) => !open && setSelectedAgent(null)}
        />
      )}
    </div>
  );
}
