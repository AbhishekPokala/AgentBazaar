# Agent Bazaar - UI (Frontend)

This directory contains the complete UI/frontend implementation for the Agent Bazaar marketplace platform.

## Overview

A React SPA with Express mock backend for the Agent Bazaar multi-agent orchestration platform. Features a Linear/Stripe-inspired design system with professional polish.

## Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **UI Components**: shadcn/ui (Radix primitives) + Tailwind CSS
- **State Management**: TanStack Query (React Query)
- **Routing**: Wouter
- **Backend (Mock)**: Express.js with in-memory storage

## Project Structure

```
ui/
├── client/                 # React frontend application
│   ├── src/
│   │   ├── pages/         # Page components (Marketplace, HubChat, Tasks, etc.)
│   │   ├── components/    # Reusable UI components
│   │   ├── lib/           # Utilities and query client
│   │   └── App.tsx        # Main app component
├── server/                 # Express mock backend
│   ├── routes.ts          # API endpoints
│   ├── storage.ts         # In-memory data storage
│   └── index.ts           # Server entry point
├── shared/                 # Shared TypeScript types
│   └── schema.ts          # Data models (Agent, Task, Payment, Message)
└── design_guidelines.md   # Design system documentation

```

## Features

### Pages
- **Marketplace** (`/`) - Browse and search AI agents with detailed modal views
- **HubChat** (`/hubchat`) - Multi-agent orchestration chat interface
- **Task History** (`/tasks`) - Visual timeline of task execution
- **Payment Logs** (`/payments`) - BazaarBucks and Stripe transaction logs
- **Settings** (`/settings`) - User preferences

### Key Features
- Professional Linear/Stripe-inspired design
- Dark/Light theme toggle
- Comprehensive error handling with retry buttons
- Skeleton loading states
- Real-time cost tracking
- Responsive grid layouts

## Installation

```bash
cd ui
npm install
```

## Development

```bash
npm run dev
```

The app will run on port 5000 with:
- Frontend served by Vite (HMR enabled)
- Backend API on `/api/*` routes
- Mock data pre-populated for demo

## API Endpoints

All endpoints are mocked with realistic data:

- `GET /api/agents` - List all agents
- `GET /api/agents/:id` - Get agent details
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/:id/steps` - Get task execution steps
- `POST /api/tasks` - Create new task
- `GET /api/messages` - Get chat messages
- `POST /api/hubchat/message` - Send chat message (creates task)
- `GET /api/payments/bazaarbucks` - Get internal payment logs
- `GET /api/payments/stripe` - Get Stripe payment logs

## Design System

The UI follows strict design guidelines (see `design_guidelines.md`):
- **Primary Color**: Professional blue (hsl(217 91% 60%))
- **Typography**: Inter (UI), JetBrains Mono (technical data)
- **Spacing**: Consistent 2/4/6/8 unit scale
- **Components**: shadcn/ui with custom theming

## Building for Production

```bash
npm run build
```

## Integration with Backend

This UI is currently using a mock Express backend. To integrate with the real FastAPI backend:

1. Update API endpoints in `client/src/lib/queryClient.ts`
2. Point to FastAPI server URL
3. Ensure CORS is configured on the backend
4. Update data models in `shared/schema.ts` if needed

## Notes

- Backend API (FastAPI) and agent orchestration are developed separately
- This is a UI-focused MVP with mock data
- All features are fully functional with realistic simulated responses
