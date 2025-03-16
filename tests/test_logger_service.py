import unittest
from unittest.mock import patch, MagicMock

from src.services.logger_service import LoggerService


class TestLoggerServiceSingleton(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Reset logger instance before each test
        LoggerService._logger = None
    
    def test_singleton_instance(self):
        """Test that LoggerService maintains a single instance of the logger."""
        # Get first logger instance
        logger1 = LoggerService.get_logger()
        
        # Get second logger instance
        logger2 = LoggerService.get_logger()
        
        # Both should reference the same object
        self.assertIs(logger1, logger2)
    
    def test_logger_initialization(self):
        """Test that logger is initialized only once."""
        with patch('src.services.logger_service.logging') as mock_logging:
            mock_logger = MagicMock()
            mock_logging.getLogger.return_value = mock_logger
            
            # First call should create the logger
            logger1 = LoggerService.get_logger()
            
            # Second call should reuse the same logger
            logger2 = LoggerService.get_logger()
            
            # Verify getLogger was called exactly once
            mock_logging.getLogger.assert_called_once_with("Social Media Simulator")
    
    def test_custom_logger_setting(self):
        """Test that a custom logger can be set and retrieved."""
        # Create a mock custom logger
        custom_logger = MagicMock()
        
        # Set the custom logger
        LoggerService.set_logger(custom_logger)
        
        # Retrieved logger should be the same as the custom logger
        retrieved_logger = LoggerService.get_logger()
        self.assertIs(retrieved_logger, custom_logger)
        
    def test_default_logger_creation(self):
        """Test that a default logger is created if none exists."""
        with patch('src.services.logger_service.logging') as mock_logging:
            mock_logger = MagicMock()
            mock_handler = MagicMock()
            mock_formatter = MagicMock()
            
            mock_logging.getLogger.return_value = mock_logger
            mock_logging.StreamHandler.return_value = mock_handler
            mock_logging.Formatter.return_value = mock_formatter
            
            # Get logger (should create default)
            logger = LoggerService.get_logger()
            
            # Verify configuration of default logger
            mock_logging.getLogger.assert_called_once_with("Social Media Simulator")
            mock_logger.setLevel.assert_called_once_with(mock_logging.INFO)
            mock_handler.setFormatter.assert_called_once_with(mock_formatter)
            mock_logger.addHandler.assert_called_once_with(mock_handler)


if __name__ == '__main__':
    unittest.main() 