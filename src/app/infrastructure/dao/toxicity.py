from app.infrastructure.dao import BaseDAO
from app.infrastructure.dto.toxicity import ToxicStatsDTO


class ToxicityDAO(BaseDAO):

    async def add(self, user_id: int, chat_id: int, toxicity: float) -> None:
        query = "INSERT INTO toxicity (user_id, chat_id, toxicity) VALUES (?, ?, ?);"
        await self.db.connection.execute(query, (user_id, chat_id, toxicity))
        await self.db.connection.commit()

    async def get_stats(self, chat_id: int) -> list[ToxicStatsDTO]:
        query = """
            WITH stats AS (
                SELECT
                    toxicity.user_id AS user_id,
                    users.full_name as full_name,
                    COUNT(toxicity.toxicity) FILTER ( WHERE toxicity.toxicity >= 0.80 ) * 1.0 AS toxic_count,
                    COUNT(toxicity.toxicity) * 1.0 AS all_count
                FROM
                     toxicity
                JOIN users on toxicity.chat_id = users.chat_id AND toxicity.user_id == users.telegram_id
                WHERE toxicity.chat_id == ?
            
                GROUP BY toxicity.user_id
            )
            
            SELECT
                stats.user_id AS user_id,
                stats.full_name as full_name,
                stats.toxic_count / stats.all_count AS toxic_ratio
            FROM
                 stats
            WHERE toxic_ratio != 0
            ORDER BY toxic_ratio DESC
            LIMIT 5
        """

        cursor = await self.db.connection.execute(query, (chat_id, ))
        results = await cursor.fetchall()
        return [ToxicStatsDTO(telegram_id=item[0], full_name=item[1], toxic_ratio=item[2]) for item in results]
