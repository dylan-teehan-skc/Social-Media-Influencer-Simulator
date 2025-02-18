from observer import Subject, Observer

class User(Subject):
    def __init__(self, handle, bio):
        super().__init__()  
        self.handle = handle
        self.bio = bio
        self.followers = 0
        self.posts = []

    def attach(self, observer: Observer):
        """Attach an observer (follower) to this user"""
        if observer not in self._observers:
            self._observers.append(observer)
            self.followers += 1

    def detach(self, observer: Observer):
        """Detach an observer (follower) from this user"""
        if observer in self._observers:
            self._observers.remove(observer)
            self.followers -= 1

    def notify(self, post=None):
        """Notify all observers (followers) about a new post or update"""
        for observer in self._observers:
            observer.update(self, post)

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

