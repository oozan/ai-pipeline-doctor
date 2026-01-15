from typing import Literal
from core.models import AnalysisResult
from parsers.github_actions import GithubActionsParser
from parsers.generic import GenericParser
from rules.patterns import classify_error, suggest_fixes


ProviderType = Literal["github", "gitlab", "circleci", "auto"]


def analyze_log(log_text: str, provider: ProviderType = "auto") -> AnalysisResult:
    # For now, provider auto-detection is simple
    normalized_provider = provider
    if provider == "auto":
        if "GitHub Actions" in log_text or "github.com" in log_text:
            normalized_provider = "github"
        else:
            normalized_provider = "generic"

    if normalized_provider == "github":
        parser = GithubActionsParser(log_text)
        provider_name = "github_actions"
    else:
        parser = GenericParser(log_text)
        provider_name = "generic"

    category, primary_error = classify_error(log_text)
    summary, suggestions, confidence = suggest_fixes(category, primary_error)
    failed_cmd = parser.detect_failed_command()

    return AnalysisResult(
        provider=provider_name,
        error_category=category,
        primary_error=primary_error,
        failed_command=failed_cmd,
        summary=summary,
        suggested_fixes=suggestions,
        confidence=confidence,
    )
