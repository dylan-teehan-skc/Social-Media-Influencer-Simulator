from abc import ABC, abstractmethod
from src.services.logger_service import LoggerService

class EngagementCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

class LikeCommand(EngagementCommand):
    def __init__(self, user, post):
        self.user = user
        self.post = post

    def execute(self) -> None:
        logger = LoggerService.get_logger()
        logger.debug(f"User {self.user} liked post from {self.post}")
        # When posts are implemented, add the user to the post's likes list

    def undo(self) -> None:
        logger = LoggerService.get_logger()
        logger.debug(f"User {self.user} unliked post from {self.post}")
        # When posts are implemented, remove the user from the post's likes list



