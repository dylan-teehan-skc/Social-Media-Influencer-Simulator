from src.models.post import Post, Comment, Sentiment
from src.services.logger_service import LoggerService
from src.services.sentiment_service import SentimentService
import os
import random
from dotenv import load_dotenv
from src.patterns.factory.post_builder_factory import PostBuilderFactory

try:
    from google import genai
    from google.api_core import exceptions as google_exceptions
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

class PostController:
    """Controller for Post model operations."""
    
    def __init__(self):
        """Initialize the post controller."""
        self.logger = LoggerService.get_logger()
        self.sentiment_service = SentimentService()
        
    def like_post(self, post):
        """Like a post."""
        if post:
            post._increment_likes()
            self.logger.info(f"Post liked: {post.content[:30]}...")
            
            # Liking a post has a small chance to gain a follower
            if random.random() < 0.1:  # 10% chance
                try:
                    # Try to get the main controller
                    from src.controllers.main_controller import MainController
                    main_controller = MainController.get_instance()
                    if main_controller and hasattr(main_controller, 'user_controller'):
                        # Generate a new follower
                        main_controller.user_controller.generate_new_followers(post, 1)
                except (ImportError, AttributeError) as e:
                    self.logger.warning(f"Could not generate follower from like: {str(e)}")
            
            return True
        return False
        
    def unlike_post(self, post):
        """Unlike a post."""
        if post:
            post._decrement_likes()
            self.logger.info(f"Post unliked: {post.content[:30]}...")
            return True
        return False
        
    def share_post(self, post):
        """Share a post."""
        if post:
            post._increment_shares()
            self.logger.info(f"Post shared: {post.content[:30]}...")
            
            # Sharing a post has a moderate chance to gain followers
            if random.random() < 0.25:  # 25% chance
                try:
                    # Try to get the main controller
                    from src.controllers.main_controller import MainController
                    main_controller = MainController.get_instance()
                    if main_controller and hasattr(main_controller, 'user_controller'):
                        # Generate new followers (1-3)
                        count = random.randint(1, 3)
                        main_controller.user_controller.generate_new_followers(post, count)
                except (ImportError, AttributeError) as e:
                    self.logger.warning(f"Could not generate followers from share: {str(e)}")
            
            return True
        return False
        
    def unshare_post(self, post):
        """Unshare a post."""
        if post:
            post._decrement_shares()
            self.logger.info(f"Post unshared: {post.content[:30]}...")
            return True
        return False
        
    def comment_on_post(self, post, content, sentiment, author):
        """Add a comment to a post."""
        if post and content:
            comment = Comment(content, sentiment, author)
            post._add_comment(comment)
            self.logger.info(f"Comment added to post: {content[:30]}...")
            
            # Comments have a small chance to gain a follower
            if random.random() < 0.05:  # 5% chance
                try:
                    # Try to get the main controller
                    from src.controllers.main_controller import MainController
                    main_controller = MainController.get_instance()
                    if main_controller and hasattr(main_controller, 'user_controller'):
                        # Generate a new follower
                        main_controller.user_controller.generate_new_followers(post, 1)
                except (ImportError, AttributeError) as e:
                    self.logger.warning(f"Could not generate follower from comment: {str(e)}")
            
            return comment
        return None
        
    def add_follower_gained(self, post):
        """Track a follower gained from a post."""
        if post:
            post._add_follower_gained()
            self.logger.info(f"Follower gained from post: {post.content[:30]}...")
            return True
        return False
        
    def add_follower_lost(self, post):
        """Track a follower lost from a post."""
        if post:
            post._add_follower_lost()
            self.logger.info(f"Follower lost from post: {post.content[:30]}...")
            return True
        return False
        
    def analyze_sentiment(self, content):
        """
        Analyze the sentiment of the content using only Google AI.
        
        Args:
            content: The content to analyze.
            
        Returns:
            A Sentiment enum value.
        """
        try:
            # Use the sentiment service for AI-based analysis only
            sentiment_result = self.sentiment_service.analyze_sentiment(content)
            self.logger.info(f"Raw sentiment result from service: {sentiment_result}, type: {type(sentiment_result)}")
            
            # Ensure sentiment_result is a float
            try:
                sentiment_float = float(sentiment_result)
                self.logger.info(f"Converted sentiment to float: {sentiment_float}, type: {type(sentiment_float)}")
            except (ValueError, TypeError):
                self.logger.error(f"Could not convert sentiment result '{sentiment_result}' to float")
                sentiment_float = 0.0  # Default to neutral
            
            # Convert the result to a Sentiment enum
            if sentiment_float <= -0.1:
                self.logger.info(f"Content classified as LEFT-leaning with score {sentiment_float}")
                return Sentiment.LEFT
            elif sentiment_float >= 0.1:
                self.logger.info(f"Content classified as RIGHT-leaning with score {sentiment_float}")
                return Sentiment.RIGHT
            else:
                self.logger.info(f"Content classified as NEUTRAL with score {sentiment_float}")
                return Sentiment.NEUTRAL
        except Exception as e:
            # Log the error and default to neutral
            self.logger.error(f"Error analyzing sentiment: {e}")
            return Sentiment.NEUTRAL

    def initial_impressions(self, post):
        """Analyze initial impressions of a post based on its sentiment."""
        try:
            if not post:
                return False
                
            self.logger.info(f"Analyzing initial impressions for post: {post.content[:30]}...")
            
            # Use the existing sentiment to determine impressions
            sentiment = post.sentiment
            
            # Log the sentiment-based analysis
            sentiment_name = sentiment.name if sentiment else "UNKNOWN"
            self.logger.info(f"Initial impressions based on sentiment: {sentiment_name}")
            
            # Adjust followers based on sentiment
            self._adjust_followers_based_on_sentiment(post)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in initial impressions analysis: {str(e)}")
            return False
    
    def _adjust_followers_based_on_sentiment(self, post):
        """Adjust followers gained/lost based on post sentiment and user's follower count."""
        if not post or not post.author:
            return
            
        # Get the user's current follower count
        user_followers = post.author._follower_count if hasattr(post.author, '_follower_count') else 0
        
        # Calculate a scaling factor based on follower count
        # More followers = more potential for both gains and losses
        # Start with a base of 1.0 and add 0.1 for every 10 followers, up to a maximum of 5.0
        scaling_factor = min(5.0, 1.0 + (user_followers / 100))
        
        self.logger.info(f"Follower scaling factor: {scaling_factor} (based on {user_followers} followers)")
        
        # Base follower changes on sentiment
        if post.sentiment == Sentiment.LEFT:
            # Left-leaning posts gain more left followers, lose some right followers
            base_gained = random.randint(1, 5)
            base_lost = random.randint(0, 3)
        elif post.sentiment == Sentiment.RIGHT:
            # Right-leaning posts gain more right followers, lose some left followers
            base_gained = random.randint(1, 5)
            base_lost = random.randint(0, 3)
        else:
            # Neutral posts have smaller, more balanced changes
            base_gained = random.randint(0, 2)
            base_lost = random.randint(0, 1)
        
        # Apply scaling factor
        gained = max(1, int(base_gained * scaling_factor))
        lost = max(0, int(base_lost * scaling_factor))
        
        self.logger.info(f"Follower changes: +{gained}, -{lost} (scaled from base +{base_gained}, -{base_lost})")
            
        # Apply the changes
        for _ in range(gained):
            self.add_follower_gained(post)
            
        for _ in range(lost):
            self.add_follower_lost(post)
    
    def _simple_keyword_analysis(self, content):
        """Simple keyword-based sentiment analysis as a fallback."""
        content_lower = content.lower()
        
        # Check for political keywords
        left_keywords = ["progressive", "liberal", "socialism", "equality", "democrat"]
        right_keywords = ["conservative", "traditional", "freedom", "patriot", "republican"]
        
        left_count = sum(1 for keyword in left_keywords if keyword in content_lower)
        right_count = sum(1 for keyword in right_keywords if keyword in content_lower)
        
        if left_count > right_count:
            return Sentiment.LEFT
        elif right_count > left_count:
            return Sentiment.RIGHT
        else:
            return Sentiment.NEUTRAL
            
    def get_post_stats(self, post):
        """Get statistics for a post."""
        if not post:
            return None
            
        return {
            "likes": post.likes,
            "shares": post.shares,
            "comments": len(post.comments),
            "sentiment": post.sentiment.name
        }
        
    def get_trending_posts(self, posts=None, limit=5):
        """
        Get trending posts based on engagement.
        
        Args:
            posts: List of posts to analyze. If None, will try to get posts from all users.
            limit: Maximum number of posts to return.
            
        Returns:
            List of trending posts sorted by engagement score.
        """
        if posts is None:
            # If no posts are provided, try to get posts from the main controller
            try:
                from src.controllers.main_controller import MainController
                main_controller = MainController.get_instance()
                if main_controller and hasattr(main_controller, 'user'):
                    # Get posts from the main user
                    posts = main_controller.user._posts if hasattr(main_controller.user, '_posts') else []
                    
                    # Also get posts from followers if available
                    if hasattr(main_controller.user, '_followers'):
                        for follower in main_controller.user._followers:
                            if hasattr(follower, '_posts'):
                                posts.extend(follower._posts)
            except (ImportError, AttributeError) as e:
                self.logger.warning(f"Could not get posts from main controller: {str(e)}")
                posts = []
                
        # If still no posts, return empty list
        if not posts:
            return []
            
        # Calculate engagement score (likes + shares + comments)
        def engagement_score(post):
            return post.likes + post.shares + len(post.comments)
            
        # Sort posts by engagement score
        sorted_posts = sorted(posts, key=engagement_score, reverse=True)
        
        # Return top posts
        return sorted_posts[:limit]