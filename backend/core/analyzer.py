from typing import Literal
from core.models import AnalysisResult
from parsers.github_actions import GithubActionsParser
from parsers.generic import GenericParser
from parsers.gitlab_ci import GitlabCIParser 
from rules.patterns import classify_error, suggest_fixes



ProviderType = Literal["github", "gitlab", "azure", "docker", "terraform", "auto"]


def analyze_log(log_text: str, provider: ProviderType = "auto") -> AnalysisResult:
    # Normalize provider (simple auto-detection for now)
    normalized_provider: str

    if provider == "auto":
        lower_log = log_text.lower()
        if "github actions" in lower_log or "github.com" in lower_log:
            normalized_provider = "github"
        elif "gitlab" in lower_log or "gitlab-runner" in lower_log:
            normalized_provider = "gitlab"
        else:
            normalized_provider = "generic"
    else:
        normalized_provider = provider

    # Choose parser based on normalized provider
    if normalized_provider == "github":
        parser = GithubActionsParser(log_text)
        provider_name = "github_actions"
    elif normalized_provider == "gitlab":
        parser = GitlabCIParser(log_text)
        provider_name = "gitlab_ci"
    else:
        parser = GenericParser(log_text)
        provider_name = "generic"

    # Classify error and build explanation
    category, primary_error = classify_error(log_text)
    summary, suggestions, confidence = suggest_fixes(category, primary_error)

    # Ask parser for failed command (if any)
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
