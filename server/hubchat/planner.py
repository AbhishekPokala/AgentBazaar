"""
Task planning and decomposition logic for HubChat.
"""

from typing import List, Dict, Any, Optional


class TaskPlanner:
    """Plans and decomposes user tasks into subtasks with agent assignments."""

    def __init__(self):
        # Skill to agent mapping (will be populated from API)
        self.skill_to_agents: Dict[str, List[str]] = {}

    def update_agent_registry(self, agents: List[Dict[str, Any]]):
        """Update the skill to agent mapping from the agent registry."""
        self.skill_to_agents = {}
        for agent in agents:
            for skill in agent.get("skills", []):
                if skill not in self.skill_to_agents:
                    self.skill_to_agents[skill] = []
                self.skill_to_agents[skill].append(agent["id"])

    def extract_skills(self, user_query: str) -> List[str]:
        """
        Extract required skills from user query.
        This is a simplified version - in practice, the LLM will do this.
        """
        # Keywords to skill mapping
        skill_keywords = {
            "summarize": ["summarize", "summary", "brief", "condense"],
            "translate": ["translate", "translation", "convert to"],
            "sentiment": ["sentiment", "emotion", "feeling", "tone"],
            "format": ["format", "formatting", "pdf", "document"],
        }

        query_lower = user_query.lower()
        skills = []

        for skill, keywords in skill_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                skills.append(skill)

        return skills

    def plan_subtasks(
        self,
        user_query: str,
        required_skills: List[str],
        agents: List[Dict[str, Any]],
        max_budget: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Plan subtasks based on required skills and available agents.

        Returns a list of planned subtasks with agent assignments.
        """
        subtasks = []

        for skill in required_skills:
            # Find agents with this skill
            suitable_agents = [
                agent for agent in agents
                if skill in agent.get("skills", [])
            ]

            if not suitable_agents:
                continue

            # Select best agent (lowest dynamic price, highest rating)
            best_agent = min(
                suitable_agents,
                key=lambda a: (a.get("dynamic_price", 999), -a.get("rating", 0))
            )

            subtask = {
                "agent_id": best_agent["id"],
                "skill": skill,
                "estimated_cost": best_agent.get("dynamic_price", 0.10)
            }

            subtasks.append(subtask)

        # Check if total cost exceeds max budget
        if max_budget:
            total_cost = sum(st["estimated_cost"] for st in subtasks)
            if total_cost > max_budget:
                # Try to find cheaper alternatives or return warning
                pass  # LLM will handle this

        return subtasks

    def should_negotiate(self, agent: Dict[str, Any]) -> bool:
        """Determine if price negotiation is appropriate for this agent."""
        # Negotiate with specific mock agents or high-priced agents
        negotiation_agents = ["mock_negotiator", "mock_highprice"]
        return agent["id"] in negotiation_agents or agent.get("dynamic_price", 0) > 0.50

    def create_execution_plan(
        self,
        subtasks: List[Dict[str, Any]],
        agents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Create an execution plan with proper ordering.

        In a simple implementation, this is sequential.
        For complex tasks, this would handle dependencies.
        """
        # For MVP, execute in order
        execution_plan = []

        for i, subtask in enumerate(subtasks):
            agent = next((a for a in agents if a["id"] == subtask["agent_id"]), None)
            if agent:
                execution_plan.append({
                    "step": i + 1,
                    "agent_id": subtask["agent_id"],
                    "agent_name": agent.get("name", subtask["agent_id"]),
                    "skill": subtask["skill"],
                    "estimated_cost": subtask["estimated_cost"],
                    "requires_negotiation": self.should_negotiate(agent)
                })

        return execution_plan

