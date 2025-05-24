from textwrap import dedent

from aiogram.types import Message

from app.features.polls import (
    create_poll,
    get_poll_list,
    remove_poll,
    add_poll_variant,
    get_poll_variants,
    remove_poll_variant,
    post_poll,
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
    if len(parts) <= 1:
        await on_polls_help(msg)
        return
    action = parts[1]
    match action:
        case "create": await on_poll_create_command(msg, container)
        case "list": await on_poll_list_command(msg, container)
        case "remove": await on_poll_delete_command(msg, container)
        case "variants": await on_poll_variants_command(msg, container)
        case "post": await on_poll_post_command(msg, container)


async def on_polls_help(msg: Message) -> None:
    text = dedent("""
    Этот модуль позволяет создавать пользовательские опросы, в которые каждый может добавлять свои варианты.
    
    *Команды*:
    - `/polls create <Название опроса>` - cоздаст опрос с именем "Название опроса".
    - `/polls list` - выведет список опросов для этого чата.
    - `/polls remove <id>` - удалит опрос с номером `<id>`.
    - `/polls post <id>` - запостит опрос с номером `<id>` как обычный Telegram-опрос.
    - `/polls variants add <poll_id>` - добавит вариант в опрос с номером `<poll_id>`. Нужно использовать как ответ на сообщение, которое вы хотите добавить в опрос.
    - `/polls variants list <poll_id>` - покажет варианты для опроса с номером `<poll_id>`.
    - `/polls variants remove <poll_id> <variant_id>` - удалит вариант опроса `<variant_id>` у опроса `<poll_id>`.
    
    *Пошаговый пример использования*:
    - Создаете опрос командой `/polls create лучшие котики`.
    - Находите его номер через `/polls list` (допустим это 1).
    - Постите котика и добавляете к нему подпись.
    - Отвечаете на картинку с котиком командой `/polls variants add 1`.
    - Постите сам опрос - `/polls post 1`.
    """)
    await msg.reply(text, parse_mode="Markdown")

async def on_poll_post_command(msg: Message, container: AppContainer) -> None:

    try:
        _, _, poll_id = msg.text.split(" ", 2)
    except ValueError:
        await msg.reply("Использование: /polls post `<id>`", parse_mode="Markdown")
        return

    await post_poll(
        issuer=msg.from_user.id,
        dto=PollFilterDTO(poll_id=poll_id, chat_id=msg.chat.id),
        poll_dao=container.dao.polls,
        poll_variant_dao=container.dao.poll_variants,
        bot=msg.bot,
    )


async def on_poll_create_command(msg: Message, container: AppContainer) -> None:
    try:
        _, _, name = msg.text.split(" ", 2)
    except ValueError:
        await msg.reply("Использование: /polls create `<название опроса>`", parse_mode="Markdown")
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
        await msg.reply("Использование: /polls remove `<id>`", parse_mode="Markdown")
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
        await msg.reply("Использование: /polls variants add `<poll_id>`", parse_mode="Markdown")
        return

    if not msg.reply_to_message:
        await msg.reply(
            "Используйте эту команду как ответ на сообщение, которое вы хотите добавить в опрос. "
            "\nУ сообщения обязательно должен быть текст или подпись (если это медиа)!"
        )
        return

    text = msg.reply_to_message.text or msg.reply_to_message.caption

    if not text:
        await msg.reply("У сообщения обязательно должен быть текст или подпись!")
        return

    dto = AddPollVariantDTO(
        poll_id=poll_id,
        user_id=msg.from_user.id,
        chat_id=msg.chat.id,
        message_id=msg.reply_to_message.message_id,
        text=text
    )

    await add_poll_variant(dto, container.dao.polls, container.dao.poll_variants)
    await msg.reply("Вариант добавлен!")
    return

async def on_poll_variants_list(msg: Message, container: AppContainer) -> None:

    try:
        _, _, _, poll_id = msg.text.split(" ", 3)
    except ValueError:
        await msg.reply("Использование: /polls variants list `<poll_id>`", parse_mode="Markdown")
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
        await msg.reply("Использование: /polls variants remove `<poll_id>` `<variant_id>`", parse_mode="Markdown")
        return

    await msg.reply(await remove_poll_variant(
        issuer_id=msg.from_user.id,
        dto=PollVariantFilterDTO(variant_id=variant_id, chat_id=msg.chat.id, poll_id=poll_id),
        poll_dao=container.dao.polls,
        poll_variant_dao=container.dao.poll_variants
    ))


