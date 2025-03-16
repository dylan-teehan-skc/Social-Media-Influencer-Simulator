from src.models.post import Post
from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.services.logger_service import LoggerService


class InappropriateContentFilter(ContentInterceptor):
    def __init__(self):
        self.logger = LoggerService.get_logger()
        # List of inappropriate words/phrases to filter
        self.inappropriate_words = [
            "offensive",
            "explicit",
            "hate speech",
            "slur",
            "profanity",
            "violent content",
            "harassment",
            "discrimination",
        ]

    def intercept(self, post: Post) -> None:
        """
        Check if the post contains inappropriate content.

        Args:
            post: The post to check
        """
        content_lower = post.content.lower()

        # Check for inappropriate content
        detected_words = []
        for word in self.inappropriate_words:
            if word in content_lower:
                detected_words.append(word)

        if detected_words:
            # Mark post as invalid
            post.is_valid = False

            # Create warning message
            warning_msg = f"Inappropriate content detected: Your post contains potentially inappropriate content ({
                ', '.join(detected_words)})"

            # Add warning to dispatcher if available
            if hasattr(post, "_dispatcher") and post._dispatcher:
                post._dispatcher.add_warning(warning_msg)

            self.logger.warning(
                f"InappropriateContentFilter: Inappropriate content detected: '{
                    ', '.join(detected_words)}'"
            )
        else:
            self.logger.info(
                "InappropriateContentFilter: No inappropriate content detected"
            )
