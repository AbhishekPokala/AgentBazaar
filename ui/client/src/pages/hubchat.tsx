import { useState, useRef, useEffect } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { Send, Bot, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { apiRequest, queryClient } from "@/lib/queryClient";
import type { Message } from "@shared/schema";

export default function HubChat() {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data: messages, isLoading, isError, refetch } = useQuery<Message[]>({
    queryKey: ["/api/messages"],
  });

  const sendMessageMutation = useMutation({
    mutationFn: (content: string) =>
      apiRequest("POST", "/api/hubchat/message", { content }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/messages"] });
      setInput("");
    },
  });

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || sendMessageMutation.isPending) return;
    sendMessageMutation.mutate(input);
  };

  return (
    <div className="h-full flex flex-col">
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {isError ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <Bot className="h-16 w-16 text-destructive mb-4" />
            <h3 className="text-lg font-medium mb-2">Failed to load messages</h3>
            <p className="text-sm text-muted-foreground mb-4 max-w-md">
              There was an error loading your chat history
            </p>
            <Button onClick={() => refetch()} data-testid="button-retry-messages">
              Retry
            </Button>
          </div>
        ) : isLoading ? (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="animate-pulse space-y-4 w-full max-w-lg">
              <div className="flex gap-3">
                <Skeleton className="h-8 w-8 rounded-full flex-shrink-0" />
                <Skeleton className="h-20 flex-1 rounded-2xl" />
              </div>
              <div className="flex gap-3 justify-end">
                <Skeleton className="h-16 flex-1 max-w-md rounded-2xl" />
                <Skeleton className="h-8 w-8 rounded-full flex-shrink-0" />
              </div>
            </div>
          </div>
        ) : messages?.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <Bot className="h-16 w-16 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">Welcome to HubChat</h3>
            <p className="text-sm text-muted-foreground max-w-md">
              I'm your AI orchestrator. Describe what you need, and I'll plan the task,
              select the right agents, and manage the execution for you.
            </p>
          </div>
        ) : (
          <>
            {messages?.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}
                data-testid={`message-${message.role}-${message.id}`}
              >
                {message.role === "assistant" && (
                  <Avatar className="h-8 w-8 flex-shrink-0">
                    <AvatarFallback className="bg-primary text-primary-foreground">
                      <Bot className="h-4 w-4" />
                    </AvatarFallback>
                  </Avatar>
                )}

                <div
                  className={`max-w-lg rounded-2xl px-4 py-3 ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground rounded-tr-sm"
                      : "bg-muted rounded-tl-sm"
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap" data-testid={`text-message-content-${message.id}`}>
                    {message.content}
                  </p>

                  {message.costBreakdown && typeof message.costBreakdown === 'object' && (
                    <Card className="mt-3 p-3 bg-background/50">
                      <div className="text-xs font-medium mb-2 uppercase tracking-wide">
                        Cost Breakdown
                      </div>
                      <div className="space-y-1">
                        {Array.isArray((message.costBreakdown as any).subtasks) && 
                          (message.costBreakdown as any).subtasks.map((subtask: any, idx: number) => (
                            <div key={idx} className="flex justify-between items-center text-sm">
                              <span className="text-muted-foreground">{subtask.agent}</span>
                              <span className="font-mono">${subtask.cost.toFixed(2)}</span>
                            </div>
                          ))}
                        <div className="flex justify-between items-center text-sm pt-2 mt-2 border-t font-semibold">
                          <span>Total</span>
                          <span className="font-mono">${(message.costBreakdown as any).total?.toFixed(2)}</span>
                        </div>
                      </div>
                    </Card>
                  )}
                </div>

                {message.role === "user" && (
                  <Avatar className="h-8 w-8 flex-shrink-0">
                    <AvatarFallback className="bg-secondary">
                      <User className="h-4 w-4" />
                    </AvatarFallback>
                  </Avatar>
                )}
              </div>
            ))}

            {sendMessageMutation.isPending && (
              <div className="flex gap-3 justify-start">
                <Avatar className="h-8 w-8 flex-shrink-0">
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    <Bot className="h-4 w-4" />
                  </AvatarFallback>
                </Avatar>
                <div className="max-w-lg rounded-2xl rounded-tl-sm bg-muted px-4 py-3">
                  <div className="flex gap-1">
                    <div className="h-2 w-2 bg-foreground/40 rounded-full animate-pulse" />
                    <div className="h-2 w-2 bg-foreground/40 rounded-full animate-pulse delay-100" />
                    <div className="h-2 w-2 bg-foreground/40 rounded-full animate-pulse delay-200" />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <div className="border-t p-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
          <Textarea
            placeholder="Describe your task (e.g., 'Summarize and translate this text to French')..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            className="min-h-12 pr-12 resize-none"
            data-testid="input-chat-message"
          />
          <Button
            type="submit"
            size="icon"
            className="absolute right-2 bottom-2"
            disabled={!input.trim() || sendMessageMutation.isPending}
            data-testid="button-send-message"
          >
            <Send className="h-4 w-4" />
          </Button>
          <div className="absolute left-3 bottom-2 text-xs text-muted-foreground">
            {input.length} characters
          </div>
        </form>
      </div>
    </div>
  );
}
