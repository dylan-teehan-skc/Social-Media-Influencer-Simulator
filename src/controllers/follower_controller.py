import random

from src.models.follower import Follower
from src.models.post import Comment, Sentiment
from src.patterns.command.post_commands import (
    CommentCommand,
    LikeCommand,
    ShareCommand,
)
from src.services.logger_service import LoggerService


class FollowerController:

    # Political lean thresholds
    LEFT_LEAN_THRESHOLD = 40
    RIGHT_LEAN_THRESHOLD = 60

    # Comment types
    FOLLOW_COMMENT_NEUTRAL = "Balanced take! Following for more."
    FOLLOW_COMMENT_POLITICAL = "Great content! Just followed you!"

    def __init__(self):
        self.logger = LoggerService.get_logger()

    def create_random_follower(self, sentiment=None):
        if sentiment is None:
            # Choose a random sentiment
            sentiment_values = list(Sentiment)
            sentiment = random.choice(sentiment_values)

        # Create a follower with the sentiment
        follower = Follower.create_with_random_handle(sentiment)
        self.logger.info(
            f"Created new follower: {
                follower.handle} with {
                sentiment.name} sentiment"
        )
        return follower

    def create_followers_batch(self, count, sentiment_distribution=None):
        followers = []

        # Set default distribution if none provided
        if sentiment_distribution is None:
            sentiment_distribution = {
                Sentiment.LEFT: 0.33,
                Sentiment.RIGHT: 0.33,
                Sentiment.NEUTRAL: 0.34,
            }

        # Validate distribution
        total = sum(sentiment_distribution.values())
        if abs(total - 1.0) > 0.01:  # Allow small rounding errors
            self.logger.warning(
                f"Sentiment distribution does not sum to 1.0: {total}"
            )
            # Normalize the distribution
            sentiment_distribution = {
                k: v / total for k, v in sentiment_distribution.items()
            }

        # Create followers based on distribution
        for _ in range(count):
            # Choose sentiment based on distribution
            r = random.random()
            cumulative = 0
            chosen_sentiment = Sentiment.NEUTRAL  # Default

            for sentiment, probability in sentiment_distribution.items():
                cumulative += probability
                if r <= cumulative:
                    chosen_sentiment = sentiment
                    break

            # Create follower with chosen sentiment
            follower = self.create_random_follower(chosen_sentiment)
            followers.append(follower)

        self.logger.info(f"Created batch of {count} followers")
        return followers

    def should_follow(self, follower, post, follow_chance):
        # Increase follow chance for debugging
        follow_chance = min(100, follow_chance * 2)

        self.logger.debug(
            f"Follower {
                follower.handle} considering following with chance {follow_chance}%"
        )

        # For neutral posts, any follower might follow
        if post.sentiment == Sentiment.NEUTRAL:
            result = random.randint(1, 100) <= follow_chance
            if result:
                self.logger.info(
                    f"Follower {
                        follower.handle} will follow due to neutral post"
                )
            return result

        # For political posts, check alignment
        right_aligned = (
            follower.political_lean > self.RIGHT_LEAN_THRESHOLD
            and post.sentiment == Sentiment.RIGHT
        )
        left_aligned = (
            follower.political_lean < self.LEFT_LEAN_THRESHOLD
            and post.sentiment == Sentiment.LEFT
        )

        # If aligned, significantly increase the chance of following
        is_aligned = right_aligned or left_aligned
        if is_aligned:
            # Boost follow chance for aligned followers
            aligned_follow_chance = min(100, follow_chance * 1.5)  # 50% boost
            result = random.randint(1, 100) <= aligned_follow_chance
        else:
            # Much lower chance for non-aligned followers
            result = random.randint(1, 100) <= (
                follow_chance * 0.3
            )  # 70% reduction

        if result:
            self.logger.info(
                f"Follower {
                    follower.handle} will follow due to {
                    'aligned' if is_aligned else 'non-aligned'} post"
            )

        return result

    def add_follow_comment(self, follower, post):
        # Check if we've already commented on this post (to avoid duplicates)
        for comment in post.comments:
            if comment.author == follower.handle:
                return  # Already commented, don't add another

        comment_text = (
            self.FOLLOW_COMMENT_NEUTRAL
            if post.sentiment == Sentiment.NEUTRAL
            else self.FOLLOW_COMMENT_POLITICAL
        )

        # Create and execute a comment command
        comment = Comment(comment_text, follower.sentiment, follower.handle)
        comment_command = CommentCommand(post, comment)
        comment_command.execute()

        # Store the command in the follower's history if available
        if hasattr(follower, "command_history"):
            follower.command_history.push(comment_command)

    def process_follower_interaction(self, follower, post):
        # First adjust political lean based on post sentiment
        self.adjust_lean_from_sentiment(follower, post.sentiment)

        # Calculate alignment between follower and post
        alignment = self.calculate_alignment(follower, post)

        # Comment chance based on alignment
        if alignment > 70:
            comment_chance = 60
        elif alignment > 40:
            comment_chance = 30
        else:
            comment_chance = 10

        # Like chance based on alignment
        if alignment > 70:
            like_chance = 80
        elif alignment > 40:
            like_chance = 40
        else:
            like_chance = 5

        # Share chance based on alignment
        if alignment > 70:
            share_chance = 30
        elif alignment > 40:
            share_chance = 10
        else:
            share_chance = 1

        # Perform interactions
        interactions_occurred = False

        # Try to comment
        if random.randint(1, 100) <= comment_chance:
            comment_text = self.get_comment_for_alignment(
                alignment, post.sentiment
            )
            comment = Comment(
                comment_text, follower.sentiment, follower.handle
            )
            comment_command = CommentCommand(post, comment)
            comment_command.execute()

            # Store the command in the follower's history if available
            if hasattr(follower, "command_history"):
                follower.command_history.push(comment_command)

            self.logger.info(
                f"Follower {follower.handle} commented on post: {comment_text[:30]}..."
            )
            interactions_occurred = True

        # Try to like
        if random.randint(1, 100) <= like_chance:
            like_command = LikeCommand(post, follower.handle)
            like_command.execute()

            # Store the command in the follower's history if available
            if hasattr(follower, "command_history"):
                follower.command_history.push(like_command)

            self.logger.info(f"Follower {follower.handle} liked post")
            interactions_occurred = True

        # Try to share
        if random.randint(1, 100) <= share_chance:
            share_command = ShareCommand(post, follower.handle)
            share_command.execute()

            # Store the command in the follower's history if available
            if hasattr(follower, "command_history"):
                follower.command_history.push(share_command)

            self.logger.info(f"Follower {follower.handle} shared post")
            interactions_occurred = True

        return interactions_occurred

    def calculate_alignment(self, follower, post):
        # Calculate how well follower aligns with post sentiment (0-100%)
        if post.sentiment == Sentiment.LEFT:
            alignment = (
                100 - follower.political_lean
            )  # Higher political_lean = less aligned with LEFT
        elif post.sentiment == Sentiment.RIGHT:
            alignment = (
                follower.political_lean
            )  # Higher political_lean = more aligned with RIGHT
        else:
            # For neutral posts, alignment is based on how moderate the follower is
            alignment = 100 - abs(50 - follower.political_lean) * 2

        # Ensure alignment is between 0 and 100
        return max(0, min(100, alignment))

    def adjust_lean_from_sentiment(self, follower, sentiment):
        old_lean = follower.political_lean

        # Small adjustment based on post sentiment
        if sentiment == Sentiment.LEFT:
            # Left content pushes political lean slightly left (lower)
            adjustment = -random.randint(1, 3)
        elif sentiment == Sentiment.RIGHT:
            # Right content pushes political lean slightly right (higher)
            adjustment = random.randint(1, 3)
        else:
            # Neutral content pushes political lean slightly toward center
            if follower.political_lean > 50:
                adjustment = -random.randint(0, 2)
            elif follower.political_lean < 50:
                adjustment = random.randint(0, 2)
            else:
                adjustment = 0

        # Apply the adjustment
        follower.political_lean = max(
            0, min(100, follower.political_lean + adjustment)
        )

        if old_lean != follower.political_lean:
            self.logger.info(
                f"Follower {
                    follower.handle} political lean adjusted from {old_lean} to {
                    follower.political_lean} due to {
                    sentiment.name} content"
            )

    def get_comment_for_alignment(self, alignment, post_sentiment):
        # Define comment pools
        positive_comments = [
            "Couldn't agree more!",
            "This is exactly what I've been saying!",
            "Great point!",
            "Thanks for sharing this important message!",
            "Absolutely spot on!",
        ]

        neutral_comments = [
            "Interesting perspective.",
            "Something to think about.",
            "I see your point.",
            "Worth considering.",
            "Thanks for sharing.",
        ]

        negative_comments = [
            "I respectfully disagree.",
            "Not sure I can agree with this.",
            "You might want to reconsider this.",
            "I see it differently.",
            "Let's agree to disagree.",
        ]

        # Select comment pool based on alignment
        if alignment > 70:
            comment_pool = positive_comments
        elif alignment > 40:
            comment_pool = neutral_comments
        else:
            comment_pool = negative_comments

        # Add sentiment-specific comments for political posts
        if post_sentiment == Sentiment.LEFT:
            if alignment > 70:
                comment_pool.extend(
                    [
                        "Progressive values at work!",
                        "This is the kind of equality we need.",
                        "Fighting for social justice!",
                    ]
                )
            elif alignment < 30:
                comment_pool.extend(
                    [
                        "This seems too radical.",
                        "Not sure this is practical.",
                        "Have you considered the economic impact?",
                    ]
                )
        elif post_sentiment == Sentiment.RIGHT:
            if alignment > 70:
                comment_pool.extend(
                    [
                        "Standing up for traditional values!",
                        "Freedom and individual responsibility!",
                        "Protecting what matters most.",
                    ]
                )
            elif alignment < 30:
                comment_pool.extend(
                    [
                        "This seems too regressive.",
                        "What about those who need help?",
                        "Have you considered the social impact?",
                    ]
                )

        # Choose a random comment from the pool
        return random.choice(comment_pool)

    def should_unfollow(self, follower, post):
        # Calculate alignment between follower and post
        alignment = self.calculate_alignment(follower, post)

        # Don't unfollow for neutral posts
        if post.sentiment == Sentiment.NEUTRAL:
            return False

        # Log the alignment for debugging
        self.logger.debug(
            f"Follower {
                follower.handle} (political lean: {
                follower.political_lean}) has {alignment}% alignment with {
                post.sentiment.name} post"
        )

        # Determine unfollow chance based on alignment
        if alignment < 20:
            unfollow_chance = 80
        elif alignment < 40:
            unfollow_chance = 50
        elif alignment < 60:
            unfollow_chance = 20
        elif alignment < 80:
            unfollow_chance = 10
        else:
            unfollow_chance = 0

        # Roll the dice
        should_unfollow = random.randint(1, 100) <= unfollow_chance

        if should_unfollow:
            self.logger.info(
                f"Follower {
                    follower.handle} (political lean: {
                    follower.political_lean}) decided to unfollow due to low alignment ({alignment}%) with {
                    post.sentiment.name} post"
            )

        return should_unfollow

    def update_follower(self, follower, subject, post=None):
        if post:
            # Let the follower interact with the post using its own method
            follower.interact_with_post(post)

            # Process the interaction in the controller
            self.process_follower_interaction(follower, post)

            # Check if should unfollow based on post sentiment
            if self.should_unfollow(follower, post):
                self.logger.info(
                    f"Follower {
                        follower.handle} is unfollowing due to disagreement with post"
                )

                # Create and execute a comment command for the unfollow notification
                unfollow_comment = Comment(
                    "I can't support this content. Unfollowing.",
                    follower.sentiment,
                    follower.handle,
                )
                comment_command = CommentCommand(post, unfollow_comment)
                comment_command.execute()

                # Store the command in the follower's history if available
                if hasattr(follower, "command_history"):
                    follower.command_history.push(comment_command)

                # Track lost follower
                post._add_follower_lost()

                # Emit signal if available
                if hasattr(follower, "unfollowed"):
                    follower.unfollowed.emit(subject)

                return True  # Indicate that unfollowing occurred

        return False  # No unfollowing occurred

    def calculate_follow_chance(self, user, post_sentiment):
        # Apply reputation penalty
        reputation_penalty = min(
            user.MAX_REPUTATION_PENALTY,
            user._recent_follower_losses * user.REPUTATION_PENALTY_PER_LOSS,
        )

        # Set base chance based on post sentiment
        if post_sentiment == Sentiment.NEUTRAL:
            base_chance = user.BASE_NEUTRAL_CHANCE
        else:
            # Political posts have higher chance to attract followers
            base_chance = (
                user.HOT_TAKE_CHANCE * 1.5
            )  # 50% boost for political posts

        # Apply reputation penalty
        adjusted_chance = base_chance * (1 - reputation_penalty)

        # Apply follower multiplier (more followers = more visibility)
        follower_multiplier = min(
            user.MAX_FOLLOWER_MULTIPLIER,
            1.0 + (user._follower_count / user.FOLLOWER_MULTIPLIER_SCALE),
        )

        final_chance = int(adjusted_chance * follower_multiplier)

        # Log the calculation
        self.logger.debug(
            f"Follow chance calculation: sentiment={post_sentiment.name}, "
            f"base={base_chance}, reputation_penalty={reputation_penalty}, "
            f"follower_multiplier={follower_multiplier}, final={final_chance}"
        )

        return final_chance

    def generate_potential_followers(self, post, count=5):
        # Create distribution based on post sentiment
        if post.sentiment == Sentiment.LEFT:
            # Left-leaning post attracts more left-leaning followers
            distribution = {
                Sentiment.LEFT: 0.6,
                Sentiment.NEUTRAL: 0.3,
                Sentiment.RIGHT: 0.1,
            }
        elif post.sentiment == Sentiment.RIGHT:
            # Right-leaning post attracts more right-leaning followers
            distribution = {
                Sentiment.RIGHT: 0.6,
                Sentiment.NEUTRAL: 0.3,
                Sentiment.LEFT: 0.1,
            }
        else:
            # Neutral post attracts balanced followers
            distribution = {
                Sentiment.NEUTRAL: 0.5,
                Sentiment.LEFT: 0.25,
                Sentiment.RIGHT: 0.25,
            }

        # Generate followers with the distribution
        return self.create_followers_batch(count, distribution)
