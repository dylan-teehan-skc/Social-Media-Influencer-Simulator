import logging

class LoggerService:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger('Social Media Application')
        return cls._logger

    @classmethod
    def set_logger(cls, logger):
        cls._logger = logger 