from random import randint

from src.command.post_commands import (
    CommandHistory,
    CommentCommand,
    LikeCommand,
    ShareCommand,
)
from src.interfaces.observer import Observer
from src.models.post import Comment, Post, Sentiment
from src.services.logger_service import LoggerService


class Follower(Observer):
    # Political lean thresholds
    LEFT_LEAN_THRESHOLD = 40
    RIGHT_LEAN_THRESHOLD = 60
    
    # Comment types
    FOLLOW_COMMENT_NEUTRAL = "Balanced take! Following for more."
    FOLLOW_COMMENT_POLITICAL = "Great content! Just followed you!"
    
    # Follower handle prefixes by sentiment
    FOLLOWER_PREFIXES = {
        Sentiment.LEFT: ["progressive_", "leftist_", "socialist_", "liberal_"],
        Sentiment.RIGHT: ["conservative_", "traditional_", "freedom_", "patriot_"],
        Sentiment.NEUTRAL: ["moderate_", "centrist_", "balanced_", "neutral_"]
    }

    def __init__(self, sentiment: Sentiment, handle: str):
        self.handle = handle
        self.logger = LoggerService.get_logger()

        # Set initial political lean based on sentiment
        if sentiment == Sentiment.LEFT:
            self.political_lean = randint(0, 30)  # Left-leaning: 0-30
        if sentiment == Sentiment.RIGHT:
            self.political_lean = randint(70, 100)  # Right-leaning: 70-100
        if sentiment == Sentiment.NEUTRAL:
            self.political_lean = randint(40, 60)  # Neutral: 40-60

        self.sentiment = sentiment  # Store the follower's sentiment
        self.command_history = CommandHistory()  # Track commands for potential undo

        self.positive_comments = [
            "Couldn't agree more!",
            "This is exactly what I've been saying!",
            "Great point!",
            "Thanks for sharing this important message!",
            "Absolutely spot on!"
        ]

        self.neutral_comments = [
            "Interesting perspective.",
            "Something to think about.",
            "I see your point.",
            "Worth considering.",
            "Thanks for sharing."
        ]

        self.negative_comments = [
            "I respectfully disagree.",
            "Not sure I can agree with this.",
            "You might want to reconsider this.",
            "I see it differently.",
            "Let's agree to disagree."
        ]

        self.logger.debug(f"Follower created: {handle} with {sentiment.name} sentiment and political lean {self.political_lean}")

    @classmethod
    def create_with_random_handle(cls, sentiment: Sentiment):
        """Create a follower with a randomly generated handle based on sentiment."""
        prefixes = cls.FOLLOWER_PREFIXES[sentiment]
        prefix = prefixes[randint(0, len(prefixes) - 1)]
        handle = f"{prefix}{randint(1000, 9999)}"
        return cls(sentiment, handle)
        
    @classmethod
    def create_random_follower(cls, index: int):
        """Create a follower with random sentiment based on index."""
        sentiment = list(cls.FOLLOWER_PREFIXES.keys())[index % 3]
        return cls.create_with_random_handle(sentiment)

    def update(self, subject, post=None):
        if post:
            self.interact_with_post(post)

            # Chance to unfollow if strongly disagree with post
            if self._should_unfollow(post):
                self.logger.info(f"Follower {self.handle} is unfollowing due to disagreement with post")
                subject.detach(self)

                # Create and execute a comment command for the unfollow notification
                unfollow_comment = Comment(
                    "I can't support this content. Unfollowing.",
                    self.sentiment,
                    self.handle)
                comment_command = CommentCommand(post, unfollow_comment)
                comment_command.execute()
                self.command_history.push(comment_command)

                post.add_follower_lost()  # Track lost follower

    def _should_unfollow(self, post: Post) -> bool:
        if post.sentiment == Sentiment.LEFT:
            alignment = 100 - self.political_lean
        elif post.sentiment == Sentiment.RIGHT:
            alignment = self.political_lean
        else:
            return False  # Don't unfollow for neutral posts

        # Higher chance to unfollow if strongly opposed to the post's sentiment
        should_unfollow = alignment < 20 and randint(1, 100) <= 30  # 30% chance if alignment < 20

        if should_unfollow:
            self.logger.debug(f"Follower {self.handle} decided to unfollow due to low alignment ({alignment})")

        return should_unfollow
        
    def should_follow(self, post: Post, follow_chance: int) -> bool:
        """Determine if follower should follow based on post sentiment and follow chance."""
        if post.sentiment == Sentiment.NEUTRAL:
            return randint(1, 100) <= follow_chance

        right_aligned = (
            self.political_lean > self.RIGHT_LEAN_THRESHOLD and
            post.sentiment == Sentiment.RIGHT
        )
        left_aligned = (
            self.political_lean < self.LEFT_LEAN_THRESHOLD and
            post.sentiment == Sentiment.LEFT
        )
        is_aligned = right_aligned or left_aligned
        return is_aligned and randint(1, 100) <= follow_chance
        
    def add_follow_comment(self, post: Post) -> None:
        """Add a comment to the post when following."""
        # Check if we've already commented on this post (to avoid duplicates)
        for comment in post.comments:
            if comment.author == self.handle:
                return  # Already commented, don't add another
                
        comment_text = (
            self.FOLLOW_COMMENT_NEUTRAL
            if post.sentiment == Sentiment.NEUTRAL
            else self.FOLLOW_COMMENT_POLITICAL
        )
        post.add_comment(Comment(comment_text, self.sentiment, self.handle))

    def _get_comment(self, alignment: float) -> str:
        if alignment > 70:
            return self.positive_comments[randint(0, len(self.positive_comments) - 1)]
        if alignment > 40:
            return self.neutral_comments[randint(0, len(self.neutral_comments) - 1)]
        return self.negative_comments[randint(0, len(self.negative_comments) - 1)]

    def _adjust_lean_from_sentiment(self, sentiment: Sentiment) -> None:
        old_lean = self.political_lean

        if sentiment == Sentiment.RIGHT:
            adjustment = randint(0, 10)
            self.political_lean = min(100, self.political_lean + adjustment)
        elif sentiment == Sentiment.LEFT:
            adjustment = randint(0, 10)
            self.political_lean = max(0, self.political_lean - adjustment)

        if old_lean != self.political_lean:
            self.logger.debug(f"Follower {self.handle} political lean adjusted from {old_lean} to {self.political_lean}")

    def interact_with_post(self, post: Post) -> None:
        self._adjust_lean_from_sentiment(post.sentiment)

        if post.sentiment == Sentiment.LEFT:
            alignment = 100 - self.political_lean
        elif post.sentiment == Sentiment.RIGHT:
            alignment = self.political_lean
        else:
            alignment = 100 - abs(50 - self.political_lean) * 2

        author_info = f"by {post.author.handle}" if post.author else "(no author)"
        self.logger.debug(f"Follower {self.handle} has {alignment}% alignment with post {author_info}")

        # Decide whether to comment (30% chance)
        if randint(1, 100) <= 30:
            comment_text = self._get_comment(alignment)
            comment = Comment(comment_text, self.sentiment, self.handle)

            # Create and execute comment command
            comment_command = CommentCommand(post, comment)
            comment_command.execute()
            self.command_history.push(comment_command)

        # Decide whether to like and/or share based on alignment
        if alignment > 70:
            # Create and execute like command
            like_command = LikeCommand(post, self.handle)
            like_command.execute()
            self.command_history.push(like_command)

            # Create and execute share command
            share_command = ShareCommand(post, self.handle)
            share_command.execute()
            self.command_history.push(share_command)

            self.logger.info(f"Follower {self.handle} liked and shared post due to high alignment ({alignment}%)")
        elif alignment > 40:
            # Create and execute like command only
            like_command = LikeCommand(post, self.handle)
            like_command.execute()
            self.command_history.push(like_command)

            self.logger.info(f"Follower {self.handle} liked post due to moderate alignment ({alignment}%)")
