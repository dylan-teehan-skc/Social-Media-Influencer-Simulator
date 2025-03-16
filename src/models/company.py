from src.models.post import Sentiment


class Company:
    # company that can sponsor users

    def __init__(
        self,
        name,
        description,
        logo_path=None,
        political_leaning=Sentiment.NEUTRAL,
    ):
        self.name = name
        self.description = description
        self.logo_path = logo_path
        self.political_leaning = political_leaning
        self.sponsored_users = []

    def sponsor_user(self, user):
        # Add a user to the company's sponsored users list
        if user not in self.sponsored_users:
            self.sponsored_users.append(user)
            return True
        return False

    def remove_sponsorship(self, user):
        # Remove a user from the company's sponsored users list
        if user in self.sponsored_users:
            self.sponsored_users.remove(user)
            return True
        return False

    @property
    def political_alignment_string(self):
        # Get a string representation of the company's political leaning
        if self.political_leaning == Sentiment.LEFT:
            return "Left-leaning"
        elif self.political_leaning == Sentiment.RIGHT:
            return "Right-leaning"
        else:
            return "Politically neutral"

    def __str__(self):
        return f"{self.name} ({self.political_alignment_string})"
