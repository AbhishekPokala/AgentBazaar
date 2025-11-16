# Agentic Marketplace Platform - Design Guidelines

## Design Approach
**System**: Hybrid of Linear's clean data density + Stripe's professional dashboard aesthetic
**Rationale**: Utility-focused platform requiring efficient information display, clear hierarchy, and sophisticated financial data visualization.

## Typography System
**Families**: Inter (UI/data) + JetBrains Mono (financial figures/addresses)
- **Hero/Headers**: text-3xl to text-5xl, font-semibold
- **Section Titles**: text-xl, font-semibold
- **Body/Labels**: text-sm to text-base, font-medium
- **Data Values**: text-lg font-semibold (Inter), monospace for addresses/hashes
- **Metadata**: text-xs text-gray-500

## Layout & Spacing
**Spacing Primitives**: Use Tailwind units of 3, 4, 6, 8, 12
- Component padding: p-4 to p-6
- Section spacing: gap-6 to gap-8
- Card spacing: space-y-4
**Container**: max-w-7xl mx-auto, full viewport height dashboard layout

## Core Components

### Dashboard Header
Top bar with wallet display, search, and user actions. Sticky positioning with backdrop-blur.
- Left: Logo + platform navigation tabs
- Center: Global agent search with autocomplete
- Right: Wallet balance (USDC) in prominent card with "Add Funds" CTA, user menu

### Agent Discovery Cards (Grid Layout)
3-column grid (lg:grid-cols-3 md:grid-cols-2) with hover elevation:
- Agent avatar/icon (top-left)
- Agent name + verification badge
- Rating stars + review count
- Pricing: Prominent $/request or $/hour with usage tiers
- Capability tags (pills)
- Quick stats: Success rate, avg response time, total invocations
- "Compare" checkbox + "Deploy" primary button

### Orchestration Timeline Component
Horizontal stepper visualization with status indicators:
- Nodes: Discovery → Configuration → Invocation → Execution → Payment → Completion
- Each node shows: timestamp, status (pending/active/complete/failed), duration
- Connecting lines with animated progress indicator for active steps
- Expandable details panels beneath each node showing logs/metadata
- Color coding: Blue (active), Green (complete), Gray (pending), Red (failed)

### Transaction Log Table
Data-dense table with fixed header scroll:
- Columns: Timestamp, Agent, Action Type, Amount (USDC), Status, Transaction Hash (truncated, copyable)
- Row hover highlights entire row
- Status badges with icons
- Sortable columns
- Pagination footer with "Show 10/25/50/100 rows"
- Export button (top-right)

### Cost Breakdown Panel
Side panel or card displaying financial analytics:
- Total Spend: Large figure at top
- Breakdown pie/donut chart: Agent costs, platform fees, gas fees
- Line graph: Spending over time (daily/weekly/monthly toggle)
- Top agents by spend (mini list)
- Budget alerts/warnings if applicable

### Agent Comparison Modal
Full-screen overlay with side-by-side comparison:
- Up to 4 agents in columns
- Rows: Pricing tiers, capabilities, performance metrics, ratings, response times
- Highlight differences with subtle background color
- "Select for deployment" action buttons at bottom

## Interaction Patterns
- Hover states: Subtle shadow elevation, no color change on primary blue
- Loading states: Skeleton screens for data tables, shimmer effect
- Empty states: Centered illustration + helpful action text
- Toast notifications: Top-right for transaction confirmations

## Images
**No hero image** - this is a dashboard application.
**Agent Cards**: Include small circular avatar/logo placeholders (80x80px) for each agent - use gradient backgrounds or abstract patterns if no logo available.
**Empty States**: Simple line illustrations for "No transactions yet" or "Start discovering agents" states.

## Data Display Principles
- **Hierarchy through weight**: Use font-weight variations, not size changes, for data-dense areas
- **Monospace for precision**: All financial amounts, addresses, hashes in JetBrains Mono
- **Status clarity**: Color + icon + text label (never color alone)
- **Scannable tables**: Zebra striping (subtle), generous row height (h-12), clear column alignment
- **Real-time updates**: Subtle pulse animation for live data changes