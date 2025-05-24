from app.infrastructure.dao.polls.poll import PollDAO
from app.infrastructure.dto.poll import (
    CreatePollDTO,
    DeletePollDTO,
    PollFilterDTO,
    AddPollVariantDTO,
    PollDTO,
)
from app.infrastructure.exceptions.polls import (
    PollDoesNotExist,
    YouCantDeletePollWhichNotBelongToYou,
)


async def create_poll(dto: CreatePollDTO, dao: PollDAO) -> None:
    await dao.create(dto)
    await dao.db.connection.commit()


async def get_poll_list(chat_id: int, dao: PollDAO) -> str:
    result = "Опросы чата: \n"
    polls = await dao.list(chat_id)
    if not len(polls):
        return "В чате нет опросов!"
    for poll in polls:
        result += f"- {poll.name} ({poll.id})\n"
    return result

async def get_poll(dto: PollFilterDTO, dao: PollDAO) -> PollDTO | None:
    poll = await dao.get(dto)
    if not poll:
        raise PollDoesNotExist()
    return poll

async def remove_poll(dto: DeletePollDTO, dao: PollDAO) -> str:
    filter_dto = PollFilterDTO(poll_id=dto.poll_id, chat_id=dto.chat_id)
    poll = await get_poll(filter_dto, dao)
    if poll.creator_user_id != dto.issuer_id:
        raise YouCantDeletePollWhichNotBelongToYou()
    await dao.delete(filter_dto)
    await dao.db.connection.commit()
    return "Опрос удалён!"
