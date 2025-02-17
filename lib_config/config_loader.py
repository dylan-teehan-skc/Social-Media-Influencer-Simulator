import json

class ConfigLoader:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.load_config()
    
    def load_config(self, config_path='config.json'):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as file:
                self._config = json.load(file)
        except Exception as e:
            raise Exception(f"Error loading config file: {str(e)}")
    
    def get(self, key, default=None):
        """Get configuration value by key"""
        try:
            keys = key.split('.')
            value = self._config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default 