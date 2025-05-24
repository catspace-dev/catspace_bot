from app.infrastructure.dao.polls.poll import PollDAO
from app.infrastructure.dao.polls.poll_variant import PollVariantDAO
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

async def add_poll_variant(dto: AddPollVariantDTO, poll_dao: PollDAO, poll_variant_dao: PollVariantDAO) -> None:
    await get_poll(PollFilterDTO(poll_id=dto.poll_id, chat_id=dto.chat_id), poll_dao)
    await poll_variant_dao.add(dto)
    await poll_variant_dao.db.connection.commit()

async def get_poll_variants(dto: PollFilterDTO, poll_dao: PollDAO, poll_variant_dao: PollVariantDAO) -> str:
    poll = await get_poll(dto=dto, dao=poll_dao)
    variants = await poll_variant_dao.list(chat_id=dto.chat_id, poll_id=dto.poll_id)
    if not len(variants):
        return f'В опросе "{poll.name}" нет вариантов!'
    result = f'Варианты опроса "{poll.name}": \n'
    for variant in variants:
        result += f"- {variant.to_link()} ({variant.id})\n"
    return result
