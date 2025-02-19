import unittest
from src.models.follower import Follower
from src.models.post import Sentiment

class TestFollower(unittest.TestCase):

    def test_initial_sentiment_adjustment_left(self):
        follower = Follower(Sentiment.LEFT, handle="follower1")
        self.assertLessEqual(follower.political_lean, 50, "Political lean should be adjusted towards left")

    def test_initial_sentiment_adjustment_right(self):
        follower = Follower(Sentiment.RIGHT, handle="follower2")
        self.assertGreaterEqual(follower.political_lean, 50, "Political lean should be adjusted towards right")

    def test_initial_sentiment_adjustment_neutral(self):
        follower = Follower(Sentiment.NEUTRAL, handle="follower3")
        self.assertEqual(follower.political_lean, 50, "Political lean should remain neutral")

if __name__ == '__main__':
    unittest.main() 