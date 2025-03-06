from src.interfaces.observer import Subject, Observer
from src.models.post import Post
from src.factory.post_builder_factory import PostBuilderFactory
from src.services.logger_service import LoggerService

class User(Subject):
    def __init__(self, handle, bio):
        super().__init__()  
        self.handle = handle
        self.bio = bio
        self.followers = 0
        self.posts = []
        self.logger = LoggerService.get_logger()

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
            self.followers += 1

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
            self.followers -= 1

    def notify(self, post=None):
        for observer in self._observers:
            observer.update(self, post)

    def create_post(self, content: str, image_path: str = None) -> Post:
        # Get the appropriate builder from the factory
        post_type = "image" if image_path else "text"
        post_builder = PostBuilderFactory.get_builder(post_type)
        
        # Build the post using the builder
        post = post_builder\
            .set_content(content)\
            .set_author(self)
            
        # Set image if provided
        if image_path:
            post = post.set_image(image_path)
            
        # Build and finalize the post
        post = post.build()
        post.initial_impressions()  # Analyze sentiment
        
        # Add to posts list and notify observers
        self.posts.append(post)
        self.notify(post)
        
        return post

    def edit_post(self, post):
        pass

    def delete_post(self, post):
        pass

    def follow(self, user):
        pass

    def unfollow(self, user):
        pass
