from typing import Optional
from .base import BaseParser


class GitlabCIParser(BaseParser):
    """
    Simple GitLab CI log parser.

    It tries to:
    - detect a failed command: lines starting with '$ ' or 'Running '
    - detect a primary error: lines starting with 'ERROR:' or 'FATAL:'
    """

    provider_name = "gitlab_ci"

    def parse(self, log_text: str) -> dict:
        lines = log_text.splitlines()

        failed_command: Optional[str] = None
        primary_error: Optional[str] = None

        # primary error
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("ERROR:") or stripped.startswith("FATAL:"):
                primary_error = stripped
                break
            if "Job failed" in stripped or "job failed" in stripped.lower():
                if primary_error is None:
                    primary_error = stripped

        # failed command – look from the bottom up
        for line in reversed(lines):
            stripped = line.strip()
            if stripped.startswith("$ "):
                failed_command = stripped[2:].strip()
                break
            if stripped.startswith("Running "):
                failed_command = stripped
                break

        return {
            "provider": self.provider_name,
            "failed_command": failed_command,
            "primary_error": primary_error,
        }
