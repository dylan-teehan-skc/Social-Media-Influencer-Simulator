from src.models.post import Post
from src.patterns.interfaces.content_interceptor import ContentInterceptor
from src.services.logger_service import LoggerService
import csv
import os


class SpamFilter(ContentInterceptor):
    
    def __init__(self):
        self.logger = LoggerService.get_logger()
        self.spam_keywords = self._load_spam_keywords()
        self.logger.info(f"SpamFilter initialized with {len(self.spam_keywords)} keywords")

    def _load_spam_keywords(self):
        """Load spam keywords from the spam.txt file"""
        keywords = set()  
        try:
            spam_file_path = 'src/patterns/interceptors/interception_criteria/spam.txt'
            
            self.logger.info(f"Attempting to load spam keywords from: {spam_file_path}")
            
            if not os.path.exists(spam_file_path):
                self.logger.error(f"Spam file not found at: {spam_file_path}")
                raise FileNotFoundError(f"Could not find spam.txt at {spam_file_path}")
            
            with open(spam_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if 'Keyword' in row and row['Keyword']:
                        keyword = row['Keyword'].strip().lower()
                        if keyword:  
                            keywords.add(keyword)
            
            if not keywords:
                self.logger.warning("No keywords were loaded from the file")
                raise ValueError("No keywords found in spam.txt")
                
            return keywords
        except Exception as e:
            self.logger.error(f"Error loading spam keywords: {str(e)}")
            # Fallback to a minimal set of spam keywords if file can't be read
            fallback_keywords = {"buy now", "limited time offer", "act now", "click here"}
            self.logger.info(f"Using fallback keywords: {fallback_keywords}")
            return fallback_keywords

    def intercept(self, post):
        content = post.content.lower()
        detected_phrases = []

        self.logger.debug(f"Checking content: {content[:100]}...")

        # Check for spam keywords
        for keyword in self.spam_keywords:
            if keyword in content:
                detected_phrases.append(keyword)
                self.logger.debug(f"Found spam keyword: {keyword}")

        SPAM_THRESHOLD = 2
        if len(detected_phrases) >= SPAM_THRESHOLD:
            post.is_valid = False
            warning_msg = f"Potential spam detected: Your post contains multiple prohibited phrases ({', '.join(detected_phrases)})"
            
            self.logger.warning(
                f"SpamFilter: Multiple spam keywords detected in post: {post.content[:50]}..."
            )

            if hasattr(post, "_dispatcher") and post._dispatcher:
                post._dispatcher.add_warning(warning_msg)

        else:   
            self.logger.info(
                f"SpamFilter: No significant spam detected in post: {post.content[:50]}..."
            )
        
        
