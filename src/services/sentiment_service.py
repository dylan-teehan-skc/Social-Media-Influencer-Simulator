import logging
import os
import re

from dotenv import load_dotenv


class SentimentService:
    # Service for analyzing sentiment of content using Google Gemini

    def __init__(self):
        self.logger = logging.getLogger("Social Media Simulator")

        # Load environment variables
        load_dotenv()

        # Initialize Google Gemini API
        try:
            import google.generativeai as genai

            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.genai = genai
                self.logger.info("Google Gemini API configured successfully")

                # Set up the model
                try:
                    self.model = genai.GenerativeModel("gemini-1.5-flash")
                    self.logger.info("Using model: gemini-1.5-flash")
                except Exception as e:
                    self.logger.error(
                        f"Error initializing recommended model: {str(e)}"
                    )
                    self.genai = None
            else:
                self.logger.error(
                    "Google API key not found in environment variables"
                )
                self.genai = None
        except ImportError:
            self.logger.error("Google Generative AI package not available")
            self.genai = None

    def analyze_sentiment(self, content):
        # Analyze political sentiment: -1.0 (left) to 1.0 (right)
        self.logger.info(f"Analyzing sentiment for: '{content}'")

        result = self.analyze_with_gemini(content)
        self.logger.info(f"Gemini sentiment analysis result: {result}")

        return result

    def analyze_with_gemini(self, content):
        # Check if Gemini is available
        if (
            not hasattr(self, "genai")
            or not self.genai
            or not hasattr(self, "model")
        ):
            self.logger.error(
                "Google Gemini not available for sentiment analysis"
            )
            return 0.0

        try:
            # Create prompt for political sentiment analysis
            prompt = f"""
            Analyze the political sentiment of the following text.
            Return ONLY a number between -1.0 (very liberal/left) and 1.0 (very conservative/right).

            Examples:
            "I support universal healthcare" -> -0.7
            "We need stronger border security" -> 0.7
            "The weather is nice today" -> 0.0
            "I hate the libs" -> 0.9
            "conservatives are ruining this country" -> -0.9

            Text to analyze: {content}

            Response (ONLY a number between -1.0 and 1.0):
            """

            # Get response from model
            response = self.model.generate_content(prompt)
            response_text = response.text

            self.logger.info(f"Gemini raw response: {response_text}")

            # Extract the numeric value
            match = re.search(r"(-?\d+(\.\d+)?)", response_text)
            if match:
                sentiment_value = float(match.group(1))
                # Ensure value is in valid range
                sentiment_value = max(-1.0, min(1.0, sentiment_value))
                self.logger.info(
                    f"Extracted sentiment value: {sentiment_value}"
                )
                return sentiment_value
            else:
                self.logger.error(
                    f"Could not extract sentiment value from response: {response_text}"
                )
                return 0.0

        except Exception as e:
            self.logger.error(
                f"Error during Gemini sentiment analysis: {str(e)}"
            )
            return 0.0
