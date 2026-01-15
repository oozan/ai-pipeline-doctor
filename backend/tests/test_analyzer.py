from core.analyzer import analyze_log


def test_dependency_error():
    log = """
    Run pip install -r requirements.txt
    Collecting requests
    ERROR: Could not find a version that satisfies the requirement nonexistinglib==1.0 (from versions: none)
    ERROR: No matching distribution found for nonexistinglib==1.0
    Error: Process completed with exit code 1.
    """
    result = analyze_log(log, provider="github")
    assert result.error_category == "dependency_error"
    assert "nonexistinglib" in result.primary_error
    assert result.failed_command == "pip install -r requirements.txt"
    assert result.confidence > 0.5


def test_test_failure():
    log = """
    Run pytest
    =================================== FAILURES ===================================
    def test_addition():
        assert 1 + 1 == 3
    E       assert 2 == 3
    Error: Process completed with exit code 1.
    """
    result = analyze_log(log, provider="github")

    assert result.error_category == "test_failure"
    # primary_error is the last error-ish line
    assert "exit code 1" in result.primary_error
    # summary text proves it recognized a test failure
    assert "tests failed" in result.summary.lower()
