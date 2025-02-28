from src.interfaces.content_interceptor import ContentInterceptor
from src.models.post import Post

class SpamFilter(ContentInterceptor):
    def intercept(self, post: Post) -> None:
        pass
        #Todo: Implement spam filter
