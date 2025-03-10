import re
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class IntentRecognizer:
    """Класс распознавания намерений"""
    
    def __init__(self):
        self.reminder_patterns = [
            r'^напомни(ть)?(\s+мне)?',
            r'^создай(\s+мне)?(\s+напоминание)?',
            r'^установи(\s+мне)?(\s+напоминание)?',
            r'не\s+забыть(\s+бы)?',
            r'нужно(\s+будет)?(\s+не)?(\s+забыть)?',
            r'надо(\s+будет)?(\s+не)?(\s+забыть)?',
        ]
        
        self.cancel_patterns = [
            r'^отмени(ть)?(\s+напоминание)?',
            r'^удали(ть)?(\s+напоминание)?',
        ]
        
        self.list_patterns = [
            r'^(покажи|посмотреть|выведи|список)(\s+мои|\s+все)?(\s+напоминания)?',
            r'^какие(\s+у\s+меня)?(\s+есть)?(\s+напоминания)?',
        ]
    
    def recognize_intent(self, text: str) -> Optional[Dict[str, Any]]:
        text_lower = text.lower().strip()
        
        for pattern in self.reminder_patterns:
            if re.search(pattern, text_lower):
                return {
                    'intent': 'create_reminder',
                    'text': text
                }
        
        for pattern in self.cancel_patterns:
            if re.search(pattern, text_lower):
                return {
                    'intent': 'cancel_reminder',
                    'text': text
                }
        
        for pattern in self.list_patterns:
            if re.search(pattern, text_lower):
                return {
                    'intent': 'list_reminders'
                }
        
        time_indicators = [
            'через', 'в ', ' в ', 'завтра', 'сегодня', 'час', 'минут', 'утром', 'вечером',
            'днем', 'ночью', '00:', '01:', '02:', '03:', '04:', '05:', '06:', '07:', '08:', '09:',
            '10:', '11:', '12:', '13:', '14:', '15:', '16:', '17:', '18:', '19:', '20:', '21:', '22:', '23:'
        ]
        
        for indicator in time_indicators:
            if indicator in text_lower:
                return {
                    'intent': 'create_reminder',
                    'text': text
                }
        
        return None