from src.controllers.follower_controller import FollowerController
from src.controllers.post_controller import PostController
from src.controllers.user_controller import UserController
from src.models.user import User
from src.services.company_service import CompanyService
from src.views.main_window import SocialMediaMainWindow


class MainController:

    # Main controller for the application
    _instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __init__(self):
        # Set the singleton instance
        MainController._instance = self

        self.user = User("default_user", "Default bio")

        # Create controllers
        self.user_controller = UserController(self.user)
        self.post_controller = PostController()
        self.follower_controller = FollowerController()

        # Initialize the company service
        self.company_service = CompanyService.get_instance()

        # Initialise UI
        self.init_ui()

        # Generate some initial followers
        self._generate_initial_followers()

    def init_ui(self):
        self.main_window = SocialMediaMainWindow(self.user)

        # Set controllers in the main window
        self.main_window.set_user_controller(self.user_controller)
        self.main_window.set_post_controller(self.post_controller)

    def _generate_initial_followers(self, count=10):
        # Create a batch of followers with balanced distribution
        followers = self.follower_controller.create_followers_batch(count)

        # Add them to the user
        for follower in followers:
            self.user_controller.add_follower(follower)

        return len(followers)

    def get_all_posts(self):
        posts = []

        # Get posts from the main user
        if hasattr(self.user, "_posts"):
            posts.extend(self.user._posts)

        # Get posts from followers
        if hasattr(self.user, "_followers"):
            for follower in self.user._followers:
                if hasattr(follower, "_posts"):
                    posts.extend(follower._posts)

        return posts
