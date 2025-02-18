from observer import Observer, Subject  # Importing Observer and Subject

class User(Subject):
    def __init__(self, handle, bio):
        super().__init__()  # Initialize the Subject class
        # Attributes
        self.handle = handle
        self.bio = bio
        self.followers = 0
        self.credibility_score = 0.0
        self.posts = []

    def create_post(self, content):
        # Implementation for creating a post
        pass

    def edit_post(self, post):
        # Implementation for editing a post
        pass

    def delete_post(self, post):
        # Implementation for deleting a post
        pass

    def follow(self, user):
        # Implementation for following a user
        pass

    def unfollow(self, user):
        # Implementation for unfollowing a user
        pass

    def update_credibility(self):
        # Implementation for updating credibility score
        pass
