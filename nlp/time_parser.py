import re
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class TimeParser:
    """Класс для парсинга временных выражений из текста"""

    def __init__(self):
        self.time_patterns = [
            # через X минут/часов/дней
            (r'через (\d+) (минут[уы]?|час[ао]в?|дн[еяй])', self._parse_relative_time),
            (r'в (\d{1,2}[:.]\d{2})', self._parse_absolute_time),
            (r'в (\d{1,2}) час[ао]?в?( (\d{1,2}) минут)?', self._parse_hours_minutes),
            (r'завтра в (\d{1,2}[:.]\d{2})', self._parse_tomorrow_time),
            (r'завтра в (\d{1,2}) час[ао]?в?', self._parse_tomorrow_hour),
            (r'сегодня в (\d{1,2}[:.]\d{2})', self._parse_absolute_time),
            (r'через (час|минуту|день)', self._parse_single_unit),
        ]
        
    def parse_time(self, text: str) -> Optional[Tuple[datetime, str]]:
        """Извлекает время из текста и возвращает его вместе с очищенным текстом."""
        text_lower = text.lower()
        
        for pattern, parser in self.time_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    time_obj = parser(match)
                    if time_obj:
                        # Удаляем найденное временное выражение из текста
                        clean_text = re.sub(pattern, '', text_lower, count=1).strip() 
                        clean_text = re.sub(r'^(напомни|напомнить)\s+', '', clean_text).strip()
    
                        if not clean_text:
                            clean_text = "Напоминание"
                        return time_obj, clean_text
                except Exception as e:
                    logger.error(f"Ошибка при парсинге времени: {e}")
        
        return None
    
    def _parse_relative_time(self, match) -> Optional[datetime]:
        """Парсинг относительного времени."""
        amount = int(match.group(1))
        unit = match.group(2)
        
        now = datetime.now()
        
        if unit.startswith('минут'):
            return now + timedelta(minutes=amount)
        elif unit.startswith('час'):
            return now + timedelta(hours=amount)
        elif unit.startswith('дн'):
            return now + timedelta(days=amount)
        
        return None
    
    def _parse_absolute_time(self, match) -> Optional[datetime]:
        """Парсинг абсолютного времени (в ЧЧ:ММ)"""
        time_str = match.group(1).replace('.', ':')
        
        try:
            hours, minutes = map(int, time_str.split(':'))
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                return None
                
            now = datetime.now()
            time_today = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            
            if time_today < now:
                time_today += timedelta(days=1)
                
            return time_today
        except ValueError:
            return None
    
    def _parse_hours_minutes(self, match) -> Optional[datetime]:
        """Парсинг времени вида 'в ЧЧ часов ММ минут'"""
        hours = int(match.group(1))
        minutes = int(match.group(3)) if match.group(3) else 0
        
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            return None
            
        now = datetime.now()
        time_today = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        
        if time_today < now:
            time_today += timedelta(days=1)
            
        return time_today
    
    def _parse_tomorrow_time(self, match) -> Optional[datetime]:
        """Парсинг времени (завтра в ЧЧ:ММ)"""
        time_str = match.group(1).replace('.', ':')
        
        try:
            hours, minutes = map(int, time_str.split(':'))
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                return None
                
            now = datetime.now()
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        except ValueError:
            return None
    
    def _parse_tomorrow_hour(self, match) -> Optional[datetime]:
        """Парсинг времени (завтра в ЧЧ часов)"""
        hours = int(match.group(1))
        
        if not (0 <= hours <= 23):
            return None
            
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=hours, minute=0, second=0, microsecond=0)
    
    def _parse_single_unit(self, match) -> Optional[datetime]:
        """Парсинг единичных временных выражений"""
        unit = match.group(1)
        now = datetime.now()
        
        if unit == 'час':
            return now + timedelta(hours=1)
        elif unit == 'минуту':
            return now + timedelta(minutes=1)
        elif unit == 'день':
            return now + timedelta(days=1)
        
        return None