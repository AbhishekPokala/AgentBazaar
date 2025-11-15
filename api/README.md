# API Layer

FastAPI-based backend responsible for:
- Agent registry access (`/agents`)
- Task creation (`/task`)
- Agent invocation (`/invoke-agent`)
- Internal payments via Locus (`/payments/locus`)
- External payments via Stripe (`/payments/stripe/*`)
- Logging execution traces (`/logs/task/{id}`)
- Database integration
- Uniform execution pipeline for all agents

## Setup

```bash
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

## Endpoints

- `GET /agents` - List all available agents
- `POST /task` - Create a new task
- `POST /invoke-agent` - Invoke a specific agent
- `POST /payments/locus` - Process internal BazaarBucks payment
- `POST /payments/stripe/card-spend` - Process external Stripe payment
- `GET /logs/task/{id}` - Retrieve task execution logs

