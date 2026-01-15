import re
from typing import Optional, Tuple

# Simple patterns for common errors
PYTHON_MODULE_NOT_FOUND = re.compile(r"ModuleNotFoundError: No module named '(.+?)'")
NPM_NOT_FOUND = re.compile(r"Error: Cannot find module '(.+?)'")
PIP_ERROR = re.compile(r"ERROR: Could not find a version that satisfies the requirement (.+)")
TEST_FAIL = re.compile(r"(FAIL|AssertionError|expected .* but got)")
DOCKER_BUILD_ERROR = re.compile(r"error:.*(docker build|failed to solve with frontend dockerfile)")
AUTH_ERROR = re.compile(r"(Permission denied|Authentication failed|access denied)")


def classify_error(log_text: str) -> Tuple[str, str]:
    """
    Returns (category, primary_error_line)
    """
    lines = log_text.splitlines()
    last_error_line = ""
    # walk from bottom up, pick the first "error-ish" line
    for line in reversed(lines):
        if any(k in line.lower() for k in ["error", "fail", "exception", "traceback"]):
            last_error_line = line.strip()
            break

    text = log_text  # for regex

    # Dependency-related
    if m := PYTHON_MODULE_NOT_FOUND.search(text):
        return "dependency_error", f"ModuleNotFoundError: No module named '{m.group(1)}'"
    if m := PIP_ERROR.search(text):
        return "dependency_error", f"Missing or incompatible dependency: {m.group(1)}"
    if m := NPM_NOT_FOUND.search(text):
        return "dependency_error", f"Cannot find NPM module '{m.group(1)}'"

    # Test failures
    if TEST_FAIL.search(text):
        return "test_failure", last_error_line or "Test(s) failed."

    # Docker build
    if DOCKER_BUILD_ERROR.search(text):
        return "docker_build_error", last_error_line or "Docker build failed."

    # Auth
    if AUTH_ERROR.search(text):
        return "auth_error", last_error_line or "Authentication or permission error."

    # Fallback
    return "unknown", last_error_line or "Unknown error – unable to classify."


def suggest_fixes(category: str, primary_error: str) -> Tuple[str, list, float]:
    """
    Returns (summary, suggestions_list, confidence)
    """
    suggestions = []
    confidence = 0.5
    summary = f"Pipeline failed with category '{category}'."

    if category == "dependency_error":
        confidence = 0.9
        summary = (
            "The pipeline failed due to a missing or incompatible dependency."
        )
        if "ModuleNotFoundError" in primary_error:
            mod_name = primary_error.split("'")[-2]
            suggestions.append(
                f"Add '{mod_name}' to your dependency file (e.g. requirements.txt, package.json) "
                "and ensure the install step runs before this command."
            )
        suggestions.append(
            "Check that your dependency installation step (pip install / npm install) is not failing earlier in the logs."
        )

    elif category == "test_failure":
        confidence = 0.8
        summary = "The pipeline failed because one or more tests failed."
        suggestions.extend(
            [
                "Run the failing test suite locally to reproduce the error.",
                "Check expected vs actual values in the failing test and adjust the code or test accordingly.",
            ]
        )

    elif category == "docker_build_error":
        confidence = 0.75
        summary = "Docker build failed during the CI pipeline."
        suggestions.extend(
            [
                "Check the Dockerfile for invalid commands or missing files in COPY/ADD steps.",
                "Build the Docker image locally with the same command to reproduce the error.",
            ]
        )

    elif category == "auth_error":
        confidence = 0.75
        summary = "The pipeline failed due to an authentication or permission issue."
        suggestions.extend(
            [
                "Check that the CI has valid credentials/secrets configured (tokens, SSH keys).",
                "Verify that the token has sufficient permissions for the operation (e.g. repo write, registry push).",
            ]
        )

    else:
        suggestions.append(
            "Inspect the last 20–30 lines of the log for more detailed error messages."
        )

    return summary, suggestions, confidence
