Bhavain Shah
bhavain
Online

Bhavain Shah
 changed the group name: Agentic Payments Hackahon. Edit Group — 9:30 AM
Bhavain Shah — 11:01 AM
https://docs.google.com/forms/d/e/1FAIpQLSfsSg_NqQ45UpxNpevdMIXijUUnT4PcDbDkxwTGANZHrspigw/viewform
Google Docs
Agentic Payments Hackathon - Claude API Credits
*** Fill out by November 15th by 10:00am to get $100 in Claude API credits ***

We're pleased to welcome you to build with Claude - Anthropic's family of state-of-the-art models with frontier safety features, cutting-edge capabilities, with multi-modality built in from the ground up. Choose from our family of models–Opus, Sonnet, and Haiku–t...
Image
Vonface — 11:01 AM
Hey
Bhavain Shah
 added 
doodle
 to the group. — 11:01 AM
Vonface — 1:28 PM
https://docs.paywithlocus.com/getting-started
Getting Started | Locus Hackathon Docs
Getting Started | Locus Hackathon Docs
doodle — 1:48 PM
AgentBazaar
https://dashboard.stripe.com/acct_1ST20NB0uMtLyx1R/test/settings/team
Stripe track: Autonomous agentic commerce
Image
Stripe Login | Sign in to the Stripe Dashboard
Sign in to the Stripe Dashboard to manage business payments and operations in your account. Manage payments and refunds, respond to disputes and more.
Introducing apps in ChatGPT and the new Apps SDK | OpenAI
doodle — 2:00 PM
Forwarded
@everyone Hi all, hope hacking is going well!.

You MUST fill out this form before 3:30pm to register your team for judging and your specific time. This is NOT the project submission form. 
https://forms.gle/GtWrHCczP9WP3fZz9

Note: Each participant can only be a member of one team. 

Note 2: Solo hackers should still register with this form.

Note 3: Only one team member should fill this out per team. 

Note 4: This is NOT the submission form.
Google Docs
Locus Agentic Payment Hackathon Team Registration
Please register all team members using this form prior to 3pm.

Indicate tracks you plan on submitting to, team name, project name, and team members names and email addresses

Note: Each participant can only be a member of one team.

Note 2: Solo hackers should still register with this form.

Note 3: Only one team member should fill this out p...
Image

Agentic Payments Hackathon - Locus @ YC  •  1:48 PM
Vonface — 3:02 PM
Wallet : Vendors : 0xe1e1d4503105d4b0466419ff173900031e7e5ed6
Group : Vendor_Group
Agents : 

    Vendor_1 :
    Client ID : 29m6i2j6p7gfsvfup7csnbndln
    Client Secret : l9j0dhj4abnsf12vsguqcbavuqrbancra88bk7vs60u5cvidsb
    API Key (Alternative Auth) : locus_dev_mWi9iX5Thj98sx_ixdWhXpDSgji0_A9R

    Summarize :
    Client ID : 26rkc6d4301rr7g82bufc1tiv1
    Client Secret : 8rqelt5qnmb3k3hhq9o0q28f0koce3jncing88hegna6vm47lbs
    API Key (Alternative Auth) : locus_dev_9l9V7XuOYFsxDy9lLT731fPkY9WdAEX0

    Translate : 
    Client ID : 3le4cmrdaropj60f58psn23hod
    Client Secret : 130f1cdm184ufl7o8jf3t9q7v4un2iud254bep6ulnvrnu454lj2
    API Key (Alternative Auth) : locus_dev_jlpDXkiIoSB_fh0TTXx4myXLMAIcAmCO

    Research :
    Client ID : 7lic0eo18hof1o1dtrfv2ob733
    Client Secret : 16av4aahel9j34phap4io6balc2t4nu1tppo1sblgtv9vkqm6j7d
    API Key (Alternative Auth) : locus_dev_cUsp0xYzhzR-I4YH5oLZFaxVHFhNXysW




Wallet : Customer : 0xf76b5a90bfa57aee275137b4e96cbc74e3933d19
Group : Customer_Group
Agents : 

    Customer_1 :
    Client ID : 780o2t5613aorsbd89uko6crg5
    Client Secret : 12beb03bh8g6q20ekf3krm09hri8lo0bfa0c6qipq7ddv5cch0pv
    API Key (Alternative Auth) : locus_dev_iP5FvYpYL7sm5ncGRqurxWkpYqHBBIZD
Vonface — 3:22 PM
vineetkhadloya@gmail.com
Vineet@98
Arinon — 4:03 PM
hubchat/agent_registry.py
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
... (94 lines left)
Collapse
message.txt
7 KB

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
