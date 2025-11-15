# FastAPI Backend Implementation Plan

## 🎯 Executive Summary

**Goal**: Replace the Express mock backend (`ui/server/`) with a production-ready Python FastAPI backend that:
1. Implements all existing UI API contracts
2. Integrates with your existing agent services (summarizer, translator, search, etc.)
3. Connects to the HubChat orchestrator for multi-agent workflows
4. Adds PostgreSQL database persistence
5. Implements proper payment tracking (BazaarBucks + Stripe)

---

## 📊 Current Architecture Analysis

### Existing Infrastructure (Already Built)

```
AgentBazaar/
├── hubchat/                    ← ✅ Orchestrator with Claude SDK
│   ├── orchestrator.py        (HubChatOrchestrator class)
│   ├── planner.py
│   ├── prompts.py
│   └── tools.py
│
├── services/                   ← ✅ Individual agent microservices
│   ├── summarizer/            (Port 8001)
│   ├── translator/            (Port 8002)
│   ├── search/                (Port 8003)
│   ├── mock_busy/             (Port 8004)
│   ├── mock_highprice/        (Port 8005)
│   └── mock_negotiator/       (Port 8006)
│
├── ui/                         ← ✅ React SPA frontend
│   ├── client/                (React + TypeScript)
│   ├── server/                ⚠️ Mock Express backend (TO BE REPLACED)
│   └── shared/schema.ts       (TypeScript data models)
│
└── api/                        ← ⚠️ Empty (mentioned in README)
    └── README.md              (Planned endpoints documented)
```

### What's Missing (To Be Built)

```
server/                         ← 🆕 NEW FastAPI backend
├── main.py                    (FastAPI app entry point)
├── api/                       (API routes)
│   ├── agents.py
│   ├── tasks.py
│   ├── payments.py
│   └── hubchat.py
├── models/                    (Pydantic models)
│   ├── agent.py
│   ├── task.py
│   ├── payment.py
│   └── message.py
├── services/                  (Business logic)
│   ├── agent_service.py
│   ├── task_service.py
│   ├── payment_service.py
│   └── orchestrator_client.py
├── db/                        (Database layer)
│   ├── database.py
│   ├── repositories/
│   │   ├── agent_repo.py
│   │   ├── task_repo.py
│   │   └── payment_repo.py
│   └── migrations/
├── config.py                  (Settings)
├── dependencies.py            (FastAPI dependencies)
└── requirements.txt
```

---

## 🔗 API Contracts (From UI Mock Server)

### Current Endpoints That UI Expects

| Method | Endpoint | Purpose | UI Page |
|--------|----------|---------|---------|
| `GET` | `/api/agents` | List all agents | Marketplace, Tasks |
| `GET` | `/api/agents/:id` | Get agent details | Agent Dialog |
| `GET` | `/api/tasks` | List all tasks | Tasks |
| `GET` | `/api/tasks/:id` | Get task details | Task Detail |
| `GET` | `/api/tasks/:id/steps` | Get execution steps | Task Detail |
| `POST` | `/api/tasks` | Create new task | - |
| `POST` | `/api/invoke-agent` | Execute single agent | - |
| `GET` | `/api/messages` | Get chat history | HubChat |
| `POST` | `/api/hubchat/message` | Send chat message | HubChat |
| `GET` | `/api/payments/bazaarbucks` | Get internal payments | Payments |
| `GET` | `/api/payments/stripe` | Get external payments | Payments |

### Data Models (From `ui/shared/schema.ts`)

**Agent**:
```typescript
{
  id: string
  name: string
  description: string
  skills: string[]
  basePrice: number
  dynamicPrice: number
  load: number
  rating: number
  jobsCompleted: number
  endpointUrl: string
  capabilities: string[]
  avgResponseTime: number  // ms
  availability: boolean
}
```

**Task**:
```typescript
{
  id: string
  userQuery: string
  requiredSkills: string[]
  status: "created" | "in_progress" | "completed" | "failed"
  maxBudget: number
  totalCost: number
  createdAt: Date
  completedAt?: Date
}
```

**TaskStep**:
```typescript
{
  id: string
  taskId: string
  agentId: string
  subtaskType: string
  status: string
  cost: number
  externalCost: number
  requiresExternalTool: boolean
  result?: string
  executionTime?: number  // ms
  createdAt: Date
  completedAt?: Date
}
```

**BazaarBucksPayment**:
```typescript
{
  id: string
  taskId: string
  agentId: string
  amount: number
  type: "agent_payment" | "platform_fee" | "refund"
  createdAt: Date
}
```

**StripePayment**:
```typescript
{
  id: string
  agentId: string
  vendor: string
  amount: number
  status: "pending" | "completed" | "failed"
  type: "card_spend" | "balance_load"
  createdAt: Date
}
```

**Message** (HubChat):
```typescript
{
  id: string
  role: "user" | "assistant"
  content: string
  taskId?: string
  costBreakdown?: {
    subtasks: Array<{agent: string, cost: number}>
    total: number
  }
  createdAt: Date
}
```

---

## 🏗️ Implementation Plan (5 Phases)

### **Phase 1: Foundation & Database Setup** (Priority: HIGH)

#### Tasks:
1. **Create `server/` directory structure**
   ```bash
   server/
   ├── main.py
   ├── config.py
   ├── dependencies.py
   ├── requirements.txt
   └── .env.example
   ```

2. **Setup PostgreSQL database**
   - Use Replit's built-in Postgres (Neon-backed)
   - Create database schema matching TypeScript models
   - Setup Alembic for migrations

3. **Define Pydantic models**
   - Convert TypeScript schemas to Pydantic
   - Match exact field names and types for frontend compatibility
   - Add validation rules

4. **Create database repositories**
   - AgentRepository (CRUD for agents)
   - TaskRepository (CRUD for tasks + steps)
   - PaymentRepository (CRUD for payments)
   - MessageRepository (CRUD for chat messages)

5. **Core configuration**
   ```python
   # config.py
   class Settings(BaseSettings):
       DATABASE_URL: str
       ANTHROPIC_API_KEY: str
       STRIPE_API_KEY: Optional[str]
       
       # Agent service URLs
       SUMMARIZER_URL: str = "http://localhost:8001"
       TRANSLATOR_URL: str = "http://localhost:8002"
       SEARCH_URL: str = "http://localhost:8003"
       
       # HubChat orchestrator
       HUBCHAT_ENABLED: bool = True
       
       class Config:
           env_file = ".env"
   ```

**Deliverable**: Working database connection + models + repositories

---

### **Phase 2: Agent Management APIs** (Priority: HIGH)

#### Tasks:
1. **Implement `/api/agents` endpoints**
   ```python
   # server/api/agents.py
   
   @router.get("/agents", response_model=List[Agent])
   async def list_agents(db: Session = Depends(get_db)):
       """List all available agents from registry"""
       return await agent_service.get_all_agents(db)
   
   @router.get("/agents/{agent_id}", response_model=Agent)
   async def get_agent(agent_id: str, db: Session = Depends(get_db)):
       """Get specific agent details"""
       agent = await agent_service.get_agent(db, agent_id)
       if not agent:
           raise HTTPException(404, "Agent not found")
       return agent
   ```

2. **Agent registry seeding**
   - Populate database with agents from `services/` folder
   - Map agent services to database records:
     ```python
     agents = [
         {
             "id": "summarizer",
             "name": "Summarizer Agent",
             "endpointUrl": "http://localhost:8001",
             "skills": ["summarization", "text_analysis"],
             ...
         },
         {
             "id": "translator", 
             "name": "Translator Agent",
             "endpointUrl": "http://localhost:8002",
             "skills": ["translation", "language"],
             ...
         },
         # ... more agents
     ]
     ```

3. **Agent health monitoring**
   - Periodic health checks to agent services
   - Update `availability` and `load` fields
   - Track `avgResponseTime`

**Deliverable**: Working agent listing + details APIs

---

### **Phase 3: Task Execution & Orchestration** (Priority: HIGH)

#### Tasks:
1. **Implement `/api/tasks` endpoints**
   ```python
   # server/api/tasks.py
   
   @router.post("/tasks", response_model=Task)
   async def create_task(
       task_data: TaskCreate,
       db: Session = Depends(get_db)
   ):
       """Create a new task"""
       return await task_service.create_task(db, task_data)
   
   @router.get("/tasks", response_model=List[Task])
   async def list_tasks(db: Session = Depends(get_db)):
       """List all tasks"""
       return await task_service.get_all_tasks(db)
   
   @router.get("/tasks/{task_id}/steps", response_model=List[TaskStep])
   async def get_task_steps(task_id: str, db: Session = Depends(get_db)):
       """Get execution steps for a task"""
       return await task_service.get_task_steps(db, task_id)
   ```

2. **Integrate with existing agent services**
   ```python
   # server/services/agent_service.py
   
   async def invoke_agent(
       agent_id: str,
       payload: dict,
       db: Session
   ) -> dict:
       """
       Invoke a specific agent microservice.
       Calls the agent's /execute endpoint.
       """
       agent = await get_agent(db, agent_id)
       if not agent:
           raise ValueError(f"Agent {agent_id} not found")
       
       async with httpx.AsyncClient() as client:
           response = await client.post(
               f"{agent.endpointUrl}/execute",
               json=payload,
               timeout=30.0
           )
           response.raise_for_status()
           return response.json()
   ```

3. **Direct agent invocation endpoint**
   ```python
   @router.post("/invoke-agent")
   async def invoke_agent_endpoint(
       request: InvokeAgentRequest,
       db: Session = Depends(get_db),
       background_tasks: BackgroundTasks = BackgroundTasks()
   ):
       """
       Execute a single agent directly.
       Creates task step, records payment, updates agent metrics.
       """
       result = await agent_service.invoke_agent(
           agent_id=request.agentId,
           task_id=request.taskId,
           payload=request.payload,
           db=db
       )
       
       # Record payment in background
       background_tasks.add_task(
           payment_service.record_agent_payment,
           task_id=request.taskId,
           agent_id=request.agentId,
           amount=result['cost'],
           db=db
       )
       
       return result
   ```

**Deliverable**: Working task creation + agent invocation

---

### **Phase 4: HubChat Integration** (Priority: MEDIUM)

#### Tasks:
1. **HubChat orchestrator client**
   ```python
   # server/services/orchestrator_client.py
   
   from hubchat.orchestrator import process_request
   
   class OrchestratorClient:
       """Client for HubChat orchestrator"""
       
       async def process_user_query(
           self,
           user_query: str,
           max_budget: float,
           db: Session
       ) -> dict:
           """
           Send user query to HubChat orchestrator.
           HubChat will autonomously select and invoke agents.
           """
           result = await process_request(
               user_query=user_query,
               max_budget=max_budget
           )
           
           # Create task record
           task = await self._create_task_from_orchestrator_result(
               db, user_query, result
           )
           
           # Record agent invocations as task steps
           for agent_info in result.get('agents_used', []):
               await self._record_task_step(db, task.id, agent_info)
           
           return {
               "task_id": task.id,
               "output": result['output'],
               "cost": result['cost_breakdown']['total_cost']
           }
   ```

2. **Implement `/api/hubchat/message` endpoint**
   ```python
   # server/api/hubchat.py
   
   @router.post("/hubchat/message")
   async def send_hubchat_message(
       request: HubChatMessageRequest,
       db: Session = Depends(get_db),
       orchestrator: OrchestratorClient = Depends(get_orchestrator)
   ):
       """
       Process user message through HubChat orchestrator.
       HubChat coordinates multiple agents to complete the request.
       """
       # Save user message
       user_msg = await message_service.create_message(
           db, role="user", content=request.content
       )
       
       # Process through orchestrator
       result = await orchestrator.process_user_query(
           user_query=request.content,
           max_budget=1.0,  # Default budget
           db=db
       )
       
       # Save assistant response
       assistant_msg = await message_service.create_message(
           db,
           role="assistant",
           content=result['output'],
           task_id=result['task_id'],
           cost_breakdown={
               "subtasks": result.get('subtasks', []),
               "total": result['cost']
           }
       )
       
       return {"success": True}
   
   @router.get("/messages", response_model=List[Message])
   async def get_messages(db: Session = Depends(get_db)):
       """Get chat message history"""
       return await message_service.get_all_messages(db)
   ```

3. **Background task execution**
   - HubChat orchestrator runs in background
   - Updates task status asynchronously
   - Creates task steps as agents complete work
   - Records payments for each agent invocation

**Deliverable**: Working HubChat integration with multi-agent workflows

---

### **Phase 5: Payment Tracking & Monitoring** (Priority: MEDIUM)

#### Tasks:
1. **Implement payment endpoints**
   ```python
   # server/api/payments.py
   
   @router.get("/payments/bazaarbucks", response_model=List[BazaarBucksPayment])
   async def get_bazaarbucks_payments(db: Session = Depends(get_db)):
       """Get all internal BazaarBucks payments"""
       return await payment_service.get_bazaarbucks_payments(db)
   
   @router.get("/payments/stripe", response_model=List[StripePayment])
   async def get_stripe_payments(db: Session = Depends(get_db)):
       """Get all external Stripe payments"""
       return await payment_service.get_stripe_payments(db)
   
   @router.post("/payments/bazaarbucks")
   async def record_bazaarbucks_payment(
       payment: BazaarBucksPaymentCreate,
       db: Session = Depends(get_db)
   ):
       """Record internal payment (called automatically after agent execution)"""
       return await payment_service.create_bazaarbucks_payment(db, payment)
   ```

2. **Automatic payment recording**
   - After each agent invocation, record BazaarBucks payment
   - If agent requires external tool, record Stripe payment
   - Update task `totalCost` field

3. **Cost calculation service**
   ```python
   # server/services/payment_service.py
   
   class PaymentService:
       async def calculate_task_cost(self, db: Session, task_id: str) -> float:
           """Calculate total cost for a task (internal + external)"""
           steps = await task_repo.get_task_steps(db, task_id)
           
           total_internal = sum(step.cost for step in steps)
           total_external = sum(step.externalCost for step in steps)
           
           return total_internal + total_external
       
       async def record_agent_payment(
           self,
           db: Session,
           task_id: str,
           agent_id: str,
           amount: float,
           external_cost: float = 0.0
       ):
           """Record payment after agent execution"""
           # Record BazaarBucks payment
           await self.create_bazaarbucks_payment(db, {
               "taskId": task_id,
               "agentId": agent_id,
               "amount": amount,
               "type": "agent_payment"
           })
           
           # Record Stripe payment if applicable
           if external_cost > 0:
               await self.create_stripe_payment(db, {
                   "agentId": agent_id,
                   "vendor": "External API",
                   "amount": external_cost,
                   "status": "completed",
                   "type": "card_spend"
               })
   ```

**Deliverable**: Complete payment tracking system

---

## 🔄 Integration Architecture

### Request Flow: HubChat Message

```
User (UI) 
  ↓ POST /api/hubchat/message {"content": "Translate 'hello' to Spanish"}
FastAPI Backend (server/)
  ↓ orchestrator_client.process_user_query()
HubChat Orchestrator (hubchat/orchestrator.py)
  ↓ Claude Agent SDK decides: use translator agent
  ↓ invoke_agent_tool(agent_id="translator", payload={...})
Translator Agent (services/translator/)
  ↓ POST http://localhost:8002/execute
  ↓ Returns: {"result": "hola", "cost": 0.02}
HubChat Orchestrator
  ↓ Returns aggregated result
FastAPI Backend
  ↓ Create Task, TaskStep, BazaarBucksPayment records
  ↓ Save assistant message
User (UI)
  ↓ Receives response in chat
```

### Request Flow: Direct Agent Invocation

```
User (UI)
  ↓ POST /api/invoke-agent {"agentId": "summarizer", "taskId": "...", "payload": {...}}
FastAPI Backend
  ↓ agent_service.invoke_agent()
  ↓ POST http://localhost:8001/execute
Summarizer Agent (services/summarizer/)
  ↓ Returns: {"result": "Summary text", "cost": 0.03}
FastAPI Backend
  ↓ Create TaskStep record
  ↓ Record BazaarBucksPayment
  ↓ Update Task totalCost
User (UI)
  ↓ Receives result
```

---

## 📁 Detailed File Structure

```
server/
├── main.py                         # FastAPI app + CORS + middleware
├── config.py                       # Settings with pydantic-settings
├── dependencies.py                 # FastAPI dependencies (get_db, get_orchestrator)
├── requirements.txt
│
├── api/                            # API route handlers
│   ├── __init__.py
│   ├── agents.py                   # /api/agents endpoints
│   ├── tasks.py                    # /api/tasks endpoints
│   ├── payments.py                 # /api/payments/* endpoints
│   └── hubchat.py                  # /api/hubchat/* + /api/messages endpoints
│
├── models/                         # Pydantic models (request/response)
│   ├── __init__.py
│   ├── agent.py                    # Agent, AgentCreate
│   ├── task.py                     # Task, TaskCreate, TaskStep
│   ├── payment.py                  # BazaarBucksPayment, StripePayment
│   └── message.py                  # Message, MessageCreate
│
├── db/                             # Database layer
│   ├── __init__.py
│   ├── database.py                 # SQLAlchemy engine + session
│   ├── base.py                     # Declarative base
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── task.py
│   │   ├── payment.py
│   │   └── message.py
│   ├── repositories/               # Data access layer
│   │   ├── __init__.py
│   │   ├── agent_repo.py
│   │   ├── task_repo.py
│   │   ├── payment_repo.py
│   │   └── message_repo.py
│   └── migrations/                 # Alembic migrations
│       └── versions/
│
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── agent_service.py            # Agent invocation, health checks
│   ├── task_service.py             # Task creation, step tracking
│   ├── payment_service.py          # Payment recording, cost calculation
│   ├── message_service.py          # Chat message management
│   └── orchestrator_client.py      # HubChat orchestrator integration
│
├── schemas/                        # Additional Pydantic schemas
│   ├── __init__.py
│   └── requests.py                 # InvokeAgentRequest, HubChatMessageRequest
│
└── utils/                          # Utilities
    ├── __init__.py
    ├── logging.py                  # Structured logging
    └── health.py                   # Agent health checks
```

---

## 🔌 Environment Variables

```bash
# .env file for server/

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agentbazaar

# API Keys
ANTHROPIC_API_KEY=sk-ant-xxxxx
STRIPE_API_KEY=sk_test_xxxxx  # Optional

# Agent Service URLs
SUMMARIZER_URL=http://localhost:8001
TRANSLATOR_URL=http://localhost:8002
SEARCH_URL=http://localhost:8003
MOCK_BUSY_URL=http://localhost:8004
MOCK_HIGHPRICE_URL=http://localhost:8005
MOCK_NEGOTIATOR_URL=http://localhost:8006

# HubChat
HUBCHAT_ENABLED=true

# Server
SERVER_PORT=8000
CORS_ORIGINS=http://localhost:5000,http://localhost:3000

# Logging
LOG_LEVEL=INFO
```

---

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/test_agent_service.py
def test_invoke_agent_success():
    """Test successful agent invocation"""
    pass

def test_invoke_agent_not_found():
    """Test agent not found error"""
    pass
```

### Integration Tests
```python
# tests/test_api_integration.py
async def test_hubchat_message_flow():
    """Test complete HubChat message flow"""
    # 1. Send message
    # 2. Verify orchestrator called
    # 3. Verify task created
    # 4. Verify payments recorded
    pass
```

### Agent Mocking
```python
# tests/conftest.py
@pytest.fixture
def mock_agent_service(httpx_mock):
    """Mock agent HTTP calls"""
    httpx_mock.add_response(
        url="http://localhost:8001/execute",
        json={"result": "mocked result", "cost": 0.01}
    )
```

---

## 🚀 Deployment Strategy

### Development
```bash
# Terminal 1: Start agent services
./start_all_services.sh

# Terminal 2: Start FastAPI backend
cd server
uvicorn main:app --reload --port 8000

# Terminal 3: Start UI
cd ui
npm run dev  # Runs on port 5000
```

### Production (Replit)
```bash
# Use Replit workflow to start all services
# Update .replit to run:
run = "bash -c './start_all_services.sh & cd server && uvicorn main:app --port 8000 & cd ui && npm run dev'"
```

### Docker (Future)
```dockerfile
# Docker Compose for all services
services:
  backend:
    build: ./server
    ports: ["8000:8000"]
    depends_on: [db]
  
  summarizer:
    build: ./services/summarizer
    ports: ["8001:8001"]
  
  # ... more agents
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: agentbazaar
```

---

## 📊 Success Metrics

### Phase Completion Criteria

**Phase 1 (Foundation)**:
- ✅ Database schema created
- ✅ All Pydantic models defined
- ✅ Repository pattern working
- ✅ Can connect to database

**Phase 2 (Agent APIs)**:
- ✅ `GET /api/agents` returns agent list
- ✅ `GET /api/agents/:id` returns agent details
- ✅ Agents seeded from services/
- ✅ UI marketplace displays agents

**Phase 3 (Task Execution)**:
- ✅ `POST /api/tasks` creates task
- ✅ `POST /api/invoke-agent` calls agent service
- ✅ Task steps recorded in database
- ✅ UI task page shows execution history

**Phase 4 (HubChat)**:
- ✅ `POST /api/hubchat/message` works
- ✅ Orchestrator invokes multiple agents
- ✅ Chat messages saved to database
- ✅ UI chat shows conversation

**Phase 5 (Payments)**:
- ✅ `GET /api/payments/*` returns payment logs
- ✅ Payments auto-recorded after agent execution
- ✅ UI payments page shows transactions
- ✅ Cost calculations accurate

---

## ⚠️ Technical Considerations

### 1. **CORS Configuration**
```python
# server/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # UI dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. **Async Operations**
- Use `async/await` throughout
- `httpx.AsyncClient` for HTTP calls to agents
- `asyncpg` for database (or SQLAlchemy with async support)

### 3. **Error Handling**
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
```

### 4. **Agent Health Checks**
- Periodic background task to check agent `/health` endpoints
- Update `availability` and `avgResponseTime` fields
- Mark agents as unavailable if health check fails

### 5. **Database Migrations**
```bash
# Initialize Alembic
alembic init server/db/migrations

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

---

## 🎯 Next Steps

### Immediate Actions (After Plan Approval):

1. **Create directory structure**
   ```bash
   mkdir -p server/{api,models,db/{models,repositories,migrations},services,schemas,utils}
   ```

2. **Setup virtual environment**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Create requirements.txt**
   ```txt
   fastapi==0.115.0
   uvicorn[standard]==0.32.1
   sqlalchemy==2.0.36
   alembic==1.14.0
   psycopg2-binary==2.9.10
   pydantic==2.10.3
   pydantic-settings==2.6.1
   httpx==0.28.1
   python-dotenv==1.0.1
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start Phase 1 implementation**

---

## 📋 Summary

This plan creates a **production-ready FastAPI backend** that:

✅ **Replaces** the Express mock server with real Python backend  
✅ **Implements** all 11 API endpoints the UI needs  
✅ **Integrates** with your existing agent microservices  
✅ **Connects** to HubChat orchestrator for multi-agent workflows  
✅ **Persists** all data in PostgreSQL database  
✅ **Tracks** payments (BazaarBucks + Stripe)  
✅ **Maintains** API compatibility with existing React UI  
✅ **Follows** FastAPI best practices for 2025  

**Estimated Timeline**: 3-5 days (with focused work)

---

## ❓ Questions for You

Before we start implementation:

1. **Database**: Use Replit's built-in Postgres or external? (I recommend Replit's)
2. **Port**: Backend on port 8000 (current plan) or different?
3. **Priority**: Start with Phase 1 immediately, or review plan first?
4. **Stripe**: Do you have Stripe integration already, or mock it for now?
5. **Agent URLs**: Are services running on localhost:8001-8006, or different hosts?

**Ready to start building?** 🚀
