from src.models.post import Post
from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.services.logger_service import LoggerService


class SpamFilter(ContentInterceptor):
    # Filter that detects and flags spam content in posts
    
    def __init__(self):
        # Initialize with spam detection phrases
        self.logger = LoggerService.get_logger()
        self.promotional_phrases = [
            "buy now",
            "limited time offer",
            "discount code",
            "click here",
            "act now",
            "special offer",
            "free gift",
            "exclusive deal",
            "best price",
            "money back guarantee",
        ]
        self.logger.debug("SpamFilter initialized")

    def intercept(self, post):
        # Check post content for spam indicators
        content = post.content.lower()
        detected_phrases = []

        # Check for promotional phrases
        for phrase in self.promotional_phrases:
            if phrase in content:
                detected_phrases.append(phrase)

        # If spam is detected, mark the post and return a warning
        if detected_phrases:
            post.is_spam = True
            warning_msg = f"Potential spam detected: Your post contains promotional phrases ({', '.join(detected_phrases)})"
            
            self.logger.warning(
                f"SpamFilter: Spam content detected in post: {post.content[:50]}..."
            )
            
            return False, warning_msg
        
        return True, None
