from observer import Subject 

class User(Subject):
    def __init__(self, handle, bio):
        super().__init__()  
        self.handle = handle
        self.bio = bio
        self.followers = 0
        self.credibility_score = 0.0
        self.posts = []

    def create_post(self, content):
        pass

    def edit_post(self, post):
        pass

    def delete_post(self, post):
        pass

    def follow(self, user):
        pass

    def unfollow(self, user):
        pass

    def update_credibility(self):
        pass
