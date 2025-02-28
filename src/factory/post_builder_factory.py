from src.builders.text_post_builder import TextPostBuilder
from src.builders.image_post_builder import ImagePostBuilder
from src.builders.post_builder import PostBuilder

class PostBuilderFactory:
    @staticmethod
    def get_builder(post_type: str) -> PostBuilder:
        if post_type == "text":
            return TextPostBuilder()
        elif post_type == "image":
            return ImagePostBuilder()
        else:
            raise ValueError("Unknown post type") 