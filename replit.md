# Agent Bazaar

## Overview

Agent Bazaar is a multi-agent orchestration platform with an integrated marketplace and payment systems. This Replit project contains the complete UI implementation.

**Repository Structure:**
- `ui/` - Complete frontend implementation (React SPA + Express dev server)
  - `ui/server/` - FastAPI backend (port 8000) for HubChat orchestration
  - `ui/client/` - React frontend (served via Express on port 5000)
- Backend services (FastAPI) are in separate folders: `api/`, `hubchat/`, `services/`

The UI provides a data-intensive interface that prioritizes information hierarchy, spacious layouts for dense data, and professional polish inspired by Linear/Stripe design systems.

**Development Setup:**
- Frontend (React + Express): Runs on port 5000 via "Start application" workflow
- Backend (FastAPI): Runs on port 8000 (requires separate workflow or manual start)
- See `PHASE4_INTEGRATION_GUIDE.md` for detailed setup instructions

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

## Project Structure

All UI code is organized in the `ui/` folder:
```
ui/
├── client/           # React frontend (port 5000)
├── server/           # FastAPI backend (port 8000)
│   ├── main.py       # FastAPI app definition
│   ├── run_server.py # Server runner (no auto-reload)
│   ├── routers/      # API route handlers
│   ├── db/           # Database models and repositories
│   └── config.py     # Server configuration
├── shared/           # Shared TypeScript schemas  
├── package.json      # Frontend dependencies
├── .env              # Environment variables (VITE_API_BASE_URL)
└── design_guidelines.md
```

### Frontend Architecture

**Framework**: React 18+ with TypeScript and Vite as the build tool
**Location**: `ui/client/`

**Design System**: shadcn/ui components built on Radix UI primitives
- Styled with Tailwind CSS using custom design tokens
- "New York" style variant with neutral base colors
- Custom color system supporting light/dark themes
- Typography: Inter for UI, JetBrains Mono for technical data

**State Management**:
- TanStack Query (React Query) for server state and API data fetching
- React hooks for local component state
- Query client configured with strict caching (staleTime: Infinity)

**Routing**: Wouter (lightweight client-side routing)

**Key UI Patterns**:
- Sidebar navigation with collapsible states
- Dialog modals for detailed views
- Tab-based organization for multi-section content
- Card-based layouts for marketplace listings
- Toast notifications for user feedback

**Pages**:
- `/` - Agent marketplace with search and filtering
- `/hubchat` - Chat interface with orchestrator agent
- `/tasks` - Task execution history and logs
- `/payments` - Payment transaction logs (BazaarBucks and Stripe)
- `/settings` - User preferences and configuration

### Backend Architecture

**Framework**: FastAPI with Python 3.x (port 8000)

**Architecture Pattern**: REST API with PostgreSQL database via SQLAlchemy async ORM

**API Endpoints**:
- **Agents**:
  - `GET /api/agents` - List all agents
  - `GET /api/agents/{id}` - Get agent details
  - `POST /api/agents` - Create new agent
  - `PATCH /api/agents/{id}` - Update agent
  - `DELETE /api/agents/{id}` - Delete agent

- **Tasks**:
  - `GET /api/tasks` - List all tasks
  - `GET /api/tasks/{id}` - Get task details
  - `GET /api/tasks/{id}/steps` - Get task execution steps
  - `POST /api/tasks` - Create new task

- **Agent Invocation**:
  - `POST /api/invoke-agent` - Invoke an agent for execution

- **HubChat** (Conversational Orchestration):
  - `GET /api/messages` - Get chat message history
  - `POST /api/hubchat/message` - Send message to orchestrator
  - `GET /api/hubchat/messages?task_id={id}` - Get task-specific messages
  - `DELETE /api/hubchat/messages/{task_id}` - Clear task conversation

**Storage Layer**:
- PostgreSQL database (via Replit's built-in Postgres)
- SQLAlchemy async ORM with Pydantic models
- Repository pattern for data access
- Database migrations handled by Alembic

**HubChat Integration**:
- ConversationalOrchestrator class (in `/hubchat/conversational_orchestrator.py`)
- Claude SDK (Anthropic) for AI-powered orchestration
- Full conversation context retention across multiple turns
- Task creation and agent invocation capabilities
- Cost tracking for Claude API usage

**Development Server**:
- Entry point: `ui/server/run_server.py` (uvicorn without auto-reload)
- CORS enabled for frontend communication
- JSON request/response handling
- Health check endpoint: `/health`

**Frontend Integration Server** (Express.js - port 5000):
- Vite middleware integration for HMR in development
- Static file serving in production
- Proxies API requests to FastAPI backend

### Data Models

**Agent**:
- Identity: id, name, description
- Capabilities: skills array, capabilities array, endpointUrl
- Performance metrics: rating, jobsCompleted, avgResponseTime, load
- Pricing: basePrice, dynamicPrice
- Status: availability boolean

**Task**:
- Lifecycle: id, status (created/in_progress/completed/failed), createdAt, completedAt
- Definition: userQuery, requiredSkills array
- Cost tracking: maxBudget, totalCost

**TaskStep**:
- Execution tracking: taskId, agentId, stepNumber
- Results: input, output, cost
- Status: status, startedAt, completedAt

**Payment Records**:
- BazaarBucksPayment: internal currency transactions
- StripePayment: external payment integration

**Message**:
- Chat history: id, role (user/assistant), content, timestamp
- Task association: optional task_id for task-specific conversations
- Cost tracking: cost_breakdown JSON for external API costs

### Design System Implementation

**Color Architecture**:
- CSS custom properties for theme tokens
- HSL-based color system with alpha channel support
- Separate light/dark mode definitions
- Semantic color naming (primary, secondary, muted, accent, destructive)
- Card and popover variants with dedicated border colors

**Spacing System**:
- Tailwind-based with consistent units: 2, 4, 6, 8, 12, 16
- Component-level: p-2, gap-2
- Section-level: p-4, gap-4, p-8, py-12
- Page-level: py-16

**Typography**:
- Inter for general UI and headings
- JetBrains Mono for code and technical identifiers
- Defined hierarchy: 3xl/xl/base/sm/xs
- Font loading via Google Fonts

**Layout Patterns**:
- Fixed sidebar: 16rem width
- Main content: max-w-7xl with horizontal padding
- Responsive grid: 1/2/3 columns based on breakpoint
- Centered modals: max-w-2xl to max-w-3xl

## External Dependencies

### UI Component Libraries
- **Radix UI**: Headless component primitives (dialogs, dropdowns, tabs, tooltips, etc.)
- **shadcn/ui**: Pre-styled component system built on Radix
- **Lucide React**: Icon library for consistent iconography

### Data Fetching
- **TanStack Query**: Server state management and caching

### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **class-variance-authority**: Component variant management
- **tailwind-merge**: Intelligent className merging

### Form Management
- **React Hook Form**: Form state and validation
- **Zod**: Schema validation
- **@hookform/resolvers**: Zod integration with React Hook Form

### Backend (Python/FastAPI)
- **FastAPI**: Modern async web framework
- **SQLAlchemy**: Async ORM for database operations
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server
- **Anthropic SDK**: Claude AI integration for HubChat
- **PostgreSQL**: Database (via Replit's built-in Postgres)

### Database (Active - PostgreSQL)
- **SQLAlchemy**: Async ORM for Python backend
- **Alembic**: Database migration tool
- **Connection**: Via DATABASE_URL environment variable (Replit managed)

### Development Tools
- **Vite**: Build tool and dev server
- **TypeScript**: Type safety across frontend and backend
- **@replit/vite-plugin-runtime-error-modal**: Development error overlay
- **@replit/vite-plugin-cartographer** and **@replit/vite-plugin-dev-banner**: Replit-specific dev tools

### Utilities
- **date-fns**: Date manipulation and formatting
- **nanoid**: Unique ID generation
- **wouter**: Lightweight routing

### Payment Integration (Planned)
- Stripe integration configured in schema but not yet implemented
- BazaarBucks internal currency system for marketplace transactions

## Recent Changes (November 2025)

### Phase 4: HubChat Integration Complete
- **FastAPI Backend**: Fully integrated with PostgreSQL database
- **ConversationalOrchestrator**: Claude SDK-based orchestration with full context retention
- **Message System**: Database-backed chat history with task association
- **Frontend Integration**: React frontend configured to communicate with FastAPI backend
- **Dual Server Setup**: Express (port 5000) + FastAPI (port 8000)
- **Environment Configuration**: VITE_API_BASE_URL for flexible backend targeting

See `PHASE4_INTEGRATION_GUIDE.md` for detailed setup and testing instructions.