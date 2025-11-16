# Simple HubChat Orchestrator - Implementation Guide

## Overview

The HubChat orchestrator is now **non-conversational** - it processes single queries, orchestrates agent execution, and returns results. No conversation history is maintained.

## How It Works

```
User Query → Claude Agent SDK → Agent Invocations → Final Response
```

### Flow:

1. **User sends a query** (e.g., "Summarize and translate this text to French: AI is awesome")
2. **Claude Agent SDK processes** the query with access to `invoke_agent` tool
3. **Claude decides** which agents to call and orchestrates them
4. **Final response** is returned to the user

No conversation history. Each query is independent.

---

## Architecture

```
┌─────────────────┐
│   Frontend UI   │  (React - Port 5173)
│  hubchat.tsx    │
└────────┬────────┘
         │ POST /api/hubchat/message
         │ {content: "Translate to French"}
         ▼
┌─────────────────┐
│  FastAPI Router │  (Python - Port 8000)
│  hubchat.py     │
└────────┬────────┘
         │ 1. Get conversation history (for UI display only)
         │ 2. Store user message in DB
         │ 3. Call orchestrator.process_message(query)
         ▼
┌────────────────────────┐
│ Simple Orchestrator    │
│ (Claude Agent SDK)     │
└────────┬───────────────┘
         │ Processes single query
         │ Tool: invoke_agent
         ▼
┌────────────────────────┐
│  Agent Microservices   │
│  - Summarizer (8001)   │
│  - Translator (8002)   │
│  - Search (8003)       │
└────────────────────────┘
```

---

## Code Implementation

### Orchestrator (`server/hubchat/conversational_orchestrator.py`)

```python
class ConversationalOrchestrator:
    """Simple orchestrator using Claude Agent SDK - NO conversation history"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        # Create MCP server with invoke_agent tool
        self.tools_server = create_sdk_mcp_server(
            name="agent_tools",
            tools=[invoke_agent_tool]
        )
    
    async def process_message(
        self,
        user_message: str,
        conversation_history: List = None,  # IGNORED
        task_id: Optional[str] = None,
        max_budget: Optional[float] = None
    ):
        # Configure Claude Agent SDK
        options = ClaudeAgentOptions(
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            mcp_servers={"agents": self.tools_server},
            allowed_tools=["mcp__agents__invoke_agent"],
            permission_mode="bypassPermissions"
        )
        
        # Process the single query
        async with ClaudeSDKClient(options=options) as client:
            await client.query(user_message)
            
            # Collect response
            response_text = ""
            async for message in client.receive_response():
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            response_text += block.text
        
        return {
            "success": True,
            "response": response_text,
            "cost_breakdown": {...},
            "agents_used": [...]
        }
```

### Tool Definition (`@tool` decorator)

```python
@tool(
    name="invoke_agent",
    description="Execute agent service via FastAPI backend",
    input_schema={
        "agent_id": str,  # e.g., "summarizer"
        "subtask": str,   # What the agent should do
        "task_id": str,
        "required_skills": list
    }
)
async def invoke_agent_tool(args: dict):
    # Calls FastAPI backend: POST /api/invoke-agent
    # Returns agent execution result
```

---

## Frontend Integration

The UI still shows messages in conversation format, but the backend doesn't use that history for processing.

### Frontend (`ui/client/src/pages/hubchat.tsx`)

```typescript
// Sends message
const sendMessageMutation = useMutation({
  mutationFn: (content: string) =>
    apiRequest("POST", "/api/hubchat/message", { content }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["/api/messages"] });
  },
});

// Displays messages
const { data: messages } = useQuery<Message[]>({
  queryKey: ["/api/messages"],
});
```

**Key Point**: The UI fetches and displays message history for UX purposes, but the orchestrator ignores it.

---

## Environment Setup

### Required Secrets

```bash
# Replit Secrets
ANTHROPIC_API_KEY=sk-ant-...

# ui/.env
VITE_API_BASE_URL=http://localhost:8000
```

### Starting Services

```bash
# Option 1: Individual services
cd ui && npx vite                    # Frontend (port 5173)
cd server && python main.py           # Backend API (port 8000)
./start_all_services.sh              # Agent services (8001-8006)

# Option 2: All-in-one
./start_all.sh
```

---

## Testing

### Test 1: Simple Query
```bash
curl -X POST http://localhost:8000/api/hubchat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "What agents are available?"}'
```

Expected: Claude responds without invoking agents

### Test 2: Agent Invocation
```bash
curl -X POST http://localhost:8000/api/hubchat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Summarize this: AI is transforming technology across industries."}'
```

Expected: Claude invokes summarizer agent and returns summary

### Test 3: Multi-Agent Task
```bash
curl -X POST http://localhost:8000/api/hubchat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Summarize this text and then translate the summary to French: AI is transforming technology."}'
```

Expected: Claude invokes summarizer, then translator, returns final result

---

## Key Differences from Conversational Version

| Feature | Conversational | Simple (Current) |
|---------|---------------|------------------|
| **Context Retention** | ✅ Maintains history | ❌ Each query independent |
| **Multi-turn Dialogue** | ✅ "Remember what I said" | ❌ No memory |
| **Complexity** | High (Messages API, tool loop) | Low (Claude Agent SDK) |
| **Implementation** | 300+ lines | 100 lines |
| **Use Case** | Chatbot, assistant | Task executor |

---

## Why This Approach?

1. **Simpler**: Claude Agent SDK handles tool orchestration automatically
2. **Faster**: No need to replay conversation history
3. **Clear Intent**: Each query is a standalone task
4. **Better for Agents**: Focuses on "get task done" not "have conversation"

---

## Database Storage

Messages are still stored in PostgreSQL for:
- **Audit trail**: Track what users asked and what was executed
- **UI display**: Show message history in frontend
- **Cost tracking**: Record costs per query

But the orchestrator **doesn't read** this history when processing new queries.

---

## Cost Tracking

Costs are tracked per query:
- **External cost**: Claude API usage (input + output tokens)
- **Internal cost**: Agent invocation costs (tracked separately)
- **Total cost**: Sum of external + internal

Example response:
```json
{
  "success": true,
  "response": "Here's the summary in French: L'IA transforme la technologie.",
  "cost_breakdown": {
    "internal_cost": 0.0,
    "external_cost": 0.0045,
    "total_cost": 0.0045
  },
  "agents_used": [
    {"agent": "summarizer", "task_id": "task-123"},
    {"agent": "translator", "task_id": "task-123"}
  ]
}
```

---

## Next Steps

1. ✅ Start all services
2. ✅ Test simple queries
3. ✅ Test agent invocations
4. ⏳ Add more agents as needed
5. ⏳ Monitor costs and performance

---

## Troubleshooting

### "ANTHROPIC_API_KEY must be set"
- Add your API key to Replit Secrets

### "Failed to initialize orchestrator"
- Check that `claude_agent_sdk` package is installed
- Verify API key is valid

### "Agent invocation failed"
- Ensure agent services are running (ports 8001-8006)
- Check agent service logs

### Frontend can't connect
- Verify `VITE_API_BASE_URL=http://localhost:8000` in `ui/.env`
- Ensure backend is running on port 8000
