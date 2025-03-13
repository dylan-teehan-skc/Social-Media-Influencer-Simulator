"""
This module imports and re-exports the view components for easier imports.
"""

from src.views.main_window import SocialMediaMainWindow
from src.views.user_profile_widget import UserProfileWidget
from src.views.post_widget import PostWidget
from src.views.create_post_widget import CreatePostWidget
from src.views.feed_widget import FeedWidget
from src.views.follower_list_widget import FollowerListWidget

# Re-export the classes
__all__ = [
    'SocialMediaMainWindow',
    'UserProfileWidget',
    'PostWidget',
    'CreatePostWidget',
    'FeedWidget',
    'FollowerListWidget'
] 