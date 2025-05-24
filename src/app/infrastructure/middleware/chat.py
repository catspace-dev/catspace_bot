from typing import Callable, Awaitable, Any


from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Chat

class ChatWhitelistMiddleware(BaseMiddleware):
    def __init__(self, allowed_chat_ids: set[int]):
        self.allowed_chat_ids = allowed_chat_ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event_chat: Chat = data.get("event_chat")
        if event_chat:
            if event_chat.id not in self.allowed_chat_ids:
                return
            return await handler(event, data)
