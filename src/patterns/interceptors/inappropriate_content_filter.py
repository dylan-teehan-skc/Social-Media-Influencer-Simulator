from src.interfaces.content_interceptor import ContentInterceptor
from src.models.post import Post


class InappropriateContentFilter(ContentInterceptor):
    def intercept(self, post: Post) -> None:
        # TODO: Implement inappropriate content filter
        # pylint: disable=W0511
        pass
