import logging
import logging.config
import json
import os
from pathlib import Path
from typing import Optional

class Logger:
    _initialized = False
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get configured logger instance"""
        if not cls._initialized:
            cls._setup_logging()
        return logging.getLogger(name)

    @classmethod
    def _setup_logging(cls):
        """Configure logging system"""
        log_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'json': {
                    '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                    'fmt': '%(asctime)s %(levelname)s %(name)s %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                    'level': 'INFO'
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'logs/system.log',
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'formatter': 'standard',
                    'level': 'DEBUG'
                },
                'error_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'logs/error.log',
                    'maxBytes': 10485760,
                    'backupCount': 5,
                    'formatter': 'json',
                    'level': 'WARNING'
                }
            },
            'loggers': {
                '': {  # root logger
                    'handlers': ['console', 'file', 'error_file'],
                    'level': 'DEBUG',
                    'propagate': True
                },
                'security': {
                    'handlers': ['file', 'error_file'],
                    'level': 'INFO',
                    'propagate': False
                }
            }
        }
        
        # Ensure logs directory exists
        Path('logs').mkdir(exist_ok=True)
        
        # Apply configuration
        logging.config.dictConfig(log_config)
        cls._initialized = True

    @classmethod
    def audit_log(cls, action: str, user: Optional[str] = None, **kwargs):
        """Specialized audit logging"""
        audit_logger = logging.getLogger('audit')
        extra = {'user': user, 'action': action}
        extra.update(kwargs)
        audit_logger.info(
            f"Audit: {action} by {user or 'system'}",
            extra=extra
        )
