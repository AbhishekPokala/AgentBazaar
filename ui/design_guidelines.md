# Agentic Marketplace - Design Guidelines

## Design Approach

**Selected Approach**: Design System - Linear/Stripe-inspired technical platform aesthetic

**Rationale**: This is a data-intensive technical marketplace requiring clarity, precision, and professional polish. The design should communicate reliability and efficiency while making complex agent orchestration approachable. Linear's spatial clarity combined with Stripe's dashboard precision provides the ideal foundation.

**Core Principles**:
- Information hierarchy over decoration
- Spacious layouts that handle dense data gracefully
- Purposeful animations only for state transitions
- Professional polish that builds user trust

---

## Typography System

**Font Stack**: 
- Primary: Inter (Google Fonts) - headings, UI labels, buttons
- Secondary: JetBrains Mono (Google Fonts) - code snippets, agent IDs, technical data

**Hierarchy**:
- Page Titles: text-3xl font-semibold (32px)
- Section Headers: text-xl font-semibold (20px)
- Card Titles: text-base font-medium (16px)
- Body Text: text-sm (14px)
- Metadata/Labels: text-xs uppercase tracking-wide font-medium (12px)
- Technical Data: JetBrains Mono text-sm

---

## Layout System

**Spacing Primitives**: Use Tailwind units of **2, 4, 6, 8, 12, 16** consistently
- Tight spacing: p-2, gap-2 (within components)
- Standard spacing: p-4, gap-4 (between related elements)
- Section spacing: p-8, py-12 (page sections)
- Large breathing room: py-16 (major page divisions)

**Grid System**:
- Marketplace: grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6
- Dashboard layouts: 2-column split (main content + sidebar)
- Agent details: Single column max-w-4xl centered

**Container Strategy**:
- Full-width app shell with fixed sidebar (16rem width)
- Main content: max-w-7xl mx-auto px-6
- Cards and modals: max-w-2xl

---

## Component Library

### Navigation
**Top Bar** (fixed, h-16):
- Logo + marketplace name (left)
- Search bar (center, max-w-md)
- User balance (BazaarBucks display), notification bell, profile avatar (right)
- All items vertically centered with gap-4

**Sidebar** (fixed left, w-64):
- Navigation items with icons (Heroicons)
- Active state: subtle left border (border-l-2)
- Sections: Marketplace, HubChat, Task History, Payment Logs, Settings
- Spacing: py-2 per item, px-4 container padding

### Agent Cards (Marketplace)
**Structure** (border rounded-lg p-6):
- Agent icon/avatar (h-12 w-12 rounded-full)
- Agent name (text-lg font-semibold)
- Skills tags (flex flex-wrap gap-2, each tag: px-3 py-1 rounded-full text-xs)
- Pricing grid (2 columns):
  - Base Price | Dynamic Price
  - Load indicator | Rating (with star icon)
- Jobs completed badge
- "View Details" button (w-full mt-4)

**Layout**: Hover state elevates card slightly (shadow-lg transition)

### HubChat Interface
**Container**: Full height split layout
- Messages area (flex-1 overflow-y-auto px-6 py-4)
- Input area (fixed bottom, p-4 border-t)

**Message Bubbles**:
- User messages: ml-auto max-w-lg bg-primary text-white rounded-2xl rounded-tr-sm p-4
- Agent responses: mr-auto max-w-lg bg-secondary rounded-2xl rounded-tl-sm p-4
- Spacing: space-y-4 between messages

**Cost Breakdown Component** (within agent responses):
- Subtle inset box (bg-subtle p-4 rounded-lg mt-3)
- Each subtask: flex justify-between items-center text-sm
- Total row: border-t pt-2 mt-2 font-semibold

**Input Area**:
- Textarea (w-full rounded-lg p-3 min-h-12)
- Send button (absolute right-3 bottom-3)
- Character/token counter (text-xs bottom-left)

### Task Execution Dashboard
**Timeline Visualization** (vertical stepper):
- Each step: flex gap-4 items-start
- Step indicator: h-8 w-8 rounded-full flex items-center justify-center
- Content area: flex-1 border-l-2 pl-6 pb-8
- Status badges: In Progress (animated pulse), Completed (checkmark), Failed (X icon)

**Step Details Card**:
- Agent name + icon
- Execution time
- Cost breakdown (internal + external if applicable)
- Output preview (max-h-32 overflow-hidden with "Show more" expansion)

### Payment Logs UI
**Dual-Tab Interface**:
- Tab headers: BazaarBucks | Stripe Transactions
- Active tab: border-b-2

**Table Structure**:
- Sticky header (bg-surface border-b font-medium text-xs uppercase)
- Columns: Date, Agent/Vendor, Type, Amount, Task ID, Status
- Row height: h-14, hover state background shift
- Pagination controls: bottom-center with page numbers

**Filters Panel** (collapsible sidebar):
- Date range picker
- Agent filter (multi-select)
- Amount range slider
- Transaction type checkboxes
- Export CSV button (w-full mt-4)

### Agent Detail Modal/Page
**Hero Section** (py-12 border-b):
- Agent avatar (h-24 w-24)
- Name + description
- Primary stats row (flex gap-8): Rating, Jobs, Avg Response Time
- "Invoke Agent" CTA button

**Tabs Section**:
- Capabilities | Pricing | Performance History | Sample Outputs
- Tab content: py-8 max-w-3xl

**Pricing Breakdown Table**:
- Base rate vs Dynamic rate comparison
- Load-based pricing visualization (simple bar chart)
- Historical pricing trend (sparkline chart)

---

## Forms & Inputs

**Standard Input**:
- Height: h-11
- Padding: px-4
- Border: border rounded-lg
- Focus: ring-2 ring-offset-2

**Labels**: text-sm font-medium mb-2 block

**Button Sizes**:
- Primary action: px-6 py-2.5 rounded-lg font-medium
- Secondary: px-4 py-2 rounded-md
- Icon-only: h-10 w-10 rounded-lg

---

## Data Visualization

**Agent Load Indicator**: Horizontal progress bar (h-2 rounded-full w-full)
**Rating Display**: Star icons + numeric value (4.8/5.0 format)
**Cost Trends**: Minimalist sparkline charts (react-sparklines or similar)
**Task Progress**: Circular progress indicator for active tasks

---

## Animations

Use sparingly:
- Card hover: transform scale-[1.01] transition-transform
- Modal entry: fade + slide from center
- Loading states: subtle pulse on skeleton loaders
- Message appearance: fade-in from bottom
- Tab transitions: crossfade content

---

## Images

**Agent Avatars**: Abstract geometric patterns or robot icons (use DiceBear API or similar for consistent generated avatars based on agent ID)

**Empty States**: 
- Empty marketplace: Illustration of connected nodes/agents (use unDraw or similar)
- No chat history: Simple messaging icon with helper text
- No transactions: Empty ledger illustration

**No hero image needed** - this is a functional dashboard, not a marketing site.