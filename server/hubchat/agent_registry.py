"""
Agent Registry - Metadata about available agents
Includes skills, pricing, reviews, and ratings
"""

from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Agent metadata registry
AGENT_REGISTRY = {
    "summarizer": {
        "id": "summarizer",
        "name": "Summarizer Agent",
        "description": "Intelligent text summarization with configurable length",
        "skills": ["summarize", "condense", "analyze", "extract"],
        "base_price": 0.05,
        "rating": 4.8,
        "total_reviews": 127,
        "success_rate": 0.98,
        "avg_response_time": 2.3,
        "endpoint": "http://localhost:8001",
        "available": True,
        "locus_api_key": "locus_dev_9l9V7XuOYFsxDy9lLT731fPkY9WdAEX0",
        "wallet_address": "0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
        "client_id": "26rkc6d4301rr7g82bufc1tiv1"
    },
    "translator": {
        "id": "translator",
        "name": "Translator Agent",
        "description": "Language translation powered by Claude",
        "skills": ["translate", "localize", "language"],
        "base_price": 0.10,
        "rating": 4.9,
        "total_reviews": 203,
        "success_rate": 0.99,
        "avg_response_time": 1.8,
        "endpoint": "http://localhost:8002",
        "available": True,
        "locus_api_key": "locus_dev_jlpDXkiIoSB_fh0TTXx4myXLMAIcAmCO",
        "wallet_address": "0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
        "client_id": "3le4cmrdaropj60f58psn23hod"
    },
    "search": {
        "id": "search",
        "name": "Search Agent",
        "description": "Web search with AI synthesis of results",
        "skills": ["search", "research", "web", "find"],
        "base_price": 0.08,
        "rating": 4.7,
        "total_reviews": 89,
        "success_rate": 0.95,
        "avg_response_time": 4.5,
        "endpoint": "http://localhost:8003",
        "available": True,
        "locus_api_key": "locus_dev_cUsp0xYzhzR-I4YH5oLZFaxVHFhNXysW",
        "wallet_address": "0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
        "client_id": "7lic0eo18hof1o1dtrfv2ob733"
    },
    "mock_busy": {
        "id": "mock_busy",
        "name": "Busy Agent (Mock)",
        "description": "Simulates high load scenarios",
        "skills": ["test", "mock"],
        "base_price": 0.05,
        "rating": 3.2,
        "total_reviews": 45,
        "success_rate": 0.60,
        "avg_response_time": 8.0,
        "endpoint": "http://localhost:8004",
        "available": False  # Often busy
    },
    "mock_highprice": {
        "id": "mock_highprice",
        "name": "Premium Agent (Mock)",
        "description": "High-quality but expensive service",
        "skills": ["premium", "test"],
        "base_price": 0.85,
        "rating": 4.95,
        "total_reviews": 312,
        "success_rate": 0.99,
        "avg_response_time": 1.2,
        "endpoint": "http://localhost:8005",
        "available": True
    },
    "mock_negotiator": {
        "id": "mock_negotiator",
        "name": "Negotiator Agent (Mock)",
        "description": "Tests price negotiation scenarios",
        "skills": ["negotiate", "test"],
        "base_price": 0.50,
        "rating": 4.1,
        "total_reviews": 67,
        "success_rate": 0.88,
        "avg_response_time": 3.0,
        "endpoint": "http://localhost:8006",
        "available": True
    }
}


class AgentRegistry:
    """Agent discovery and selection system"""

    def __init__(self):
        self.agents = AGENT_REGISTRY

    def discover_by_skill(self, skill: str, max_price: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Find agents that match a specific skill.

        Args:
            skill: Skill to search for (e.g., "translate", "summarize")
            max_price: Optional maximum price filter

        Returns:
            List of matching agents, sorted by rating (best first)
        """
        matching_agents = []

        for agent_id, agent in self.agents.items():
            # Check if agent has the skill
            if any(skill.lower() in s.lower() for s in agent["skills"]):
                # Filter by price if specified
                if max_price and agent["base_price"] > max_price:
                    continue

                matching_agents.append(agent)

        # Sort by rating (descending), then by price (ascending)
        matching_agents.sort(key=lambda a: (-a["rating"], a["base_price"]))

        logger.info(f"Found {len(matching_agents)} agents for skill '{skill}'")
        return matching_agents

    def get_best_agent(self, skill: str, max_price: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Get the best agent for a skill based on rating and price.

        Args:
            skill: Skill required
            max_price: Optional budget constraint

        Returns:
            Best matching agent or None
        """
        agents = self.discover_by_skill(skill, max_price)

        if not agents:
            logger.warning(f"No agents found for skill '{skill}'")
            return None

        # Return highest-rated available agent
        for agent in agents:
            if agent.get("available", True):
                logger.info(f"Best agent for '{skill}': {agent['name']} (${agent['base_price']}, rating {agent['rating']})")
                return agent

        # If no available agents, return best one anyway (may fail)
        logger.warning(f"Best agent for '{skill}' may not be available")
        return agents[0]

    def get_agent_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent metadata by ID"""
        return self.agents.get(agent_id)

    def list_all_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents"""
        return list(self.agents.values())

    def estimate_cost(self, agent_ids: List[str]) -> float:
        """
        Estimate total cost for a list of agents.

        Args:
            agent_ids: List of agent IDs to use

        Returns:
            Total estimated cost in USD
        """
        total = 0.0
        for agent_id in agent_ids:
            agent = self.get_agent_by_id(agent_id)
            if agent:
                total += agent["base_price"]

        return total


# Global registry instance
registry = AgentRegistry()

