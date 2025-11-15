# HubChat - Central Orchestrator

Built with Anthropic Agent SDK, HubChat is the central orchestrator that:
- Parses user intent
- Extracts required skills
- Plans multi-step workflows
- Selects appropriate agents
- Negotiates prices (if applicable)
- Computes internal + external cost breakdown
- Calls API for invoking agents + payments
- Aggregates results
- Returns structured responses to UI

## Key Principle
**HubChat never calls agents or payments directly** — it only calls our API tools.

## Components

- `orchestrator.py` - Main orchestrator logic using Anthropic SDK
- `planner.py` - Task planning and decomposition
- `tools.py` - Tool definitions for API integration
- `prompts.py` - System prompts and templates

## Tools Available to HubChat

1. `list_agents` - Calls GET /agents
2. `create_task` - Calls POST /task
3. `invoke_agent` - Calls POST /invoke-agent
4. `trigger_locus_payment` - Calls POST /payments/locus
5. `trigger_stripe_card_spend` - Calls POST /payments/stripe/card-spend
6. `fetch_logs` - Calls GET /logs/task/{id}

