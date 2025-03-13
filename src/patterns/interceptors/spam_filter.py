from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.models.post import Post
from src.services.logger_service import LoggerService


class SpamFilter(ContentInterceptor):
    def __init__(self):
        self.logger = LoggerService.get_logger()
        
    def intercept(self, post: Post) -> None:
        """
        Check if the post contains spam content.
        
        Args:
            post: The post to check
        """
        spam_keywords = ["buy now", "free", "click here", "limited time offer"]
        
        # Check for spam content
        detected_keywords = []
        for keyword in spam_keywords:
            if keyword in post.content.lower():
                detected_keywords.append(keyword)
                
        if detected_keywords:
            # Mark as spam
            post.is_spam = True
            
            # Create warning message
            warning_msg = f"Potential spam detected: Your post contains promotional phrases ({', '.join(detected_keywords)})"
            
            # Add warning to dispatcher if available
            if hasattr(post, '_dispatcher') and post._dispatcher:
                post._dispatcher.add_warning(warning_msg)
                
            self.logger.warning(f"SpamFilter: Spam content detected in post: {', '.join(detected_keywords)}")
        else:
            post.is_spam = False  # Mark as not spam
            self.logger.info("SpamFilter: No spam content detected")
