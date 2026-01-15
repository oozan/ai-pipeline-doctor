from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.models import AnalyzeRequest, AnalysisResult
from core.analyzer import analyze_log

app = FastAPI(
    title="AI Pipeline Doctor",
    description="Analyze CI/CD logs and suggest likely root causes and fixes.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze", response_model=AnalysisResult)
def analyze(request: AnalyzeRequest):
    """
    Analyze a CI/CD log and return an estimated category + suggestions.
    """
    result = analyze_log(request.log_text, request.provider)  # type: ignore
    return result
