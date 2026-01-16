from typing import Optional
from .base import BaseParser


class GitlabCIParser(BaseParser):
    provider_name = "gitlab_ci"

    def detect_failed_command(self) -> Optional[str]:
        lines = self.log_text.splitlines()

        for line in reversed(lines):
            stripped = line.strip()
            if stripped.startswith("$ "):
                return stripped[2:].strip()
        return None
