from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.models.post import Post


class Dispatcher:
    def __init__(self):
        self.interceptors = []
        self.warnings = []

    def add_interceptor(self, interceptor: ContentInterceptor) -> None:
        self.interceptors.append(interceptor)
        
    def clear_warnings(self) -> None:
        """Clear all warnings collected during post processing."""
        self.warnings = []
        
    def add_warning(self, warning: str) -> None:
        """Add a warning message from an interceptor."""
        self.warnings.append(warning)
        
    def get_warnings(self) -> list:
        """Get all warnings collected during post processing."""
        return self.warnings.copy()

    def process_post(self, post: Post) -> None:
        """
        Process a post through all interceptors.
        
        Args:
            post: The post to process
        
        Returns:
            None
        """
        # Clear previous warnings
        self.clear_warnings()
        
        # Process the post through each interceptor
        for interceptor in self.interceptors:
            interceptor.intercept(post)
