# Agent Bazaar

A multi-agent orchestration platform with integrated marketplace and payment systems.

## Project Structure

This monorepo contains cleanly separated backend and frontend components:

```
AgentBazaar/
├── ui/                   # Frontend only
│   ├── client/           # React application
│   ├── package.json
│   ├── vite.config.ts
│   └── (all frontend configs)
└── server/               # Backend only
    ├── hubchat/          # Agent orchestration system
    ├── services/         # Agent microservices
    │   ├── summarizer/   # Claude-powered text summarization
    │   ├── translator/   # Claude-powered translation
    │   ├── search/       # Claude-powered search
    │   └── mock_*/       # Mock agents for testing
    ├── db/               # Database models & repositories
    ├── models/           # Pydantic models
    ├── routers/          # API endpoints
    ├── main.py           # FastAPI application entry point
    ├── .venv/            # Python virtual environment
    └── requirements.txt  # Python dependencies
```

## Components

### Backend (Python/FastAPI)
- **server/hubchat/**: Multi-agent orchestration engine with conversational AI
- **server/services/**: Agent microservices (Claude-powered and mock agents)
- **server/routers/**: RESTful API endpoints
- **server/db/**: Database layer with SQLAlchemy models and repositories
- **server/models/**: Pydantic schemas for request/response validation

### Frontend (React/TypeScript)
- **ui/client/**: Complete React SPA with shadcn/ui components
- Built with Vite for fast development and HMR
- TypeScript for type safety

## Getting Started

### Initial Setup

1. **Install Python dependencies**:
```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Install Node dependencies**:
```bash
cd ui
npm install
```

### Running All Services

**Start everything with one command:**
```bash
./start_all.sh
```

This starts:
- Frontend (Vite dev server) on http://localhost:5173
- Backend API (FastAPI) on http://localhost:8000
- 6 Agent Services on ports 8001-8006

**Stop all services:**
```bash
./stop_all_services.sh
```

### Service URLs
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Agents**: http://localhost:8001-8006

## Development

- **Backend**: Python 3.x with FastAPI
- **Frontend**: Node.js with React 18 + TypeScript + Vite
- **Database**: PostgreSQL (planned)
- **Payment**: Stripe integration (planned)

## License

TBD
