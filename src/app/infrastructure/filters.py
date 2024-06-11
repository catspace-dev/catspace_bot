from aiogram.filters import Filter

from aiogram.types import Message, User


class ChatOnlyFilter(Filter):

    async def __call__(self, message: Message, event_from_user: User) -> bool:
        return True
