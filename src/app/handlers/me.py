from aiogram.types import Message


async def on_me_command(msg: Message) -> None:
    await msg.delete()
    _, action = msg.text.split(' ', 1)
    await msg.answer(f"<i>* {msg.from_user.full_name} {action}</i>")
