import argparse
import asyncio
from typing import cast
from dotenv import load_dotenv
from src.graph import create_docs_agent
from src.logger import setup_logger
from src.state import AgentState

# Load environment variables from .env file
load_dotenv()

logger = setup_logger()


async def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation for a GitHub repository."
    )
    parser.add_argument("repo_url", help="GitHub repository URL")
    parser.add_argument(
        "--branch", "-b", help="Specific branch to clone (default: repository default)"
    )
    args = parser.parse_args()

    repo_url = args.repo_url
    branch = args.branch

    if not repo_url:
        logger.error("No repository URL provided.")
        print("Please provide a repository URL.")
        print("Example: uv run main.py https://github.com/username/repo")
        print(
            "Example with branch: uv run main.py https://github.com/username/repo --branch develop"
        )
        return

    logger.info(
        f"Starting documentation agent for: {repo_url} (branch: {branch or 'default'})"
    )

    try:
        agent = create_docs_agent()
        # Initialize state
        initial_state = cast(AgentState, {"repo_url": repo_url})
        if branch:
            initial_state["branch_name"] = branch

        # Run the graph
        logger.info("Invoking agent workflow...")
        await agent.ainvoke(initial_state)

        logger.info("Workflow completed successfully.")

    except Exception as e:
        logger.error(f"Error running agent: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
