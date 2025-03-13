# import unittest
# from unittest.mock import MagicMock, patch

# from src.models.user import User
# from src.models.post import Post, Sentiment
# from src.models.follower import Follower


# class TestUser(unittest.TestCase):
#     def setUp(self):
#         # Need pygame for the timer stuff
#         pygame.init()
        
#         # Create a test user
#         self.user = User("test_user", "Test user bio")
        
#         # Set up some mock followers with different political leanings
#         self.left_follower = Follower(Sentiment.LEFT, "left_follower")
#         self.right_follower = Follower(Sentiment.RIGHT, "right_follower")
#         self.neutral_follower = Follower(Sentiment.NEUTRAL, "neutral_follower")

#     def tearDown(self):
#         pygame.quit()

#     def test_user_initialization(self):
#         """Check if user gets created with the right starting values."""
#         self.assertEqual(self.user.handle, "test_user")
#         self.assertEqual(self.user.bio, "Test user bio")
#         self.assertEqual(self.user.followers, 0)
#         self.assertEqual(len(self.user.posts), 0)
#         self.assertEqual(self.user.recent_follower_losses, 0)

#     def test_attach_observer(self):
#         """Make sure we can add followers to a user."""
#         self.user.attach(self.left_follower)
#         self.assertEqual(self.user.followers, 1)
#         self.assertIn(self.left_follower, self.user._observers)

#     def test_detach_observer(self):
#         """Make sure we can remove followers from a user."""
#         self.user.attach(self.left_follower)
#         self.user.detach(self.left_follower)
#         self.assertEqual(self.user.followers, 0)
#         self.assertNotIn(self.left_follower, self.user._observers)

#     @patch('src.factory.post_builder_factory.PostBuilderFactory.get_builder')
#     def test_create_text_post(self, mock_get_builder):
#         """Check if we can create a text post."""
#         # Set up our mock builder
#         mock_builder = MagicMock()
#         mock_builder.set_content.return_value = mock_builder
#         mock_builder.set_author.return_value = mock_builder
#         mock_post = MagicMock(spec=Post)
#         mock_builder.build.return_value = mock_post
#         mock_get_builder.return_value = mock_builder
        
#         # Create the post
#         post = self.user.create_post("Test post content")
        
#         # Check if the builder was used correctly
#         mock_get_builder.assert_called_once_with("text")
#         mock_builder.set_content.assert_called_once_with("Test post content")
#         mock_builder.set_author.assert_called_once_with(self.user)
#         mock_builder.build.assert_called_once()
        
#         # Check if the post was added to the user's posts
#         self.assertIn(mock_post, self.user.posts)
        
#         # Check if initial_impressions was called
#         mock_post.initial_impressions.assert_called_once()

#     @patch('src.factory.post_builder_factory.PostBuilderFactory.get_builder')
#     def test_create_image_post(self, mock_get_builder):
#         """Check if we can create an image post."""
#         # Set up our mock builder
#         mock_builder = MagicMock()
#         mock_builder.set_content.return_value = mock_builder
#         mock_builder.set_author.return_value = mock_builder
#         mock_builder.set_image.return_value = mock_builder
#         mock_post = MagicMock(spec=Post)
#         mock_builder.build.return_value = mock_post
#         mock_get_builder.return_value = mock_builder
        
#         # Create the post
#         post = self.user.create_post("Test post with image", "path/to/image.jpg")
        
#         # Check if the builder was used correctly
#         mock_get_builder.assert_called_once_with("image")
#         mock_builder.set_content.assert_called_once_with("Test post with image")
#         mock_builder.set_author.assert_called_once_with(self.user)
#         mock_builder.set_image.assert_called_once_with("path/to/image.jpg")
#         mock_builder.build.assert_called_once()
        
#         # Check if the post was added to the user's posts
#         self.assertIn(mock_post, self.user.posts)

#     def test_calculate_follow_chance(self):
#         """Check the math for calculating follow chance."""
#         # Neutral post with no reputation penalty
#         chance = self.user.calculate_follow_chance(Sentiment.NEUTRAL)
#         self.assertEqual(chance, 40)  # BASE_NEUTRAL_CHANCE
        
#         # Political post should have higher chance
#         chance = self.user.calculate_follow_chance(Sentiment.LEFT)
#         self.assertEqual(chance, 60)  # HOT_TAKE_CHANCE
        
#         # Bad reputation should reduce chances
#         self.user.recent_follower_losses = 2
#         chance = self.user.calculate_follow_chance(Sentiment.NEUTRAL)
#         self.assertEqual(chance, 24)  # 40 * (1 - 0.4)
        
#         # More followers should boost chances
#         self.user.recent_follower_losses = 0
#         self.user.followers = 30
#         chance = self.user.calculate_follow_chance(Sentiment.NEUTRAL)
#         self.assertEqual(chance, 120)  # 40 * 3.0

#     def test_update_reputation(self):
#         """Check if reputation gets damaged when followers leave."""
#         # Set up the test
#         initial_followers = 10
#         self.user.followers = 8  # 2 followers lost
#         mock_post = MagicMock(spec=Post)
        
#         # Update reputation
#         self.user.update_reputation(initial_followers, mock_post)
        
#         # Check if reputation was updated
#         self.assertEqual(self.user.recent_follower_losses, 2)
        
#         # Check if warning threshold works
#         self.user.followers = 5  # 5 more followers lost
#         self.user.update_reputation(10, mock_post)
#         self.assertEqual(self.user.recent_follower_losses, 7)
#         mock_post.add_comment.assert_called_once()  # Should add a warning comment

#     def test_update_reputation_recovery(self):
#         """Check if reputation recovers over time."""
#         # Set up the test
#         self.user.recent_follower_losses = 3
#         self.user.last_reputation_check = pygame.time.get_ticks() - User.REPUTATION_RECOVERY_DELAY - 1000
        
#         # Update reputation recovery
#         self.user.update_reputation_recovery(pygame.time.get_ticks())
        
#         # Check if reputation recovered
#         self.assertEqual(self.user.recent_follower_losses, 2)
        
#         # Check if it can recover completely
#         self.user.recent_follower_losses = 1
#         self.user.last_reputation_check = pygame.time.get_ticks() - User.REPUTATION_RECOVERY_DELAY - 1000
#         self.user.update_reputation_recovery(pygame.time.get_ticks())
#         self.assertEqual(self.user.recent_follower_losses, 0)


# if __name__ == '__main__':
#     unittest.main() 