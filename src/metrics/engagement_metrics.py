from src.models.post import Post

class EngagementMetrics:
    def __init__(self):
        self.total_likes = 0
        self.total_shares = 0
        self.engagement_rate = 0.0

    def update_metrics(self, post: Post) -> None:
        self.total_likes += post.likes
        self.total_shares += post.shares

    def calculate_engagement_rate(self) -> float:
        total_engagements = self.total_likes + self.total_shares
        if total_engagements == 0:
            return 0.0
        self.engagement_rate = total_engagements / 2  # Example calculation
        return self.engagement_rate 