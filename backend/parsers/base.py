from __future__ import annotations
from typing import Optional


class BaseParser:
    """
    Minimal base parser class.

    It stores the raw log text and exposes a common interface for
    detecting the failed command. Subclasses can override methods
    as needed.
    """

    def __init__(self, log_text: str) -> None:
        self.log_text = log_text

    def detect_failed_command(self) -> Optional[str]:
        """
        Default implementation: subclasses should override.
        """
        return None


# Backwards-compatible name for existing parsers
class BaseLogParser(BaseParser):
    """
    Alias for BaseParser for older parsers expecting BaseLogParser.
    """
    pass
