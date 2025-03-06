from src.interfaces.content_interceptor import ContentInterceptor
from src.models.post import Post


class Dispatcher:
    def __init__(self):
        self.interceptors = []

    def add_interceptor(self, interceptor: ContentInterceptor) -> None:
        self.interceptors.append(interceptor)

    def process_post(self, post: Post) -> None:
        for interceptor in self.interceptors:
            interceptor.intercept(post)
