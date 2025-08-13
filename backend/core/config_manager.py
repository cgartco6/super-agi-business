import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from .logging_setup import Logger

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize configuration manager"""
        self.logger = Logger.get_logger(__name__)
        self.config = {}
        self._load_environment()
        self._load_config_files()
        
    def _load_environment(self):
        """Load environment variables"""
        load_dotenv()
        self.env = os.environ
        
    def _load_config_files(self):
        """Load configuration from JSON files"""
        config_paths = [
            'config/core.json',
            'config/database.json',
            'config/services.json'
        ]
        
        for path in config_paths:
            try:
                with open(path) as f:
                    self.config.update(json.load(f))
            except FileNotFoundError:
                self.logger.warning(f"Config file not found: {path}")
            except json.JSONDecodeError:
                self.logger.error(f"Invalid JSON in config file: {path}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get configuration value with dot notation
        Example: get('database.host')
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return self.env.get(key.upper().replace('.', '_'), default)

    def update(self, key: str, value: Any, persist: bool = False):
        """
        Update configuration value
        """
        keys = key.split('.')
        current_level = self.config
        
        for k in keys[:-1]:
            if k not in current_level:
                current_level[k] = {}
            current_level = current_level[k]
        
        current_level[keys[-1]] = value
        
        if persist:
            self._persist_config()

    def _persist_config(self):
        """Save configuration changes to file"""
        for path, keys in [
            ('config/core.json', ['logging', 'security']),
            ('config/database.json', ['database']),
            ('config/services.json', ['services'])
        ]:
            config_part = {k: self.config[k] for k in keys if k in self.config}
            with open(path, 'w') as f:
                json.dump(config_part, f, indent=2)
