from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal

from src.services.logger_service import LoggerService


class User(QObject):
    # User model representing a social media account

    # Signals
    follower_added = pyqtSignal(object)  # when a follower is added
    follower_removed = pyqtSignal(object)  # when a follower is removed
    post_created = pyqtSignal(object)  # when a post is created
    reputation_changed = pyqtSignal(int)  # when reputation changes

    # Reputation constants
    REPUTATION_RECOVERY_DELAY = 60000
    MAX_REPUTATION_PENALTY = 0.5
    REPUTATION_PENALTY_PER_LOSS = 0.1
    REPUTATION_WARNING_THRESHOLD = 5

    # Follower gain constants
    BASE_NEUTRAL_CHANCE = 20
    HOT_TAKE_CHANCE = 30
    MAX_FOLLOWER_MULTIPLIER = 3.0
    FOLLOWER_MULTIPLIER_SCALE = 1000

    # Verification constants
    VERIFICATION_THRESHOLD = 40  # Number of followers needed for verification

    def __init__(self, handle, bio):
        """Initialize a user with handle and bio."""
        super().__init__()
        self._handle = handle
        self._bio = bio
        self._followers = []
        self._posts = []
        self._follower_count = 0
        self._recent_follower_losses = 0
        self._last_reputation_check = (
            datetime.now().timestamp() * 1000
        )  # Convert to milliseconds
        self._profile_picture_path = None  # Default profile picture path
        self.logger = LoggerService.get_logger()
        self._observers = []  # For the Subject pattern

    @property
    def handle(self):
        return self._handle

    @handle.setter
    def handle(self, value):
        self._handle = value

    @property
    def bio(self):
        return self._bio

    @bio.setter
    def bio(self, value):
        self._bio = value

    @property
    def profile_picture_path(self):
        return self._profile_picture_path

    @profile_picture_path.setter
    def profile_picture_path(self, value):
        self._profile_picture_path = value

    @property
    def followers(self):
        return self._followers.copy()

    @property
    def follower_count(self):
        return self._follower_count

    @property
    def posts(self):
        return self._posts.copy()

    @property
    def recent_follower_losses(self):
        return self._recent_follower_losses

    # Subject pattern methods (implemented directly instead of inheriting)

    def attach(self, observer, post=None):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, post=None):
        for observer in self._observers:
            observer.update(self, post)

    # notify_followers method has been moved to UserController
