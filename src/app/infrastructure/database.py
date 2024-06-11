import aiosqlite


class DatabaseWrapper:

    def __init__(self, connection: aiosqlite.Connection):
        self.connection = connection

    @classmethod
    async def create(cls, path: str) -> "DatabaseWrapper":
        connection = await aiosqlite.connect(path)
        # await connection.execute("PRAGMA foreign_keys=ON") - ну потом включу, как бд буду переделывать
        return cls(connection)

    async def close(self):
        await self.connection.close()
