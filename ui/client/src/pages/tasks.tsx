import { useQuery } from "@tanstack/react-query";
import { Clock, CheckCircle2, XCircle, Circle, DollarSign } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Skeleton } from "@/components/ui/skeleton";
import type { Task, TaskStep, Agent } from "@shared/schema";

export default function Tasks() {
  const { data: tasks, isLoading, isError, refetch } = useQuery<Task[]>({
    queryKey: ["/api/tasks"],
  });

  const { data: agents, isError: agentsError, refetch: refetchAgents } = useQuery<Agent[]>({
    queryKey: ["/api/agents"],
  });

  if (isError) {
    return (
      <div className="h-full overflow-auto">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-semibold mb-2">Task History</h1>
          </div>
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Circle className="h-12 w-12 text-destructive mb-4" />
              <h3 className="text-lg font-medium mb-2">Failed to load tasks</h3>
              <p className="text-sm text-muted-foreground mb-4">
                There was an error loading your task history
              </p>
              <Button onClick={() => refetch()} data-testid="button-retry-tasks">
                Retry
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="h-full overflow-auto">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <Skeleton className="h-10 w-64 mb-8" />
          <div className="space-y-6">
            {[...Array(3)].map((_, i) => (
              <Card key={i}>
                <CardContent className="p-6">
                  <Skeleton className="h-6 w-full mb-4" />
                  <Skeleton className="h-32 w-full" />
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-auto">
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-semibold mb-2" data-testid="text-page-title">
            Task History
          </h1>
          <p className="text-sm text-muted-foreground">
            View execution details and logs for all your tasks
          </p>
        </div>

        {agentsError && (
          <Card className="mb-6">
            <CardContent className="flex items-center justify-between py-4">
              <p className="text-sm text-destructive">Failed to load agent information</p>
              <Button onClick={() => refetchAgents()} variant="outline" size="sm" data-testid="button-retry-agents-tasks">
                Retry
              </Button>
            </CardContent>
          </Card>
        )}

        {tasks?.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Circle className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium mb-2">No tasks yet</h3>
              <p className="text-sm text-muted-foreground text-center max-w-md">
                Start a conversation in HubChat to create your first task
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {tasks?.map((task) => (
              <TaskTimeline key={task.id} task={task} agents={agents || []} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function TaskTimeline({ task, agents }: { task: Task; agents: Agent[] }) {
  const { data: steps, isError: stepsError, refetch: refetchSteps } = useQuery<TaskStep[]>({
    queryKey: ["/api/tasks", task.id, "steps"],
  });

  const getAgent = (agentId: string) => agents.find((a) => a.id === agentId);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="h-5 w-5 text-status-online" />;
      case "failed":
        return <XCircle className="h-5 w-5 text-destructive" />;
      case "in_progress":
        return <Circle className="h-5 w-5 text-status-away animate-pulse" />;
      default:
        return <Circle className="h-5 w-5 text-muted-foreground" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return <Badge className="bg-status-online">Completed</Badge>;
      case "failed":
        return <Badge variant="destructive">Failed</Badge>;
      case "in_progress":
        return <Badge className="bg-status-away">In Progress</Badge>;
      default:
        return <Badge variant="secondary">Pending</Badge>;
    }
  };

  return (
    <Card data-testid={`card-task-${task.id}`}>
      <CardContent className="p-6">
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold mb-2" data-testid={`text-task-query-${task.id}`}>
              {task.userQuery}
            </h3>
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {new Date(task.createdAt).toLocaleString()}
              </span>
              <span className="flex items-center gap-1">
                <DollarSign className="h-3 w-3" />
                ${task.totalCost.toFixed(2)}
              </span>
            </div>
          </div>
          {getStatusBadge(task.status)}
        </div>

        {stepsError ? (
          <div className="text-center py-8">
            <p className="text-sm text-destructive mb-3">Failed to load task execution steps</p>
            <Button onClick={() => refetchSteps()} variant="outline" size="sm" data-testid={`button-retry-steps-${task.id}`}>
              Retry
            </Button>
          </div>
        ) : (
          <div className="space-y-6">
            {steps?.map((step, idx) => {
            const agent = getAgent(step.agentId);
            return (
              <div key={step.id} className="flex gap-4" data-testid={`step-${step.id}`}>
                <div className="flex flex-col items-center">
                  <div className="h-8 w-8 rounded-full flex items-center justify-center bg-muted">
                    {getStatusIcon(step.status)}
                  </div>
                  {idx < (steps.length - 1) && (
                    <div className="flex-1 w-px bg-border mt-2 mb-2 min-h-16" />
                  )}
                </div>

                <div className="flex-1 pb-8">
                  <div className="flex items-center gap-3 mb-2">
                    {agent && (
                      <Avatar className="h-6 w-6">
                        <AvatarFallback className="text-xs bg-primary text-primary-foreground">
                          {agent.name.slice(0, 2).toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                    )}
                    <span className="font-medium" data-testid={`text-step-agent-${step.id}`}>
                      {agent?.name || step.agentId}
                    </span>
                    <Badge variant="outline" className="text-xs">
                      {step.subtaskType}
                    </Badge>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                    <div>
                      <span className="text-muted-foreground">Cost: </span>
                      <span className="font-mono" data-testid={`text-step-cost-${step.id}`}>
                        ${step.cost.toFixed(2)}
                      </span>
                    </div>
                    {step.executionTime && (
                      <div>
                        <span className="text-muted-foreground">Time: </span>
                        <span className="font-mono">{step.executionTime}ms</span>
                      </div>
                    )}
                    {step.requiresExternalTool && (
                      <div className="col-span-2">
                        <span className="text-muted-foreground">External Cost: </span>
                        <span className="font-mono">${step.externalCost.toFixed(2)}</span>
                      </div>
                    )}
                  </div>

                  {step.result && (
                    <div className="bg-muted/30 rounded-md p-3 text-sm">
                      <div className="text-xs uppercase tracking-wide font-medium text-muted-foreground mb-2">
                        Output
                      </div>
                      <p className="text-sm line-clamp-3" data-testid={`text-step-result-${step.id}`}>
                        {step.result}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
