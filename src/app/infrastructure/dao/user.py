from app.infrastructure.dao import BaseDAO
from app.infrastructure.dto.user import UserDTO


class UserDAO(BaseDAO):

    async def create(self, user: UserDTO):
        query = "INSERT INTO users (telegram_id, chat_id, full_name, username) VALUES (?, ?, ?, ?);"
        await self.db.connection.execute(query, (user.telegram_id, user.chat_id, user.full_name, user.username))
        await self.db.connection.commit()

    async def is_exists(self, chat_id: int, user_id: int):
        query = """
        SELECT 
            telegram_id 
        FROM 
            users
        WHERE 
            telegram_id = ? AND chat_id = ?
        """

        cursor = await self.db.connection.execute(query, (user_id, chat_id))
        return bool(await cursor.fetchone())

