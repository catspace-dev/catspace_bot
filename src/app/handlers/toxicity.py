from aiogram.types import Message

from app.features.toxicity import ToxicClassificationService, ToxicStatsService
from app.infrastructure.container import AppContainer

# TODO: фильтр - ток в чате на все эти ручки


async def process_toxic_classification(msg: Message, container: AppContainer) -> None:
    if msg.text:
        classificator = ToxicClassificationService(
            tokenizer=container.toxic_container.get_tokenizer(),
            model=container.toxic_container.get_model(),
            dao=container.dao.toxicity,
            pool=container.toxic_container.get_pool()
        )
        await classificator.execute(msg.from_user.id, msg.chat.id, msg.text)


async def on_toxicity_command(msg: Message, container: AppContainer) -> None:
    result = await ToxicStatsService(container.dao.toxicity).execute(msg.chat.id)
    await msg.reply(result)
