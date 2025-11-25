from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse
from celery.result import AsyncResult
from .config import settings
from .models import GenerateRequest
from .worker import celery_app, generate_documentation_task
import redis

app = FastAPI(title="Cerebro API", version="0.1.0")
redis_client = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB, 
    decode_responses=True
)

@app.post("/generate", status_code=202)
async def generate_docs(request: GenerateRequest):
    """
    Trigger documentation generation for a repository.
    """
    task = generate_documentation_task.delay(request.repo_url, request.branch)
    return {"task_id": task.id, "status": "processing"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    """
    Check the status of a background task.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
    }
    return result

@app.get("/{org}/{repo}")
async def preview_docs(org: str, repo: str):
    """
    Redirect to the latest generated documentation for the given repo.
    """
    key = f"{org}/{repo}"
    s3_url = redis_client.get(key)
    
    if not s3_url:
        raise HTTPException(status_code=404, detail="Documentation not found for this repository")
    
    return RedirectResponse(url=s3_url)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
