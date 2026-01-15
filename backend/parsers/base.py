from typing import Optional


class BaseLogParser:
    def __init__(self, log_text: str):
        self.log_text = log_text

    def detect_failed_command(self) -> Optional[str]:
        """
        Override in subclasses. Try to extract the shell command that failed.
        """
        return None
