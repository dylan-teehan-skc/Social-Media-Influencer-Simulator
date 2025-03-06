from src.builders.text_post_builder import TextPostBuilder
from src.builders.image_post_builder import ImagePostBuilder
from src.interfaces.post_builder import PostBuilder
from src.services.logger_service import LoggerService

class PostBuilderFactory:
    @staticmethod
    def get_builder(post_type: str) -> PostBuilder:
        logger = LoggerService.get_logger()
        
        try:
            if post_type == "text":
                logger.info("PostBuilderFactory: Creating TextPostBuilder")
                return TextPostBuilder()
                
            elif post_type == "image":
                logger.info("PostBuilderFactory: Creating ImagePostBuilder")
                return ImagePostBuilder()
                
            else:
                logger.error("PostBuilderFactory: Unknown post type requested: %s", post_type)
                raise ValueError(f"Unknown post type: {post_type}. Valid types are 'text' and 'image'")
                
        except Exception as e:
            logger.error("PostBuilderFactory: Error creating builder: %s", str(e))
            raise 