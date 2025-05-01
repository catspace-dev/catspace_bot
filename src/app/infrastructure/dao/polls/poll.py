from app.infrastructure.dao import BaseDAO
from app.infrastructure.dto.poll import (
    CreatePollDTO,
    PollListItemDTO,
    PollFilterDTO,
    PollDTO,
)


class PollDAO(BaseDAO):

    async def create(self, dto: CreatePollDTO):
        query = "INSERT INTO polls (creator_user_id, chat_id, name) VALUES (?, ?, ?);"
        await self.db.connection.execute(
            query,
            (dto.creator_user_id, dto.chat_id, dto.name)
        )

    async def list(self, chat_id: int):
        query = "SELECT id, name FROM polls WHERE chat_id = ?;"
        cursor = await self.db.connection.execute(query, (chat_id, ))
        results = await cursor.fetchall()
        return [PollListItemDTO(id=item[0], name=item[1]) for item in results]

    async def get(self, dto: PollFilterDTO) -> PollDTO | None:
        query = "SELECT id, creator_user_id, chat_id, name FROM polls WHERE id = ? AND chat_id = ?;"
        cursor = await self.db.connection.execute(query, (dto.poll_id, dto.chat_id))
        result = await cursor.fetchone()
        if result:
            return PollDTO(id=result[0], creator_user_id=result[1], chat_id=result[2], name=result[3])
        else: return None


    async def delete(self, dto: PollFilterDTO) -> None:
        query = "DELETE FROM polls WHERE id = ? AND chat_id = ?;"
        await self.db.connection.execute(query, (dto.poll_id, dto.chat_id))
