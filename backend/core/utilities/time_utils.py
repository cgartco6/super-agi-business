from datetime import datetime, timedelta
import pytz
from typing import Optional, Union
from ..logging_setup import Logger

class TimeUtils:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        
    def now(self, timezone: str = 'UTC') -> datetime:
        """Get current time in specified timezone"""
        try:
            tz = pytz.timezone(timezone)
            return datetime.now(tz)
        except pytz.UnknownTimeZoneError:
            self.logger.warning(f"Unknown timezone: {timezone}")
            return datetime.now(pytz.UTC)

    def format_duration(self, seconds: Union[int, float]) -> str:
        """Format duration as human-readable string"""
        periods = [
            ('year', 60*60*24*365),
            ('month', 60*60*24*30),
            ('day', 60*60*24),
            ('hour', 60*60),
            ('minute', 60),
            ('second', 1)
        ]
        
        parts = []
        for period_name, period_seconds in periods:
            if seconds >= period_seconds:
                period_value, seconds = divmod(seconds, period_seconds)
                plural = 's' if period_value > 1 else ''
                parts.append(f"{int(period_value)} {period_name}{plural}")
                
        return ', '.join(parts) if parts else '0 seconds'

    def parse_date(self, date_str: str, timezone: Optional[str] = None) -> datetime:
        """Parse date string with timezone support"""
        try:
            dt = datetime.fromisoformat(date_str)
            if timezone:
                tz = pytz.timezone(timezone)
                if dt.tzinfo is None:
                    return tz.localize(dt)
                return dt.astimezone(tz)
            return dt
        except ValueError as e:
            self.logger.error(f"Failed to parse date {date_str}: {str(e)}")
            raise
