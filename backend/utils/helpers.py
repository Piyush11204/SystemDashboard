import json
import logging
import os

class LoggerHelper:
    @staticmethod
    def setup_logger():
        logger = logging.getLogger("flask_app")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

class ConfigManager:
    @staticmethod
    def load_config():
        """Loads configuration from config.json."""
        config_path = os.path.join(os.path.dirname(__file__), "../config.json")
        with open(config_path, "r") as file:
            return json.load(file)
