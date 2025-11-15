# Phase 4: HubChat Integration - Setup Guide

## Overview
The HubChat conversational orchestration system is now integrated between the FastAPI backend and React frontend. This guide explains how to run both services.

## Prerequisites

### Required Environment Variables
1. **ANTHROPIC_API_KEY** - Already configured in Replit Secrets ✓
2. **VITE_API_BASE_URL** - Already set in `ui/.env` to `http://localhost:8000` ✓

## Running the Application

### Option 1: Create a Second Workflow (Recommended)

1. Open the Workflows tool (Command + K → search "Workflows")
2. Create a new workflow named "Start FastAPI"
3. Add a task: "Execute Shell Command"
4. Command: `cd ui/server && python run_server.py`
5. Save the workflow

Then:
- Start the "Start FastAPI" workflow (runs backend on port 8000)
- Start the "Start application" workflow (runs frontend on port 5000)

Both servers will run simultaneously.

### Option 2: Manual Background Process

```bash
# Terminal 1: Start FastAPI backend
cd ui/server
python run_server.py

# Terminal 2: Start frontend (via workflow or manually)
cd ui
npm run dev
```

## Architecture

### Backend (FastAPI - Port 8000)
- **Main entry**: `ui/server/run_server.py`
- **Health check**: `http://localhost:8000/health`
- **API Base**: `http://localhost:8000/api`

**Key Endpoints**:
- `GET /api/messages` - Fetch chat message history
- `POST /api/hubchat/message` - Send a chat message to the orchestrator
  ```json
  {
    "content": "Your message here",
    "task_id": "optional-task-id",
    "max_budget": 100.0  // optional
  }
  ```
- `GET /api/hubchat/messages?task_id={id}` - Get messages for a specific task
- `DELETE /api/hubchat/messages/{task_id}` - Clear conversation for a task

### Frontend (React + Express - Port 5000)
- **URL**: `http://localhost:5000`
- **HubChat UI**: `/hubchat`
- **Environment**: Configured to call `http://localhost:8000/api` (via VITE_API_BASE_URL)

### Data Flow
```
User Input (Frontend)
  ↓
  POST /api/hubchat/message
  ↓
Message Repository (stores user message)
  ↓
ConversationalOrchestrator
  ├─ Loads conversation history
  ├─ Sends to Claude API (Anthropic)
  ├─ Processes response
  ├─ Can create tasks
  ├─ Can invoke agents
  └─ Returns response
  ↓
Message Repository (stores assistant response)
  ↓
Frontend displays messages
```

## Files Modified

### Backend
- `ui/server/main.py` - Added messages router
- `ui/server/routers/messages.py` - NEW: Provides `/api/messages` endpoint
- `ui/server/routers/hubchat.py` - HubChat endpoints
- `ui/server/run_server.py` - NEW: Server runner without auto-reload
- `ui/server/models/message.py` - **UPDATED**: Added camelCase serialization aliases (taskId, costBreakdown, createdAt)

### Frontend
- `ui/client/src/lib/queryClient.ts` - Added VITE_API_BASE_URL support
- `ui/client/src/pages/hubchat.tsx` - **UPDATED**: Displays cost breakdown with internal/external/total costs
- `ui/.env` - NEW: Environment configuration

## Testing the Integration

### 1. Verify Backend Health
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### 2. Test Message History
```bash
curl http://localhost:8000/api/messages
# Expected: [] (empty array initially)
```

### 3. Send a Chat Message
```bash
curl -X POST http://localhost:8000/api/hubchat/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello, can you help me analyze some sales data?"}'
```

Expected response:
```json
{
  "success": true,
  "user_message": {
    "id": "...",
    "role": "user",
    "content": "Hello, can you help me analyze some sales data?",
    ...
  },
  "assistant_message": {
    "id": "...",
    "role": "assistant",
    "content": "I'd be happy to help you analyze sales data! ...",
    ...
  },
  "cost_breakdown": {
    "internal_cost": 0.0,
    "external_cost": 0.015,
    "total_cost": 0.015
  }
}
```

### 4. Test Frontend
1. Open `http://localhost:5000/hubchat`
2. Type a message in the input field
3. Click "Send"
4. The orchestrator should respond with helpful assistance

## Troubleshooting

### Backend won't start
- Check that port 8000 is not already in use
- Verify ANTHROPIC_API_KEY is set in Replit Secrets
- Check logs for detailed error messages

### Frontend can't connect to backend
- Verify both servers are running
- Check that `ui/.env` contains `VITE_API_BASE_URL=http://localhost:8000`
- Restart the frontend workflow after changing .env

### "Failed to initialize orchestrator" error
- Verify ANTHROPIC_API_KEY is set correctly
- Check Replit Secrets configuration

## Next Steps
- Test conversational flow with multiple turns
- Verify context retention across messages
- Test task creation and agent invocation
- Monitor cost tracking accuracy
