# Agent Bazaar

A multi-agent orchestration platform with integrated marketplace and payment systems.

## Project Structure

This monorepo contains both backend and frontend components:

```
AgentBazaar/
├── api/              # FastAPI backend services
├── hubchat/          # Agent orchestration system
├── services/         # Backend microservices
├── ui/               # React frontend (complete UI implementation)
└── requirements.txt  # Python dependencies
```

## Components

### Backend (Python/FastAPI)
- **api/**: RESTful API endpoints
- **hubchat/**: Multi-agent orchestration engine
- **services/**: Supporting backend services

### Frontend (React/TypeScript)
- **ui/**: Complete UI implementation
  - React SPA with shadcn/ui components
  - Express mock backend for development
  - See [ui/README.md](ui/README.md) for details

## Getting Started

### Backend Setup
```bash
pip install -r requirements.txt
# Additional backend setup instructions to be added
```

### Frontend Setup
```bash
cd ui
npm install
npm run dev
```

The UI will run on http://localhost:5000

## Development

- **Backend**: Python 3.x with FastAPI
- **Frontend**: Node.js with React 18 + TypeScript + Vite
- **Database**: PostgreSQL (planned)
- **Payment**: Stripe integration (planned)

## License

TBD
