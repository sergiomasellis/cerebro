import os
import asyncio
import logging
import shutil
import subprocess
import redis
from celery import Celery
from .config import settings
from .graph import create_docs_agent
from .state import AgentState
from .s3_utils import upload_directory_to_s3
from typing import cast

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cerebro.worker")

celery_app = Celery(
    "cerebro",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

redis_client = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB, 
    decode_responses=True
)

async def run_agent(repo_url: str, branch: str = None):
    agent = create_docs_agent()
    initial_state = cast(AgentState, {"repo_url": repo_url})
    if branch:
        initial_state["branch_name"] = branch
    
    logger.info(f"Starting agent for {repo_url}...")
    result = await agent.ainvoke(initial_state)
    logger.info("Agent finished.")
    return result

@celery_app.task(bind=True)
def generate_documentation_task(self, repo_url: str, branch: str = None):
    """
    Background task to generate documentation, build it, and upload to S3.
    """
    try:
        # 1. Run the agent
        # Since Celery runs in a sync loop, we need to run the async agent
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # We need to run this in a way that works with Celery
        # For simplicity in this context, using asyncio.run or loop.run_until_complete
        # Note: In a production worker, might need better async handling or asgiref
        try:
            result = loop.run_until_complete(run_agent(repo_url, branch))
        except RuntimeError:
             # If loop is already running (e.g. gevent), use it
             result = asyncio.run(run_agent(repo_url, branch))

        # Extract run_id and repo info from result
        # The agent returns the final state.
        # We need to find where the docs were generated.
        # Based on nodes.py: write_files uses generated-docs/{run_id}/{repo_full_name}
        
        # We can't easily get the state back from ainvoke if it returns a complex object
        # But we can infer the path if we had the run_id. 
        # Wait, nodes.py generates a run_id inside clone_node. 
        # We might need to modify nodes.py to accept a run_id or return it more explicitly.
        # For now, let's assume we can find the latest folder or we modify nodes.py to return the path.
        
        # Actually, let's look at how we can get the path. 
        # The agent returns the final state dict.
        final_state = result
        run_id = final_state.get("run_id")
        repo_name = final_state.get("repo_name")
        
        # Reconstruct path
        repo_url_parts = repo_url.rstrip("/").split("/")
        if len(repo_url_parts) > 1:
            repo_full_name = f"{repo_url_parts[-2]}/{repo_url_parts[-1]}".replace(".git", "")
        else:
            repo_full_name = repo_name
            
        base_output_dir = os.path.join("generated-docs", run_id, repo_full_name)
        
        if not os.path.exists(base_output_dir):
            raise Exception(f"Output directory not found: {base_output_dir}")

        # 2. Build with MkDocs
        logger.info(f"Building documentation in {base_output_dir}...")
        # We need to run `uv mkdocs build` inside that directory or pointing to it.
        # The mkdocs.yml is in base_output_dir.
        
        # We can run `mkdocs build` directly if installed, or `uv run mkdocs build`
        # Assuming we are in the worker container which has dependencies installed.
        cmd = ["mkdocs", "build", "-f", os.path.join(base_output_dir, "mkdocs.yml")]
        subprocess.run(cmd, check=True, capture_output=True)
        
        site_dir = os.path.join(base_output_dir, "site")
        if not os.path.exists(site_dir):
            raise Exception("MkDocs build failed to create site directory")

        # 3. Upload to S3
        if settings.S3_BUCKET_NAME:
            logger.info("Uploading to S3...")
            # Construct prefix: org/repo/branch (or default)
            # We need org/repo.
            org_repo = repo_full_name # already org/repo format usually
            target_branch = branch or "default"
            s3_prefix = f"{org_repo}/{target_branch}"
            
            s3_url = upload_directory_to_s3(site_dir, settings.S3_BUCKET_NAME, s3_prefix)
            
            # 4. Update Redis for Preview
            if s3_url:
                redis_key = org_repo
                redis_client.set(redis_key, s3_url)
                logger.info(f"Updated Redis key {redis_key} -> {s3_url}")
                
            return {"status": "success", "s3_url": s3_url, "run_id": run_id}
        else:
            logger.info("S3_BUCKET_NAME not set, skipping upload.")
            return {"status": "success", "run_id": run_id, "message": "S3 upload skipped"}

    except Exception as e:
        logger.error(f"Task failed: {e}")
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise e
