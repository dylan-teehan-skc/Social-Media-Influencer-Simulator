from src.models.post import Post
from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.services.logger_service import LoggerService
import os


class InappropriateContentFilter(ContentInterceptor):
    def __init__(self):
        self.logger = LoggerService.get_logger()
        self.inappropriate_words = self._load_bad_words()

    def _load_bad_words(self):
        """Load bad words from the CSV file."""
        bad_words = set()  # Using a set for faster lookups and to avoid duplicates
        try:
            # Get the absolute path to the bad_words.txt file
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            file_path = os.path.join(base_dir, 'bad_words.txt')
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Parse the CSV line and extract the word
                    parts = line.strip().split(',')
                    if len(parts) >= 5:
                        # Remove quotes if present and add to set
                        word = parts[4].strip('"')
                        if word:  # Only add non-empty words
                            bad_words.add(word.lower())
            
            self.logger.info(f"Loaded {len(bad_words)} inappropriate words from file")
            return bad_words
            
        except Exception as e:
            self.logger.error(f"Error loading bad words file: {str(e)}")
            # Fallback to a basic list if file can't be loaded
            return {
                "fuck", "shit", "bitch", "hate", "asshole"
            }

    def intercept(self, post: Post) -> None:
        """
        Intercept and check post content for inappropriate words.
        
        Args:
            post (Post): The post to check for inappropriate content
        """
        content_lower = post.content.lower()

        # Check for inappropriate content
        detected_words = set()
        for word in self.inappropriate_words:
            # Check if the word is a complete word (using word boundaries)
            if f" {word} " in f" {content_lower} ":
                detected_words.add(word)

        if detected_words:
            # Mark post as invalid
            post.is_valid = False

            # Create warning message
            warning_msg = f"Inappropriate content detected: Your post contains banned words ({', '.join(detected_words)})"

            # Add warning to dispatcher if available
            if hasattr(post, "_dispatcher") and post._dispatcher:
                post._dispatcher.add_warning(warning_msg)
        else:
            self.logger.info(
                "InappropriateContentFilter: No inappropriate content detected"
            )
