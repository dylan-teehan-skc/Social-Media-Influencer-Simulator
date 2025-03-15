from src.models.user import User
from src.views.main_window import SocialMediaMainWindow
from src.controllers.user_controller import UserController
from src.controllers.post_controller import PostController
from src.controllers.follower_controller import FollowerController
from src.services.company_service import CompanyService
from PyQt6.QtWidgets import QVBoxLayout

class MainController:
    """Main controller for the application."""
    
    # Singleton instance
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the MainController."""
        return cls._instance
    
    def __init__(self):
        """Initialize the main controller."""
        # Set the singleton instance
        MainController._instance = self
        
        # Create a user model
        self.user = User("default_user", "Default bio")
        
        # Create controllers
        self.user_controller = UserController(self.user)
        self.post_controller = PostController()
        self.follower_controller = FollowerController()
        
        # Initialize the company service (this will create the default companies)
        self.company_service = CompanyService.get_instance()
        
        # Initialize the UI
        self.init_ui()
        
        # Generate some initial followers
        self._generate_initial_followers()
        
    def init_ui(self):
        """Initialize the UI."""
        # Create the main window and pass the user model
        self.main_window = SocialMediaMainWindow(self.user)
        
        # Set controllers in the main window
        self.main_window.set_user_controller(self.user_controller)
        self.main_window.set_post_controller(self.post_controller)
        
    def _generate_initial_followers(self, count=10):
        """Generate some initial followers for the user."""
        # Create a batch of followers with balanced distribution
        followers = self.follower_controller.create_followers_batch(count)
        
        # Add them to the user
        for follower in followers:
            self.user_controller.add_follower(follower)
            
        return len(followers)
        
    def get_all_posts(self):
        """Get all posts from the user and their followers."""
        posts = []
        
        # Get posts from the main user
        if hasattr(self.user, '_posts'):
            posts.extend(self.user._posts)
            
        # Get posts from followers
        if hasattr(self.user, '_followers'):
            for follower in self.user._followers:
                if hasattr(follower, '_posts'):
                    posts.extend(follower._posts)
                    
        return posts

