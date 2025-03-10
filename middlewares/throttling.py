from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache
import time

class ThrottlingMiddleware(BaseMiddleware):
    """Ограничения частоты запросов от пользователей."""

    def __init__(self, rate_limit: float = 0.7):
        self.rate_limit = rate_limit
        self.cache = TTLCache(maxsize=10000, ttl=60)
        super().__init__()
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        if not isinstance(event, Message):
            return await handler(event, data)
        
        user_id = event.from_user.id
        
        current_time = time.time()
        
        if user_id in self.cache:
            last_request_time = self.cache[user_id]
            time_passed = current_time - last_request_time
            
            if time_passed < self.rate_limit:
                return None
        
        self.cache[user_id] = current_time
        

        return await handler(event, data)