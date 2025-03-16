from src.patterns.interfaces.command import Command
from src.services.logger_service import LoggerService


class CommandHistory:
    """Class for managing command history."""

    def __init__(self):
        """Initialize command history."""
        self.history = []
        self.logger = LoggerService.get_logger()
        self.logger.debug("Command history initialized")

    def push(self, command: Command) -> None:
        """Add a command to the history after execution."""
        self.history.append(command)
        self.logger.debug(
            f"Command added to history, total commands: {len(self.history)}"
        )

    def clear(self) -> None:
        """Clear the command history."""
        self.history.clear()
        self.logger.debug("Command history cleared")
