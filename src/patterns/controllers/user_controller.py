from PyQt6.QtCore import QObject

from src.services.logger_service import LoggerService


class UserController(QObject):
    # Controller for user-related operations

    def __init__(self, user_model):
        # Initialize with user model
        super().__init__()
        self._user = user_model
        self._logger = LoggerService.get_logger()

    def initialize(self):
        # Set up the controller
        self._logger.info(
            f"User controller initialized for user: {self._user.handle}"
        )

    def update_reputation(self, current_time):
        # Update user reputation based on time
        self._user.update_reputation_recovery(current_time)

    def get_user(self):
        # Return the user model
        return self._user

    def get_follower_count(self):
        # Return the user's follower count
        return self._user.follower_count

    def get_posts(self):
        # Return the user's posts
        return self._user.posts
