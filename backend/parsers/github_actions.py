from .base import BaseLogParser


class GithubActionsParser(BaseLogParser):
    def detect_failed_command(self):
        """
        Very rough heuristic: look for lines like:
        'Run <command>'
        followed by an 'Error' later.
        """
        lines = self.log_text.splitlines()
        last_run_cmd = None

        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("Run "):
                last_run_cmd = line_stripped.replace("Run ", "", 1)

        return last_run_cmd
