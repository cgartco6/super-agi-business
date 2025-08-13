import re
from typing import Dict, Optional
from ..logging_setup import Logger
from ..error_handler import ErrorHandler

class RequestValidator:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        
    def validate_request(self, request: Dict, schema: Dict) -> Optional[Dict]:
        """Validate request against schema"""
        errors = {}
        
        for field, config in schema.items():
            value = request.get(field)
            
            # Check required fields
            if config.get('required') and value is None:
                errors[field] = "This field is required"
                continue
                
            # Type validation
            if value is not None and not self._validate_type(value, config.get('type')):
                errors[field] = f"Expected type {config['type']}"
                continue
                
            # Pattern validation
            if 'pattern' in config and not re.match(config['pattern'], str(value)):
                errors[field] = "Invalid format"
                
            # Custom validation
            if 'validate' in config and not config['validate'](value):
                errors[field] = "Validation failed"
        
        if errors:
            error_msg = "Request validation failed"
            self.logger.warning(f"{error_msg}: {errors}")
            return ErrorHandler.handle_error(
                ValueError(error_msg),
                extra={'validation_errors': errors}
            )
        return None

    def _validate_type(self, value, expected_type: str) -> bool:
        """Validate value type"""
        type_checkers = {
            'string': lambda x: isinstance(x, str),
            'number': lambda x: isinstance(x, (int, float)),
            'boolean': lambda x: isinstance(x, bool),
            'array': lambda x: isinstance(x, list),
            'object': lambda x: isinstance(x, dict)
        }
        
        if expected_type not in type_checkers:
            return True
            
        return type_checkers[expected_type](value)
