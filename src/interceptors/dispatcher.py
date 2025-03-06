from src.models.post import Post
from src.interfaces.content_interceptor import ContentInterceptor

class Dispatcher:
    """
    The Dispatcher class is responsible for dispatching posts to the appropriate interceptors.
    It also holds the list of interceptors.
    """
    def __init__(self):
        self.interceptors = []

    def add_interceptor(self, interceptor: ContentInterceptor) -> None:
        self.interceptors.append(interceptor)

    def process_post(self, post: Post) -> None:
        for interceptor in self.interceptors:
            interceptor.intercept(post) 