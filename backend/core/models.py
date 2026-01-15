from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzeRequest(BaseModel):
    log_text: str = Field(..., description="Raw CI/CD log output")
    provider: Optional[str] = Field(
        default="auto",
        description="CI provider: github, gitlab, circleci, auto",
    )


class AnalysisResult(BaseModel):
    provider: str
    error_category: str
    primary_error: str
    failed_command: Optional[str] = None
    summary: str
    suggested_fixes: List[str]
    confidence: float
