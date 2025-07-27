from .connection import db


async def add_product(short_name, name, description, photo, price):
    conn = await db.connect()
    await conn.execute(
        'INSERT INTO products (short_name, name, description, photo, price) VALUES (?, ?, ?, ?, ?)',
        (short_name, name, description, photo, price)
    )
    await conn.commit()


async def get_product(short_name):
    conn = await db.connect()
    cursor = await conn.execute(
        'SELECT name, description, photo, price FROM products WHERE short_name = ?',
        (short_name,)
    )
    return await cursor.fetchone()


async def get_short_name_product():
    conn = await db.connect()
    cursor = await conn.execute('SELECT short_name FROM products')
    rows = await cursor.fetchall()
    return [row[0] for row in rows]


async def update_product_statistics(short_name: str):
    conn = await db.connect()
    await conn.execute('UPDATE products SET statistics = statistics + 1 WHERE short_name = ?',
                       (short_name,))
    await conn.commit()


async def get_statistics():
    conn = await db.connect()
    cursor = await conn.execute(
        'SELECT name, statistics FROM products WHERE statistics >= 1 ORDER BY statistics DESC')
    rows = await cursor.fetchall()
    await cursor.close()
    return rows


async def get_products():
    conn = await db.connect()
    cursor = await conn.execute("SELECT id, name, price FROM products")
    rows = await cursor.fetchall()
    await cursor.close()
    return rows


async def delete_product(product_id: int):
    conn = await db.connect()
    await conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    await conn.commit()
