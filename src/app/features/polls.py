from app.infrastructure.dao.polls.poll import PollDAO
from app.infrastructure.dao.polls.poll_variant import PollVariantDAO
from app.infrastructure.dto.poll import (
    CreatePollDTO,
    DeletePollDTO,
    PollFilterDTO,
    AddPollVariantDTO,
    PollDTO,
    PollVariantFilterDTO,
    PollVariantDTO,
)
from app.infrastructure.exceptions.polls import (
    PollDoesNotExist,
    YouCantDeletePollWhichNotBelongToYou,
    PollVariantDoesNotExist,
    YouCantDeletePollVariantWhichNotBelongToYou,
)
from app.settings import ADMINS


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
    if not (poll.creator_user_id == dto.issuer_id or dto.issuer_id not in ADMINS):
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

async def get_poll_variant(dto: PollVariantFilterDTO, dao: PollVariantDAO) -> PollVariantDTO | None:
    variant = await dao.get(dto)
    if not variant:
        raise PollVariantDoesNotExist()
    return variant

async def remove_poll_variant(
    issuer_id: int,
    dto: PollVariantFilterDTO,
    poll_dao: PollDAO,
    poll_variant_dao: PollVariantDAO
) -> str:
    poll = await get_poll(dto=dto.to_poll_filter(), dao=poll_dao)
    variant = await get_poll_variant(dto=dto, dao=poll_variant_dao)
    if not (variant.user_id == issuer_id or issuer_id in ADMINS):
        raise YouCantDeletePollVariantWhichNotBelongToYou()
    await poll_variant_dao.delete(variant.id)
    await poll_variant_dao.db.connection.commit()
    return f"Вариант {variant.to_link()} в опросе {poll.name} удалён."
