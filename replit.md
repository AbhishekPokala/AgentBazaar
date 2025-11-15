# Agent Bazaar

## Overview

Agent Bazaar is a multi-agent orchestration platform with an integrated marketplace and payment systems. This Replit project contains the complete UI implementation.

**Repository Structure:**
- `ui/` - Complete frontend implementation (React SPA + Express mock backend)
- Backend services (FastAPI) are in separate folders: `api/`, `hubchat/`, `services/`

The UI provides a data-intensive interface that prioritizes information hierarchy, spacious layouts for dense data, and professional polish inspired by Linear/Stripe design systems.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

## Project Structure

All UI code is organized in the `ui/` folder:
```
ui/
├── client/           # React frontend
├── server/           # Express mock backend  
├── shared/           # Shared TypeScript schemas
├── package.json      # Dependencies
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

**Framework**: Express.js with TypeScript running on Node.js

**Architecture Pattern**: REST API with in-memory storage (designed to be replaced with database)

**API Endpoints**:
- `GET /api/agents` - List all agents
- `GET /api/agents/:id` - Get agent details
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/:id` - Get task details
- `GET /api/tasks/:id/steps` - Get task execution steps
- `POST /api/tasks` - Create new task
- `POST /api/invoke-agent` - Simulate agent execution
- `GET /api/messages` - Get chat messages
- `POST /api/hubchat/message` - Send chat message
- `GET /api/payments/bazaarbucks` - Get internal payment logs
- `GET /api/payments/stripe` - Get Stripe payment logs

**Storage Layer**:
- Currently: In-memory storage using Map data structures (MemStorage class)
- Designed for: PostgreSQL via Drizzle ORM (configuration present but not yet implemented)
- Interface-based design allows swapping storage implementations

**Development Server**:
- Vite middleware integration for HMR in development
- Static file serving in production
- Request/response logging middleware
- JSON body parsing with raw body preservation (for webhooks)

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
- Chat history: role (user/assistant), content, timestamp

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

### Database (Configured but Not Active)
- **Drizzle ORM**: TypeScript ORM for PostgreSQL
- **@neondatabase/serverless**: Serverless Postgres driver
- **drizzle-zod**: Zod schema generation from Drizzle schemas
- Configuration present in drizzle.config.ts and shared/schema.ts

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