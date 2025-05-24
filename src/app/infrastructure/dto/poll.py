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
