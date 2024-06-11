from aiogram import Router
from aiogram.filters import Command

from app.handlers.me import on_me_command
from app.handlers.toxicity import process_toxic_classification, on_toxicity_command


def prepare_router() -> Router:
    router = Router()
    # general
    router.message.register(on_me_command, Command("me"))
    router.message.register(on_toxicity_command, Command("toxics"))
    router.message.register(process_toxic_classification)
    return router
