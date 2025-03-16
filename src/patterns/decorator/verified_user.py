from src.patterns.interfaces.user_decorator import UserDecorator


class VerifiedUser(UserDecorator):
    def get_handle(self) -> str:
        # Add verification checkmark to user handle
        return f"{self._user.handle} ✔️"

    def get_bio(self) -> str:
        return f"{self._user.bio} (Verified)"

    @property
    def follower_count(self):
        # Forward follower_count to the decorated user
        return self._user.follower_count

    @property
    def followers(self):
        # Forward followers to the decorated user
        return self._user.followers

    @property
    def posts(self):
        # Forward posts to the decorated user
        return self._user.posts

    @property
    def recent_follower_losses(self):
        # Forward recent_follower_losses to the decorated user
        return self._user.recent_follower_losses

    # Forward signals
    @property
    def follower_added(self):
        return self._user.follower_added

    @property
    def follower_removed(self):
        return self._user.follower_removed

    @property
    def post_created(self):
        return self._user.post_created

    @property
    def reputation_changed(self):
        return self._user.reputation_changed

    # Forward methods
    def add_follower(self, follower, post=None):
        return self._user.add_follower(follower, post)

    def remove_follower(self, follower):
        return self._user.remove_follower(follower)

    def create_post(self, content, image_path=None):
        return self._user.create_post(content, image_path)

    def attach(self, observer, post=None):
        return self._user.attach(observer, post)

    def detach(self, observer):
        return self._user.detach(observer)

    def notify(self, post=None):
        return self._user.notify(post)

    def update_reputation_recovery(self, current_time):
        return self._user.update_reputation_recovery(current_time)

    def __getattr__(self, name):
        # Forward any attribute access to the wrapped user
        return getattr(self._user, name)
