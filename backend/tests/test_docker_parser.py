from core.analyzer import analyze_log


def test_docker_dependency_error():
    log = """
#5 [4/5] RUN pip install -r requirements.txt
ERROR: Could not find a version that satisfies the requirement nonexistinglib==1.0
ERROR: No matching distribution found for nonexistinglib==1.0
failed to solve: process "/bin/sh -c pip install -r requirements.txt" did not complete successfully: exit code: 1
    """

    result = analyze_log(log, provider="docker")

    assert result.error_category == "dependency_error"
    assert "nonexistinglib" in (result.primary_error or "")
    assert "pip install -r requirements.txt" in (result.failed_command or "")
    assert result.confidence > 0.5
