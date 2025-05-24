from textwrap import dedent

from app.infrastructure.dao import BaseDAO
from app.infrastructure.dto.poll import AddPollVariantDTO, PollVariantDTO


class PollVariantDAO(BaseDAO):


    async def add(self, dto: AddPollVariantDTO):
        query = "INSERT INTO poll_variants (poll_id, user_id, chat_id, message_id, text) VALUES (?, ?, ?, ?, ?);"
        await self.db.connection.execute(
            query,
            (dto.poll_id, dto.user_id, dto.chat_id, dto.message_id, dto.text),
        )

    async def list(self, chat_id: int, poll_id: int):
        query = dedent("""
            SELECT 
                id, poll_id, user_id, chat_id, message_id, text
            FROM 
                poll_variants 
            WHERE chat_id = ? AND poll_id = ?;
        """)
        cursor = await self.db.connection.execute(query, (chat_id, poll_id))
        results = await cursor.fetchall()
        return [PollVariantDTO(**item) for item in results]


