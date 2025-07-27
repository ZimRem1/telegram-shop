from .connection import db

async def init_db():
    conn = await db.connect()
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT
        )
    ''')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_name TEXT,
            name TEXT,
            description TEXT,
            photo TEXT,
            price INTEGER,
            statistics INTEGER DEFAULT 0
        )
    ''')

    await conn.commit()
