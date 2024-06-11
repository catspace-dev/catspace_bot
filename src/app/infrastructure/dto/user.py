from dataclasses import dataclass


@dataclass
class UserDTO:
    telegram_id: int
    chat_id: int
    full_name: str
    username: str | None
