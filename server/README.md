# Agent Bazaar FastAPI Backend

Production-ready Python FastAPI backend for the Agent Bazaar multi-agent orchestration platform.

## Features

- ✅ **RESTful API** - All endpoints UI needs (agents, tasks, payments, hubchat)
- ✅ **PostgreSQL Database** - Persistent storage with SQLAlchemy ORM
- ✅ **Agent Integration** - Connects to microservices on ports 8001-8006
- ✅ **HubChat Orchestration** - Multi-agent workflow coordination
- ✅ **Payment Tracking** - BazaarBucks (internal) + Stripe (external)
- ✅ **Type Safety** - Pydantic models matching TypeScript frontend
- ✅ **Async/Await** - High-performance async operations
- ✅ **Auto Documentation** - OpenAPI/Swagger docs at `/docs`

## Quick Start

### On Replit (Production)

The `.env` file is already configured with DATABASE_URL from Replit Postgres.

```bash
# Install dependencies
cd server
pip install -r requirements.txt

# Initialize database
python -c "import asyncio; from db.database import init_db; asyncio.run(init_db())"

# Start server
python main.py
```

Server will be running at http://0.0.0.0:8000

### Local Development

See [LOCAL_SETUP.md](./LOCAL_SETUP.md) for detailed instructions on running locally with Docker or local PostgreSQL.

## API Endpoints

### Agents
- `GET /api/agents` - List all agents
- `GET /api/agents/{id}` - Get agent details

### Tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/{id}` - Get task details
- `GET /api/tasks/{id}/steps` - Get task execution steps

### Agent Execution
- `POST /api/invoke-agent` - Execute specific agent

### HubChat
- `POST /api/hubchat/message` - Send message to orchestrator
- `GET /api/messages` - Get chat history

### Payments
- `GET /api/payments/bazaarbucks` - Get internal payments
- `GET /api/payments/stripe` - Get external payments

## Architecture

```
server/
├── main.py              # FastAPI app entry point
├── config.py            # Settings from environment
├── api/                 # API route handlers
├── models/              # Pydantic schemas (request/response)
├── db/
│   ├── database.py      # SQLAlchemy setup
│   ├── models/          # ORM models
│   └── repositories/    # Data access layer
├── services/            # Business logic
└── utils/               # Utilities
```

## Environment Variables

Required:
- `DATABASE_URL` - PostgreSQL connection string (auto-set on Replit)

Optional:
- `ANTHROPIC_API_KEY` - For HubChat orchestration
- `SUMMARIZER_URL` - Summarizer agent URL (default: http://localhost:8001)
- `TRANSLATOR_URL` - Translator agent URL (default: http://localhost:8002)
- `SEARCH_URL` - Search agent URL (default: http://localhost:8003)
- `SERVER_PORT` - Server port (default: 8000)
- `CORS_ORIGINS` - Allowed origins (default: http://localhost:5000)
- `LOG_LEVEL` - Logging level (default: INFO)

## Development

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run with auto-reload
```bash
uvicorn main:app --reload --port 8000
```

### API Documentation
Visit http://localhost:8000/docs for interactive Swagger UI

### Testing
```bash
pytest tests/
```

## Integration with Existing Services

This backend integrates with:

1. **Agent Microservices** (`services/` folder)
   - Summarizer (port 8001)
   - Translator (port 8002)
   - Search (port 8003)
   - Mock agents (ports 8004-8006)

2. **HubChat Orchestrator** (`hubchat/orchestrator.py`)
   - Multi-agent workflow coordination
   - Claude SDK integration

3. **React Frontend** (`ui/client/`)
   - All API contracts match TypeScript schemas
   - CORS configured for http://localhost:5000

## Database

### Initialize database tables
```bash
python -c "import asyncio; from db.database import init_db; asyncio.run(init_db())"
```

### Database models
- `agents` - Agent registry
- `tasks` - User tasks
- `task_steps` - Execution timeline
- `bazaarbucks_payments` - Internal payments
- `stripe_payments` - External payments
- `messages` - HubChat history

## Next Steps

1. ✅ Phase 1: Foundation & Database (COMPLETE)
2. 🔨 Phase 2: Agent Management APIs (IN PROGRESS)
3. ⏳ Phase 3: Task Execution & Orchestration
4. ⏳ Phase 4: HubChat Integration
5. ⏳ Phase 5: Payment Tracking

See [BACKEND_IMPLEMENTATION_PLAN.md](../BACKEND_IMPLEMENTATION_PLAN.md) for full roadmap.

## License

MIT
