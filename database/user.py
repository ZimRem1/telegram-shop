from .connection import db

async def add_user(user_id: int, full_name: str, username: str):
    conn = await db.connect()
    await conn.execute('INSERT OR IGNORE INTO users (user_id, full_name, username) VALUES (?, ?, ?)',
                       (user_id, full_name, username))
    await conn.commit()
