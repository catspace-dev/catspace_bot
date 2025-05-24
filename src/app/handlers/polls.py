from aiogram.types import Message

from app.features.polls import (
    create_poll,
    get_poll_list,
    remove_poll,
    add_poll_variant,
    get_poll_variants,
    remove_poll_variant,
)
from app.infrastructure.container import AppContainer
from app.infrastructure.dto.poll import (
    CreatePollDTO,
    DeletePollDTO,
    AddPollVariantDTO,
    PollFilterDTO,
    PollVariantFilterDTO,
)


async def on_polls_command(msg: Message, container: AppContainer) -> None:
    parts = msg.text.split(" ")
    if len(parts) < 1:
        return
    action = parts[1]
    match action:
        case "create": await on_poll_create_command(msg, container)
        case "list": await on_poll_list_command(msg, container)
        case "remove": await on_poll_delete_command(msg, container)
        case "variants": await on_poll_variants_command(msg, container)

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


async def on_poll_variants_command(msg: Message, container: AppContainer) -> None:
    parts = msg.text.split(" ")
    if len(parts) == 2:
        await msg.reply("Список: add, list, remove")
        return
    action = parts[2]
    match action:
        case "add": await on_poll_variants_add(msg, container)
        case "list": await on_poll_variants_list(msg, container)
        case "remove": await on_poll_variant_remove(msg, container)

async def on_poll_variants_add(msg: Message, container: AppContainer) -> None:
    try:
        _, _, _, poll_id = msg.text.split(" ", 3)
    except ValueError:
        await msg.reply("Использование: /poll variants add `<poll_id>`", parse_mode="Markdown")
        return

    if not msg.reply_to_message:
        await msg.reply(
            "Используйте эту команду как ответ на сообщение, которое вы хотите добавить в опрос. "
            "\nУ сообщения обязательно должен быть текст или подпись (если это медиа)!"
        )
        return

    dto = AddPollVariantDTO(
        poll_id=poll_id,
        user_id=msg.from_user.id,
        chat_id=msg.chat.id,
        message_id=msg.reply_to_message.message_id,
        text=msg.reply_to_message.text or msg.reply_to_message.caption
    )

    await add_poll_variant(dto, container.dao.polls, container.dao.poll_variants)
    await msg.reply("Вариант добавлен!")
    return

async def on_poll_variants_list(msg: Message, container: AppContainer) -> None:

    try:
        _, _, _, poll_id = msg.text.split(" ", 3)
    except ValueError:
        await msg.reply("Использование: /poll variants list `<poll_id>`", parse_mode="Markdown")
        return

    text = await get_poll_variants(
        dto=PollFilterDTO(poll_id=poll_id, chat_id=msg.chat.id),
        poll_dao=container.dao.polls,
        poll_variant_dao=container.dao.poll_variants
    )
    await msg.reply(text)

async def on_poll_variant_remove(msg: Message, container: AppContainer) -> None:
    try:
        _, _, _, poll_id, variant_id = msg.text.split(" ", 4)
    except ValueError:
        await msg.reply("Использование: /poll variants remove `<poll_id>` `<variant_id>`", parse_mode="Markdown")
        return

    await msg.reply(await remove_poll_variant(
        issuer_id=msg.from_user.id,
        dto=PollVariantFilterDTO(variant_id=variant_id, chat_id=msg.chat.id, poll_id=poll_id),
        poll_dao=container.dao.polls,
        poll_variant_dao=container.dao.poll_variants
    ))


