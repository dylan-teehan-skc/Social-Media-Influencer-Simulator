from src.builders.text_post_builder import TextPostBuilder
from src.builders.image_post_builder import ImagePostBuilder
from src.builders.post_builder import PostBuilder
from src.services.logger_service import LoggerService

class PostBuilderFactory:
    logger = LoggerService.get_logger()

    @staticmethod
    def get_builder(post_type: str) -> PostBuilder:
        PostBuilderFactory.logger.debug("Requesting builder for post type: %s", post_type)
        
        if post_type == "text":
            PostBuilderFactory.logger.info("Creating TextPostBuilder")
            return TextPostBuilder()
        elif post_type == "image":
            PostBuilderFactory.logger.info("Creating ImagePostBuilder")
            return ImagePostBuilder()
        else:
            PostBuilderFactory.logger.error("Unknown post type requested: %s", post_type)
            raise ValueError("Unknown post type") 