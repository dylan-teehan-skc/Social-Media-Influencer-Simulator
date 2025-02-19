import unittest
from src.models.follower import Follower
from src.models.post import Sentiment

class TestFollower(unittest.TestCase):

    def test_initial_sentiment_adjustment_left(self):
        follower = Follower(Sentiment.LEFT)
        self.assertLessEqual(follower.political_lean, 50, "Political lean should be adjusted towards left")

    def test_initial_sentiment_adjustment_right(self):
        follower = Follower(Sentiment.RIGHT)
        self.assertGreaterEqual(follower.political_lean, 50, "Political lean should be adjusted towards right")

    def test_initial_sentiment_adjustment_neutral(self):
        follower = Follower(Sentiment.NEUTRAL)
        self.assertEqual(follower.political_lean, 50, "Political lean should remain neutral")

if __name__ == '__main__':
    unittest.main() 