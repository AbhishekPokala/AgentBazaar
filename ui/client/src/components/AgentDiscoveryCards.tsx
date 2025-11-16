import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Star, CheckCircle2 } from "lucide-react";

interface Agent {
  skill: string;
  max_price?: number;
}

interface AgentDiscoveryCardsProps {
  agentsDiscovered: Agent[];
}

export function AgentDiscoveryCards({ agentsDiscovered }: AgentDiscoveryCardsProps) {
  if (!agentsDiscovered || agentsDiscovered.length === 0) {
    return null;
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold flex items-center gap-2">
        <Star className="h-4 w-4 text-primary" />
        Agents Discovered ({agentsDiscovered.length})
      </h3>
      <div className="grid gap-2">
        {agentsDiscovered.map((agent, idx) => (
          <Card key={idx} className="p-3" data-testid={`card-agent-discovered-${idx}`}>
            <div className="flex items-center justify-between gap-2">
              <div className="flex-1">
                <div className="text-sm font-medium capitalize" data-testid={`text-agent-skill-${idx}`}>
                  {agent.skill}
                </div>
                {agent.max_price && (
                  <div className="text-xs text-muted-foreground mt-0.5">
                    Max budget: ${agent.max_price.toFixed(2)}
                  </div>
                )}
              </div>
              <CheckCircle2 className="h-4 w-4 text-green-500" />
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
