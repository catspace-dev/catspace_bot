from typing import Any, Awaitable, Callable, TYPE_CHECKING

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Chat

from app.infrastructure.dto.user import UserDTO

if TYPE_CHECKING:
    from app.infrastructure.container import AppContainer


class UserMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        container: AppContainer = data["container"]
        event_chat: Chat = data.get("event_chat")
        event_user: User = data.get("event_from_user")
        if bool(event_chat) and bool(event_user):
            result = await container.dao.users.is_exists(chat_id=event_chat.id, user_id=event_user.id)
            if not result:
                await container.dao.users.create(UserDTO(
                    telegram_id=event_user.id,
                    chat_id=event_chat.id,
                    full_name=event_user.full_name,
                    username=event_user.username
                ))
        result = await handler(event, data)
        return result
