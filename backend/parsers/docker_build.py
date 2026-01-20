from typing import Optional
from .base import BaseParser


class DockerBuildParser(BaseParser):
    provider_name = "docker_build"

    def detect_failed_command(self) -> Optional[str]:
        lines = self.log_text.splitlines()

        for line in reversed(lines):
            s = line.strip()

            # BuildKit style: "#5 [4/5] RUN <cmd>"
            if "] RUN " in s:
                return s.split("] RUN ", 1)[1].strip()

            # Classic docker build: "Step X/Y : RUN <cmd>"
            if s.startswith("Step ") and " : RUN " in s:
                return s.split(" : RUN ", 1)[1].strip()

            # Plain: "RUN <cmd>"
            if s.startswith("RUN "):
                return s[4:].strip()

        return None
