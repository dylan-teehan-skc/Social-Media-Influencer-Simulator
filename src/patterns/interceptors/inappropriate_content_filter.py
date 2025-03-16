from src.models.post import Post
from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.services.logger_service import LoggerService
import os


class InappropriateContentFilter(ContentInterceptor):
    def __init__(self):
        self.logger = LoggerService.get_logger()
        self.inappropriate_words = self._load_bad_words()

    def _load_bad_words(self):
        bad_words = set()
        try:
            file_path = 'src/patterns/interceptors/interception_criteria/bad_words.csv'
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 5:
                        word = parts[4].strip('"')
                        if word:
                            bad_words.add(word.lower())
            
            self.logger.info(f"Loaded {len(bad_words)} inappropriate words from file")
            return bad_words
            
        except Exception as e:
            self.logger.error(f"Error loading bad words file: {str(e)}")
            return set()

    def intercept(self, post: Post) -> None:
        content_lower = post.content.lower()
        detected_words = set()
        
        for word in self.inappropriate_words:
            if f" {word} " in f" {content_lower} ":
                detected_words.add(word)

        if detected_words:
            post.is_valid = False
            warning_msg = f"Inappropriate content detected: Your post contains banned words ({', '.join(detected_words)})"
            if hasattr(post, "_dispatcher") and post._dispatcher:
                post._dispatcher.add_warning(warning_msg)
        else:
            self.logger.info("InappropriateContentFilter: No inappropriate content detected")
