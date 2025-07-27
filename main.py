import asyncio
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from core.config import TOKEN
from handlers import payments_router, user_router, admin_router, add_product_router
from database import init_db

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


async def main():
    await init_db()
    dp.include_router(user_router)
    dp.include_router(add_product_router)
    dp.include_router(payments_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot, skip_updates=False)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот успешно выключен')
