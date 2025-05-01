from app.infrastructure.dao.polls.poll import PollDAO
from app.infrastructure.dto.poll import CreatePollDTO, DeletePollDTO, PollFilterDTO


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

async def remove_poll(dto: DeletePollDTO, dao: PollDAO) -> str:
    filter_dto = PollFilterDTO(poll_id=dto.poll_id, chat_id=dto.chat_id)
    poll = await dao.get(filter_dto)
    if not poll:
        return "Такого опроса не существует."
    if poll.creator_user_id != dto.issuer_id:
        return "Вы не можете удалить опрос который вам не принадлежит."
    await dao.delete(filter_dto)
    await dao.db.connection.commit()
    return "Опрос удалён!"
