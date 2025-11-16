# HubChat Conversational Orchestrator - Complete Flow Explanation

## Overview

HubChat is an AI-powered conversational orchestrator that helps users accomplish tasks by:
- Understanding user requests through natural language
- Planning task execution strategies
- Invoking specialized agent microservices
- Maintaining conversation context across multiple turns
- Tracking costs for both AI usage and agent invocations

---

## Architecture

```
┌─────────────────┐
│   Frontend UI   │  (React - Port 5173)
│  hubchat.tsx    │
└────────┬────────┘
         │ HTTP POST /api/hubchat/message
         │ {content: "Translate this text to French"}
         ▼
┌─────────────────┐
│  FastAPI Router │  (Python - Port 8000)
│  hubchat.py     │
└────────┬────────┘
         │ 1. Fetch conversation history from DB
         │ 2. Call orchestrator.process_message()
         ▼
┌────────────────────────┐
│ ConversationalOrchest  │
│ conversational_        │
│ orchestrator.py        │
└────────┬───────────────┘
         │ Uses Claude SDK with full context
         │ Tools: invoke_agent
         ▼
┌────────────────────────┐
│   Claude AI (Anthropic)│
│   Sonnet 3.5           │
└────────┬───────────────┘
         │ Can call invoke_agent tool
         ▼
┌────────────────────────┐
│  Agent Microservices   │  (Ports 8001-8006)
│  - Summarizer          │
│  - Translator          │
│  - Search              │
└────────────────────────┘
```

---

## Detailed Flow

### Step 1: User Sends Message (Frontend)

**File**: `ui/client/src/pages/hubchat.tsx`

```typescript
// User types: "Summarize and translate this to French: AI is awesome"
const sendMessageMutation = useMutation({
  mutationFn: (content: string) =>
    apiRequest("POST", "/api/hubchat/message", { content }),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["/api/messages"] });
  },
});
```

**What happens**:
- Frontend sends POST request to `http://localhost:8000/api/hubchat/message`
- Payload: `{content: "Summarize and translate this to French: AI is awesome"}`
- After success, refetches all messages to update the chat UI

---

### Step 2: Backend Receives Request (FastAPI Router)

**File**: `server/routers/hubchat.py`

```python
@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(request: ChatMessageRequest, session: AsyncSession):
    # 1. Get conversation history from database
    if request.task_id:
        history = await message_repo.get_by_task_id(request.task_id)
    else:
        history = await message_repo.get_all(limit=100)  # All messages
    
    # 2. Convert to conversation format
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]
    
    # 3. Store user message in database
    user_message = await message_repo.create(MessageCreate(
        role="user",
        content=request.content,
        task_id=request.task_id
    ))
    
    # 4. Process with orchestrator
    result = await orch.process_message(
        user_message=request.content,
        conversation_history=conversation_history,
        task_id=request.task_id,
        max_budget=request.max_budget
    )
    
    # 5. Store assistant response
    assistant_message = await message_repo.create(MessageCreate(
        role="assistant",
        content=result["response"],
        task_id=result.get("task_id"),
        cost_breakdown=result.get("cost_breakdown")
    ))
    
    return ChatMessageResponse(...)
```

**Key Points**:
- Conversation history is fetched from PostgreSQL database
- Both user and assistant messages are persisted for context retention
- Messages can be linked to specific tasks via `task_id`

---

### Step 3: Orchestrator Processes Message

**File**: `server/hubchat/conversational_orchestrator.py`

```python
async def process_message(
    self,
    user_message: str,
    conversation_history: List[Dict[str, str]],
    task_id: Optional[str] = None,
    max_budget: Optional[float] = None
) -> Dict[str, Any]:
    # Build conversation with full context
    messages = []
    for msg in conversation_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Add new user message
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    # Configure Claude with invoke_agent tool
    options = ClaudeAgentOptions(
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
        mcp_servers={"agents": self.tools_server},
        allowed_tools=["mcp__agents__invoke_agent"]
    )
    
    # Send to Claude with full context
    async with ClaudeSDKClient(options=options) as client:
        # 🔴 ISSUE: Only sends user messages, not assistant responses!
        for msg in messages:
            if msg["role"] == "user":
                await client.query(msg["content"])
        
        # Collect response
        async for message in client.receive_response():
            # Extract text and track tool usage
            ...
```

---

## 🔴 Current Issues

### Issue #1: Conversation Context Not Replayed (CRITICAL)

**Problem**: Lines 229-231 only send user messages to Claude:
```python
for msg in messages:
    if msg["role"] == "user":  # ❌ Skips assistant messages!
        await client.query(msg["content"])
```

**Impact**: 
- Claude loses all context from previous assistant responses
- Multi-turn conversations fail
- Claude can't remember what it previously said or decided

**Fix**: Send the entire conversation using Claude's messages API format

---

### Issue #2: Cost Tracking Always Returns Zero

**Problem**: `total_cost` is never updated:
```python
total_cost = 0.0  # Set to 0
# ... process with Claude ...
return {
    "cost_breakdown": {
        "internal_cost": total_cost,  # ❌ Always 0!
        "external_cost": 0.0,
        "total_cost": total_cost
    }
}
```

**Impact**:
- Users can't see actual AI costs
- No visibility into Claude API usage
- Agent invocation costs not tracked

**Fix**: Capture usage from Claude SDK response and calculate costs

---

### Issue #3: Task/Budget Context Appended as Plain Text

**Problem**: Lines 203-208 append metadata to message content:
```python
if max_budget:
    messages[-1]["content"] += f"\n\n(Max budget: ${max_budget:.2f})"
if task_id:
    messages[-1]["content"] += f"\n\n(Task ID: {task_id})"
```

**Impact**:
- Pollutes conversation history with metadata
- Less clean separation of concerns
- Harder to parse/filter messages

**Fix**: Use Claude's metadata fields or system prompts for context

---

## Environment Variables Required

### Frontend (ui/.env)
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### Backend (Replit Secrets)
```bash
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://...  # Auto-provided by Replit
```

---

## Starting the System

### Option 1: Individual Services
```bash
# Terminal 1: Frontend
cd ui && npx vite

# Terminal 2: Backend API
cd server && python main.py

# Terminal 3: Agent Services
./start_all_services.sh
```

### Option 2: All-in-One Script
```bash
./start_all.sh
```

---

## Testing the Flow

### 1. Simple Question
```bash
curl -X POST http://localhost:8000/api/hubchat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "What agents are available?"}'
```

Expected: Claude responds without invoking agents

### 2. Agent Invocation
```bash
curl -X POST http://localhost:8000/api/hubchat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Summarize this: AI is transforming technology"}'
```

Expected: Claude invokes the summarizer agent

### 3. Multi-Turn Conversation
```bash
# First message
curl -X POST http://localhost:8000/api/hubchat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Translate AI is awesome to French"}'

# Follow-up (should remember previous context)
curl -X POST http://localhost:8000/api/hubchat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Now translate it to Spanish"}'
```

Expected: Claude remembers the previous text and translates it

---

## Next Steps to Fix

1. **Fix conversation replay** - Send full message history to Claude
2. **Implement cost tracking** - Capture Claude SDK usage metrics
3. **Clean up metadata handling** - Use proper Claude API fields
4. **Add error handling** - Better failure messages and recovery
5. **Test multi-turn conversations** - Verify context retention works

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `ui/client/src/pages/hubchat.tsx` | Frontend chat UI |
| `server/routers/hubchat.py` | API endpoints for chat |
| `server/hubchat/conversational_orchestrator.py` | Claude SDK integration |
| `server/hubchat/prompts.py` | System prompt for Claude |
| `server/models/message.py` | Pydantic models with camelCase |
| `server/db/repositories/message_repository.py` | Database operations |
