"""
Seed database with agents from services folder
"""
import asyncio
import httpx
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db.database import AsyncSessionLocal
from db.repositories import AgentRepository
from models.agent import AgentCreate


# Agent service configurations
AGENT_SERVICES = [
    {
        "id": "summarizer",
        "port": 8001,
        "capabilities": ["text_processing", "analysis"],
        "rating": 4.8,
        "jobsCompleted": 1247,
        "avgResponseTime": 2.3,
        "load": 0.45,
        "availability": True
    },
    {
        "id": "translator",
        "port": 8002,
        "capabilities": ["language_translation", "localization"],
        "rating": 4.9,
        "jobsCompleted": 2891,
        "avgResponseTime": 1.8,
        "load": 0.62,
        "availability": True
    },
    {
        "id": "search",
        "port": 8003,
        "capabilities": ["web_search", "research", "tool_calling"],
        "rating": 4.7,
        "jobsCompleted": 856,
        "avgResponseTime": 4.2,
        "load": 0.33,
        "availability": True
    },
    {
        "id": "mock_busy",
        "port": 8004,
        "capabilities": ["demonstration", "load_testing"],
        "rating": 3.5,
        "jobsCompleted": 145,
        "avgResponseTime": 15.7,
        "load": 0.95,
        "availability": False
    },
    {
        "id": "mock_highprice",
        "port": 8005,
        "capabilities": ["premium_service", "demonstration"],
        "rating": 4.2,
        "jobsCompleted": 67,
        "avgResponseTime": 3.1,
        "load": 0.15,
        "availability": True
    },
    {
        "id": "mock_negotiator",
        "port": 8006,
        "capabilities": ["negotiation", "price_optimization"],
        "rating": 4.6,
        "jobsCompleted": 423,
        "avgResponseTime": 5.4,
        "load": 0.28,
        "availability": True
    },
]


async def fetch_agent_info(agent_id: str, port: int) -> dict:
    """
    Fetch agent info from service /info endpoint
    Falls back to defaults if service is not running
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"http://localhost:{port}/info")
            if response.status_code == 200:
                return response.json()
    except Exception as e:
        print(f"⚠️  Could not fetch info from {agent_id} service on port {port}: {e}")
    
    # Return defaults if service unavailable
    return {
        "name": f"{agent_id.replace('_', ' ').title()} Agent",
        "description": f"AI agent for {agent_id} tasks",
        "skills": [agent_id],
        "base_price": 0.10
    }


async def seed_agents():
    """Seed database with all agent services"""
    print("🌱 Starting agent database seeding...")
    
    async with AsyncSessionLocal() as session:
        try:
            repo = AgentRepository(session)
            
            # Check if agents already exist
            existing_agents = await repo.get_all()
            if existing_agents:
                print(f"ℹ️  Found {len(existing_agents)} existing agents")
                overwrite = input("Overwrite existing agents? (y/N): ").lower()
                if overwrite != 'y':
                    print("❌ Seeding cancelled")
                    return
                
                # Delete existing agents (inside transaction)
                print("🗑️  Deleting existing agents...")
                from db.models.agent import Agent as AgentModel
                from sqlalchemy import delete
                await session.execute(delete(AgentModel))
                print(f"🗑️  Deleted {len(existing_agents)} existing agents")
            
            # Create agents
            created_count = 0
            agents_to_create = []
            
            for config in AGENT_SERVICES:
                agent_id = config["id"]
                port = config["port"]
                
                print(f"\n📡 Fetching info for {agent_id} on port {port}...")
                info = await fetch_agent_info(agent_id, port)
                
                # Calculate dynamic price (base + load factor)
                base_price = info.get("base_price", 0.10)
                load = config["load"]
                dynamic_price = round(base_price * (1 + load * 0.5), 2)
                
                agent_data = AgentCreate(
                    id=agent_id,
                    name=info.get("name", f"{agent_id.title()} Agent"),
                    description=info.get("description", f"AI agent for {agent_id}"),
                    skills=info.get("skills", [agent_id]),
                    capabilities=config["capabilities"],
                    endpoint_url=f"http://localhost:{port}",
                    rating=config["rating"],
                    jobs_completed=config["jobsCompleted"],
                    avg_response_time=config["avgResponseTime"],
                    load=config["load"],
                    availability=config["availability"],
                    base_price=base_price,
                    dynamic_price=dynamic_price
                )
                
                agents_to_create.append((agent_data, agent_id))
            
            # Bulk create all agents in one transaction
            from db.models.agent import Agent as AgentModel
            for agent_data, agent_id in agents_to_create:
                try:
                    # Skip validation check since we're in a transaction after deletion
                    agent = AgentModel(**agent_data.model_dump())
                    session.add(agent)
                    created_count += 1
                    print(f"✅ Prepared agent: {agent_data.name}")
                    print(f"   ID: {agent_data.id}")
                    print(f"   Skills: {', '.join(agent_data.skills)}")
                    print(f"   Base Price: ${agent_data.base_price:.2f}")
                    print(f"   Dynamic Price: ${agent_data.dynamic_price:.2f}")
                    print(f"   Rating: {agent_data.rating}/5.0")
                    print(f"   Jobs: {agent_data.jobs_completed}")
                    print(f"   Availability: {'✓' if agent_data.availability else '✗'}")
                except Exception as e:
                    print(f"❌ Failed to prepare {agent_id}: {e}")
                    raise  # Re-raise to trigger rollback
            
            # Commit transaction
            await session.commit()
            print(f"\n✨ Successfully seeded {created_count}/{len(AGENT_SERVICES)} agents!")
            
        except Exception as e:
            # Rollback on any error
            await session.rollback()
            print(f"\n❌ Seeding failed and was rolled back: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_agents())
