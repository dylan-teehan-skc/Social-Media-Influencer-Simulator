from src.models.post import Post
from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.services.logger_service import LoggerService


class PostCreationInterceptor(ContentInterceptor):
    def __init__(self):
        self.logger = LoggerService.get_logger()

    def intercept(self, post: Post) -> None:
        """
        Intercept post creation to perform validation and processing.
        This method is called during post creation to validate and process the post.

        Args:
            post: The post being created
        """
        self.logger.info(
            f"PostCreationInterceptor: Processing post creation: {post.content[:30]}..."
        )

        # Check for empty content
        if not post.content or post.content.strip() == "":
            post.is_valid = False

            # Create warning message
            warning_msg = "Empty post: Your post doesn't contain any content"

            # Add warning to dispatcher if available
            if hasattr(post, "_dispatcher") and post._dispatcher:
                post._dispatcher.add_warning(warning_msg)

            self.logger.warning(
                "PostCreationInterceptor: Empty post content detected"
            )
            return

        # Check for minimum content length
        if len(post.content) < 5:
            post.is_valid = False

            # Create warning message
            warning_msg = f"Post too short: Your post is only {
                len(
                    post.content)} characters long (minimum 5 characters)"

            # Add warning to dispatcher if available
            if hasattr(post, "_dispatcher") and post._dispatcher:
                post._dispatcher.add_warning(warning_msg)

            self.logger.warning(
                f"PostCreationInterceptor: Post content too short: {len(post.content)} chars"
            )
            return

        # Check for maximum content length
        if len(post.content) > 500:
            post.is_valid = False

            # Create warning message
            warning_msg = f"Post too long: Your post is {
                len(
                    post.content)} characters long (maximum 500 characters)"

            # Add warning to dispatcher if available
            if hasattr(post, "_dispatcher") and post._dispatcher:
                post._dispatcher.add_warning(warning_msg)

            self.logger.warning(
                f"PostCreationInterceptor: Post content too long: {len(post.content)} chars"
            )
            return

        # If all checks pass, mark the post as valid
        post.is_valid = True
        self.logger.info("PostCreationInterceptor: Post validation successful")
