from typing import Literal
from core.models import AnalysisResult
from parsers.github_actions import GithubActionsParser
from parsers.generic import GenericParser
from parsers.gitlab_ci import GitlabCIParser
from parsers.docker_build import DockerBuildParser
from rules.patterns import classify_error, suggest_fixes

ProviderType = Literal["github", "gitlab", "docker", "azure", "terraform", "auto"]


def analyze_log(log_text: str, provider: ProviderType = "auto") -> AnalysisResult:
    # Normalize provider (simple auto-detection for now)
    normalized_provider: str

    if provider == "auto":
        lower_log = log_text.lower()

        if "github actions" in lower_log or "github.com" in lower_log:
            normalized_provider = "github"
        elif "gitlab" in lower_log or "gitlab-runner" in lower_log:
            normalized_provider = "gitlab"
        elif "failed to solve" in lower_log or "dockerfile" in lower_log or "step " in lower_log:
            normalized_provider = "docker"
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
    elif normalized_provider == "docker":
        parser = DockerBuildParser(log_text)
        provider_name = "docker_build"
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
