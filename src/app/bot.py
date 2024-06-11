import asyncio
import logging
from typing import cast

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers import prepare_router
from app.infrastructure.container import ToxicContainer, AppContainer
from app.infrastructure.database import DatabaseWrapper
from app.infrastructure.user import UserMiddleware
from app.settings import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def on_startup(dispatcher: Dispatcher) -> None:
    logger.info("Setup middlewares")
    dispatcher.update.middleware(UserMiddleware())
    dispatcher.include_router(prepare_router())


async def on_shutdown(dispatcher: Dispatcher) -> None:
    logging.warning("Shutting down...")
    container: AppContainer = dispatcher["container"]
    await container.finalize()
    logging.warning("Container finalized...")

    await dispatcher.storage.close()
    logging.warning("Bye!")


async def main() -> None:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    bot = Bot(token=cast(str, TELEGRAM_BOT_TOKEN), default=DefaultBotProperties(parse_mode="HTML"))
    container = await AppContainer.create()
    await dp.start_polling(
        bot, container=container
    )


if __name__ == "__main__":
    asyncio.run(main())
