from app.infrastructure.dao import BaseDAO
from app.infrastructure.dto.poll import AddPollVariantDTO


class PollVariantDAO(BaseDAO):


    async def add(self, dto: AddPollVariantDTO):
        query = "INSERT INTO poll_variants (poll_id, user_id, chat_id, message_id, text) VALUES (?, ?, ?, ?, ?);"
        await self.db.connection.execute(
            query,
            (dto.poll_id, dto.user_id, dto.chat_id, dto.message_id, dto.text),
        )


