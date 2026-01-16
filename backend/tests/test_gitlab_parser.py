from core.analyzer import analyze_log


def test_gitlab_dependency_error():
    log = """
Running with gitlab-runner 16.0.2
  on docker-auto-scale xyz123
Using Docker executor with image python:3.11-slim ...

$ pip install -r requirements.txt
Collecting requests
ERROR: Could not find a version that satisfies the requirement totallynonexistent==1.0 (from versions: none)
ERROR: No matching distribution found for totallynonexistent==1.0
Cleaning up project directory and file based variables
ERROR: Job failed: exit code 1
    """

    result = analyze_log(log, provider="gitlab")

    assert result.error_category == "dependency_error"
    assert "totallynonexistent" in (result.primary_error or "")
    assert "pip install -r requirements.txt" in (result.failed_command or "")
    assert result.confidence > 0.5
