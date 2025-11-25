from typing import List, Optional
from pydantic import BaseModel, Field


class RepoNote(BaseModel):
    content: str = Field(..., max_length=10000)
    author: Optional[str] = None


class Page(BaseModel):
    title: str = Field(..., min_length=1)
    purpose: str
    parent: Optional[str] = None
    page_notes: Optional[List[str]] = None


class CerebroConfig(BaseModel):
    repo_notes: Optional[List[RepoNote]] = None
    pages: Optional[List[Page]] = Field(None, max_length=80)  # Enterprise limit as safe default


class GenerateRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = None
