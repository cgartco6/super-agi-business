from typing import Dict, Any
from http import HTTPStatus
from .logging_setup import Logger

class ErrorHandler:
    _error_map = {
        400: {
            'status': HTTPStatus.BAD_REQUEST,
            'message': 'Bad request'
        },
        401: {
            'status': HTTPStatus.UNAUTHORIZED,
            'message': 'Unauthorized'
        },
        403: {
            'status': HTTPStatus.FORBIDDEN,
            'message': 'Forbidden'
        },
        404: {
            'status': HTTPStatus.NOT_FOUND,
            'message': 'Resource not found'
        },
        500: {
            'status': HTTPStatus.INTERNAL_SERVER_ERROR,
            'message': 'Internal server error'
        }
    }
    
    @classmethod
    def handle_error(cls, error: Exception) -> Dict[str, Any]:
        """Handle exceptions and return appropriate response"""
        logger = Logger.get_logger(__name__)
        error_type = type(error).__name__
        
        # Map specific exceptions to HTTP status codes
        status_code = getattr(error, 'status_code', 500)
        error_details = cls._error_map.get(status_code, cls._error_map[500])
        
        # Log the error
        logger.error(
            f"Error {status_code}: {str(error)}",
            exc_info=True,
            extra={'error_type': error_type}
        )
        
        # Prepare response
        response = {
            'status': 'error',
            'code': status_code,
            'message': error_details['message'],
            'details': str(error),
            'type': error_type
        }
        
        # Add traceback in development mode
        if cls._is_development():
            from traceback import format_exc
            response['traceback'] = format_exc()
            
        return response

    @classmethod
    def _is_development(cls) -> bool:
        """Check if running in development environment"""
        import os
        return os.getenv('ENVIRONMENT', 'production') == 'development'
