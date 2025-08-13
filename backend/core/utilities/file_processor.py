import os
import csv
import json
from typing import Union, Dict, List
from pathlib import Path
from ..logging_setup import Logger
from ..error_handler import ErrorHandler

class FileProcessor:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        
    def read_file(self, file_path: str, format: str = 'auto') -> Union[Dict, List, str]:
        """Read file with automatic format detection"""
        try:
            if format == 'auto':
                format = self._detect_format(file_path)
                
            with open(file_path, 'r') as f:
                if format == 'json':
                    return json.load(f)
                elif format == 'csv':
                    return list(csv.DictReader(f))
                else:
                    return f.read()
                    
        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {str(e)}")
            raise ErrorHandler.handle_error(e)

    def write_file(self, data: Union[Dict, List, str], file_path: str, format: str = 'auto'):
        """Write data to file"""
        try:
            Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)
            
            if format == 'auto':
                format = self._detect_format(file_path)
                
            with open(file_path, 'w') as f:
                if format == 'json':
                    json.dump(data, f, indent=2)
                elif format == 'csv' and isinstance(data, list):
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    f.write(str(data))
                    
        except Exception as e:
            self.logger.error(f"Failed to write file {file_path}: {str(e)}")
            raise ErrorHandler.handle_error(e)

    def _detect_format(self, file_path: str) -> str:
        """Detect file format from extension"""
        ext = os.path.splitext(file_path)[1].lower()
        return {
            '.json': 'json',
            '.csv': 'csv',
            '.txt': 'text'
        }.get(ext, 'text')
