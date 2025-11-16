import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, Zap, DollarSign, Search } from "lucide-react";

interface AgentUsed {
  agent: string;
  payload?: any;
}

interface PaymentMade {
  agent_id: string;
  amount: number;
  memo: string;
  recipient: string;
}

interface OrchestrationTimelineProps {
  agentsDiscovered?: any[];
  agentsUsed?: AgentUsed[];
  paymentsMade?: PaymentMade[];
  totalPaid?: number;
}

export function OrchestrationTimeline({
  agentsDiscovered = [],
  agentsUsed = [],
  paymentsMade = [],
  totalPaid = 0,
}: OrchestrationTimelineProps) {
  const hasData = agentsDiscovered.length > 0 || agentsUsed.length > 0 || paymentsMade.length > 0;

  if (!hasData) {
    return null;
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold">Orchestration Flow</h3>
      
      <div className="space-y-2">
        {agentsDiscovered.length > 0 && (
          <Card className="p-3" data-testid="card-discovery-step">
            <div className="flex items-start gap-3">
              <div className="mt-0.5">
                <Search className="h-4 w-4 text-blue-500" />
              </div>
              <div className="flex-1 space-y-1">
                <div className="text-sm font-medium">Discovery Phase</div>
                <div className="text-xs text-muted-foreground">
                  Found {agentsDiscovered.length} matching agent{agentsDiscovered.length > 1 ? 's' : ''}
                </div>
              </div>
              <CheckCircle2 className="h-4 w-4 text-green-500" />
            </div>
          </Card>
        )}

        {agentsUsed.length > 0 && (
          <Card className="p-3" data-testid="card-invocation-step">
            <div className="flex items-start gap-3">
              <div className="mt-0.5">
                <Zap className="h-4 w-4 text-amber-500" />
              </div>
              <div className="flex-1 space-y-2">
                <div className="text-sm font-medium">Invocation Phase</div>
                <div className="space-y-1">
                  {agentsUsed.map((agent, idx) => (
                    <div key={idx} className="flex items-center gap-2" data-testid={`text-agent-used-${idx}`}>
                      <div className="h-1.5 w-1.5 rounded-full bg-amber-500" />
                      <span className="text-xs capitalize">{agent.agent.replace(/_/g, ' ')}</span>
                    </div>
                  ))}
                </div>
              </div>
              <CheckCircle2 className="h-4 w-4 text-green-500" />
            </div>
          </Card>
        )}

        {paymentsMade.length > 0 && (
          <Card className="p-3" data-testid="card-payment-step">
            <div className="flex items-start gap-3">
              <div className="mt-0.5">
                <DollarSign className="h-4 w-4 text-green-500" />
              </div>
              <div className="flex-1 space-y-2">
                <div className="text-sm font-medium">Payment Phase</div>
                <div className="space-y-1">
                  {paymentsMade.map((payment, idx) => (
                    <div key={idx} className="flex items-center justify-between gap-2" data-testid={`row-payment-${idx}`}>
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
                        <span className="text-xs capitalize">{payment.agent_id.replace(/_/g, ' ')}</span>
                      </div>
                      <Badge variant="outline" className="text-xs font-mono">
                        ${payment.amount.toFixed(2)}
                      </Badge>
                    </div>
                  ))}
                </div>
                <div className="pt-1 border-t">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-medium">Total Paid:</span>
                    <span className="text-sm font-mono font-semibold" data-testid="text-total-paid">
                      ${totalPaid.toFixed(2)} USDC
                    </span>
                  </div>
                </div>
              </div>
              <CheckCircle2 className="h-4 w-4 text-green-500" />
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
