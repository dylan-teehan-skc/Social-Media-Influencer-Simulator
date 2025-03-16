from PyQt6.QtCore import QObject

from src.services.logger_service import LoggerService


class UserController(QObject):
    """Controller for user-related operations."""

    def __init__(self, user_model):
        """Initialize the user controller with a user model."""
        super().__init__()
        self._user = user_model
        self._logger = LoggerService.get_logger()

    def initialize(self):
        """Initialize the user controller."""
        self._logger.info(
            f"User controller initialized for user: {self._user.handle}"
        )

    def update_reputation(self, current_time):
        """Update user reputation."""
        self._user.update_reputation_recovery(current_time)

    def get_user(self):
        """Get the user model."""
        return self._user

    def get_follower_count(self):
        """Get the user's follower count."""
        return self._user.follower_count

    def get_posts(self):
        """Get the user's posts."""
        return self._user.posts
