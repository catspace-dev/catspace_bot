from aiogram.types import Message

from app.features.polls import create_poll, get_poll_list, remove_poll
from app.infrastructure.container import AppContainer
from app.infrastructure.dto.poll import CreatePollDTO, DeletePollDTO


async def on_polls_command(msg: Message, container: AppContainer) -> None:
    parts = msg.text.split(" ")
    if len(parts) > 1: action = parts[1]
    match action:
        case "create": await on_poll_create_command(msg, container)
        case "list": await on_poll_list_command(msg, container)
        case "remove": await on_poll_delete_command(msg, container)

async def on_poll_create_command(msg: Message, container: AppContainer) -> None:
    try:
        _, _, name = msg.text.split(" ", 2)
    except ValueError:
        await msg.reply("Использование: /poll create `<название опроса>`", parse_mode="Markdown")
        return

    await create_poll(CreatePollDTO(msg.from_user.id, msg.chat.id, name), container.dao.polls)
    await msg.reply(f"Опрос создан: `{name}`", parse_mode="Markdown")

async def on_poll_list_command(msg: Message, container: AppContainer) -> None:
    result = await get_poll_list(msg.chat.id, container.dao.polls)
    await msg.reply(result)

async def on_poll_delete_command(msg: Message, container: AppContainer) -> None:
    try:
        _, _, poll_id = msg.text.split(" ", 2)
    except ValueError:
        await msg.reply("Использование: /poll remove `<id>`", parse_mode="Markdown")
        return

    try:
        poll_id = int(poll_id)
    except ValueError:
        await msg.reply("ID опроса должен быть целым числом!")
        return

    result = await remove_poll(DeletePollDTO(
        issuer_id=msg.from_user.id,
        poll_id=poll_id,
        chat_id=msg.chat.id
    ), container.dao.polls)
    await msg.reply(result)
