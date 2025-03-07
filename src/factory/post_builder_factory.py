from src.builders.image_post_builder import ImagePostBuilder
from src.builders.text_post_builder import TextPostBuilder
from src.interfaces.post_builder import PostBuilder
from src.services.logger_service import LoggerService


class PostBuilderFactory:
    """
    A factory for creating post builders.
    implements the PostBuilder interface.

    methods:
    -get_builder : returns the appropriate builder for the post type (text or image).
    """
    @staticmethod
    def get_builder(post_type: str) -> PostBuilder:
        logger = LoggerService.get_logger()

        try:
            if post_type == "text":
                logger.info("PostBuilderFactory: Creating TextPostBuilder")
                return TextPostBuilder()

            if post_type == "image":
                logger.info("PostBuilderFactory: Creating ImagePostBuilder")
                return ImagePostBuilder()

            logger.error("PostBuilderFactory: Invalid post type: %s", post_type)
            raise ValueError(f"Invalid post type: {post_type}")

        except Exception as e:
            logger.error("PostBuilderFactory: Error creating builder: %s", str(e))
            raise
