from typing import Callable, Any, Awaitable

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Update

from app.handlers.me import on_me_command
from app.handlers.polls import on_polls_command
from app.handlers.toxicity import process_toxic_classification, on_toxicity_command
from app.infrastructure.exceptions.base import AppException

async def app_exception_middleware(
    handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: dict[str, Any]
) -> Any:
    try:
        return await handler(event, data)
    except AppException as ex:
       await event.reply(ex.reason)



def prepare_router() -> Router:
    router = Router()
    # general
    router.message.register(on_me_command, Command("me"))
    router.message.register(on_toxicity_command, Command("toxics"))
    router.message.register(process_toxic_classification)
    router.message.register(on_polls_command, Command("polls"))
    router.message.middleware(app_exception_middleware)
    return router
