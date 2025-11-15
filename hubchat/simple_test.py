"""
Simple HubChat test - Just one example to verify it works
"""

import asyncio
import os
import logging
from orchestrator import process_request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not set")
        return

    print("🤖 Testing HubChat Orchestrator...\n")

    logger.info("Starting test request...")
    logger.info("Query: Translate 'Hello, how are you?' to Spanish")
    logger.info("Max budget: $0.50")

    # Simple test: Ask HubChat to translate something
    logger.info("Calling process_request()...")
    result = await process_request(
        user_query="Translate 'Hello, how are you?' to Spanish",
        max_budget=0.50
    )
    logger.info("process_request() returned")

    print("=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(f"Success: {result['success']}")
    print(f"\nOutput:\n{result['output']}")
    print(f"\nCost: ${result['cost_breakdown']['total_cost']:.2f}")
    print(f"\nAgents Used: {result['agents_used']}")
    print("=" * 60)


if __name__ == "__main__":
    print("Make sure agents are running: ./start_all_services.sh\n")
    asyncio.run(main())

