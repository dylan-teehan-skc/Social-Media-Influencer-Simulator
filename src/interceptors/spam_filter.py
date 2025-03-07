from src.interfaces.content_interceptor import ContentInterceptor
from src.models.post import Post


class SpamFilter(ContentInterceptor):
    """
    SpamFilter class responsible for filtering out spam posts.
    """
    def intercept(self, post: Post) -> None:
        spam_keywords = ["buy now", "free", "click here", "limited time offer"]
        if any(keyword in post.content.lower() for keyword in spam_keywords):
            post.is_spam = True  # Assuming Post has an is_spam attribute
        else:
            post.is_spam = False  # Mark as not spam
