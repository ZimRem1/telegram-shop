from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from kb import admin_panel, build_delete_keyboard
from database import get_statistics, delete_product
from core.config import ADMIN_ID

router = Router()


@router.message(Command('admin'))
async def admin_handler(message: Message):
    if message.from_user.id in ADMIN_ID:
        await message.answer('<b>Добро пожаловать в админ панель бота</b>\n\nВыберете что вам нужно',
                             reply_markup=admin_panel)


@router.callback_query(F.data == 'statistics')
async def statistics_handler(callback: CallbackQuery):
    await callback.answer()
    if not await get_statistics():
        await callback.message.answer('📊 Статистика пуста. Пока ни один товар не был продан')
        return

    text = '<b>📊 Статистика продаж товаров:</b>\n\n'
    for name, count in await get_statistics():
        text += f"<b>{name}</b>: {count} раз(а)\n"
    await callback.message.answer(text)


@router.callback_query(F.data == 'delete_product')
async def delete_keyboard(callback: CallbackQuery):
    await callback.answer()
    keyboard = await build_delete_keyboard()

    if not keyboard.inline_keyboard:
        await callback.message.edit_text("📭 Нет товаров для удаления")
        return

    await callback.message.edit_text("🗑 Выберите товар для удаления:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("delete_"))
async def process_delete_product(callback: CallbackQuery):
    await callback.answer()
    product_id = int(callback.data.split("_")[1])
    await delete_product(product_id)
    await callback.message.answer("Товар удалён")
    await callback.message.edit_reply_markup(reply_markup=await build_delete_keyboard())
