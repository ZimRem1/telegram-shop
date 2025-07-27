import aiosqlite

class Database:
    def __init__(self, path: str):
        self.path = path
        self._connection = None

    async def connect(self):
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.path)
            await self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None

db = Database("database/database.db")
