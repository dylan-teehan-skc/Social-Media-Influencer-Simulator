from PyQt6.QtCore import QObject, pyqtSignal
from src.factory.post_builder_factory import PostBuilderFactory

from src.services.logger_service import LoggerService
from src.services.sentiment_service import SentimentService


class PostController(QObject):
    # Controller for post-related operations

    # Signals
    post_created = pyqtSignal(object)  # Emitted when a post is created

    def __init__(self, user_controller, sentiment_service=None):
        # Initialize with user controller and sentiment service
        super().__init__()
        self._user_controller = user_controller
        self._sentiment_service = sentiment_service or SentimentService()
        self._logger = LoggerService.get_logger()
        self._posts = []

    def initialize(self):
        # Set up the controller
        self._logger.info("Post controller initialized")

    def create_post(self, content, image_path=None):
        # Create a new post with content and optional image
        user = self._user_controller.get_user()

        # Create post using builder factory
        post_type = "image" if image_path else "text"
        builder = PostBuilderFactory.get_builder(post_type)

        # Build post
        post = builder.set_content(content).set_author(user)

        # Set image if provided
        if image_path:
            post = post.set_image(image_path)

        # Build and finalize
        post = post.build()

        # Analyze sentiment using the sentiment service
        self._logger.info(
            f"Analyzing sentiment for new post: '{content[:30]}...'"
        )
        sentiment = self._sentiment_service.analyze(content)
        self._logger.info(f"Sentiment analysis result: {sentiment.name}")

        # Set the sentiment directly
        post.sentiment = sentiment

        # Add to posts list
        self._posts.insert(0, post)

        # Track initial follower count
        initial_followers = user.follower_count
        self._logger.info(f"Initial follower count: {initial_followers}")

        # Notify all followers about the new post
        user.notify_followers(post)
        self._logger.info(
            f"Notified {len(user.followers)} followers about new post"
        )

        # Update reputation based on follower losses
        lost_followers = user.update_reputation(initial_followers, post)
        if lost_followers > 0:
            self._logger.warning(
                f"Lost {lost_followers} followers due to post"
            )

        # Emit signal
        self.post_created.emit(post)

        # Log
        self._logger.info(
            f"Post created by {
                user.handle} with sentiment {
                post.sentiment.name}"
        )

        return post, initial_followers

    def get_posts(self):
        # Return a copy of all posts
        return self._posts.copy()

    def add_comment(self, post, comment):
        # Add a comment to a post
        post.add_comment(comment)
        self._logger.debug(f"Comment added to post: {comment.content[:30]}...")

    def like_post(self, post):
        # Increment post likes
        post.like()
        self._logger.debug(f"Post liked, total likes: {post.likes}")

    def unlike_post(self, post):
        # Decrement post likes
        post.unlike()
        self._logger.debug(f"Post unliked, total likes: {post.likes}")

    def share_post(self, post):
        # Increment post shares
        post.share()
        self._logger.debug(f"Post shared, total shares: {post.shares}")

    def unshare_post(self, post):
        # Decrement post shares
        post.unshare()
        self._logger.debug(f"Post unshared, total shares: {post.shares}")
