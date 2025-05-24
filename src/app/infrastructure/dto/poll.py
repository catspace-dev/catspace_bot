from dataclasses import dataclass


@dataclass
class CreatePollDTO:
    creator_user_id: int
    chat_id: int
    name: str


@dataclass
class PollListItemDTO:
    id: int
    name: str

@dataclass
class DeletePollDTO:
    issuer_id: int
    poll_id: int
    chat_id: int

@dataclass
class PollFilterDTO:
    poll_id: int
    chat_id: int

@dataclass
class PollDTO:
    id: int
    creator_user_id: int
    chat_id: int
    name: str

@dataclass
class AddPollVariantDTO:
    poll_id: int
    user_id: int
    chat_id: int
    message_id: int
    text: str

@dataclass
class PollVariantDTO:
    id: int
    poll_id: int
    user_id: int
    chat_id: int
    message_id: int
    text: str

    def to_link(self):
        return f'https://t.me/c/{abs(self.chat_id + 1_000_000_000_000)}/{self.message_id}'

    def to_html_link(self):
        return f'<a href="{self.to_link()}">{self.text}</a>'


@dataclass
class PollVariantFilterDTO:
    variant_id: int
    poll_id: int
    chat_id: int

    def to_poll_filter(self) -> PollFilterDTO:
        return PollFilterDTO(poll_id=self.poll_id, chat_id=self.chat_id)
