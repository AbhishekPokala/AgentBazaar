# Local Development Setup

## Prerequisites
- Python 3.10+
- PostgreSQL 15+ (or Docker)

## Option 1: Docker PostgreSQL (Recommended)

### 1. Start PostgreSQL container
```bash
docker run --name agentbazaar-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=agentbazaar \
  -p 5432:5432 \
  -d postgres:15
```

### 2. Verify database is running
```bash
docker ps | grep agentbazaar-db
```

### 3. Create `.env` file
```bash
cd server
cp .env.example .env
```

Edit `.env`:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/agentbazaar
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Option 2: Local PostgreSQL Installation

### macOS
```bash
brew install postgresql@15
brew services start postgresql@15
createdb agentbazaar
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install postgresql-15
sudo -u postgres createdb agentbazaar
```

### Windows
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install and start the service
3. Create database using pgAdmin or:
```cmd
createdb agentbazaar
```

### Create `.env` file
```bash
cd server
cp .env.example .env
```

Edit `.env`:
```bash
DATABASE_URL=postgresql://localhost/agentbazaar
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Installation

### 1. Create virtual environment
```bash
cd server
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize database
```bash
python -c "import asyncio; from db.database import init_db; asyncio.run(init_db())"
```

## Running the Server

### Development mode (with auto-reload)
```bash
cd server
source venv/bin/activate  # if not already activated
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running with Agent Services

### Terminal 1: Start all agent microservices
```bash
# From repository root
./start_all_services.sh
```

This starts:
- Summarizer Agent (port 8001)
- Translator Agent (port 8002)
- Search Agent (port 8003)
- Mock Agents (ports 8004-8006)

### Terminal 2: Start FastAPI backend
```bash
cd server
python main.py
```

### Terminal 3: Start UI (React frontend)
```bash
cd ui
npm run dev
```

## Stopping Services

### Stop backend
```
Ctrl+C in the terminal running main.py
```

### Stop agent services
```bash
./stop_all_services.sh
```

### Stop Docker database
```bash
docker stop agentbazaar-db
```

### Remove Docker database (deletes data!)
```bash
docker rm agentbazaar-db
```

## Troubleshooting

### Database connection error
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**: Make sure PostgreSQL is running:
```bash
# Docker:
docker ps | grep agentbazaar-db

# macOS:
brew services list | grep postgresql

# Linux:
sudo systemctl status postgresql
```

### Port already in use
```
ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Solution**: Kill process on port 8000:
```bash
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Missing ANTHROPIC_API_KEY
```
ValidationError: ANTHROPIC_API_KEY
```

**Solution**: Add your Anthropic API key to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key
```

## Development Workflow

1. Make code changes
2. Server auto-reloads (if using `--reload`)
3. Test endpoints at http://localhost:8000/docs
4. Check logs in terminal

## Next Steps

After local setup works, see `BACKEND_IMPLEMENTATION_PLAN.md` for:
- Phase 2: Implementing agent APIs
- Phase 3: Task execution
- Phase 4: HubChat integration
- Phase 5: Payment tracking
