from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import get_short_name_product, get_products

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🗂 Каталог'),
     KeyboardButton(text='👤 Поддержка')],
    [KeyboardButton(text='📌 О нас')]
], resize_keyboard=True)


async def category():
    builder = InlineKeyboardBuilder()

    for product in await get_short_name_product():
        builder.add(InlineKeyboardButton(text=product, callback_data=f'product_{product}'))
    return builder.adjust(2).as_markup()


admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✔️ Добавить товар', callback_data='add_product'),
     InlineKeyboardButton(text='🗑 Удалить товар', callback_data='delete_product')],
    [InlineKeyboardButton(text='📊 Статистика', callback_data='statistics')]
])

abort_creation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отменить создание товара', callback_data='cancel_product')]
])

product_confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Готово, все хорошо', callback_data='confirm_product')],
    [InlineKeyboardButton(text='❌ Отмена, мне не нравится', callback_data='cancel_product')]
])


def generate_product_kb(short_name: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💸 Купить', callback_data=f'buy_{short_name}')],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='catalog')]
    ])


async def build_delete_keyboard():
    builder = InlineKeyboardBuilder()

    for product_id, name, price in await get_products():
        builder.add(InlineKeyboardButton(text=f"{name} — {price} ₽", callback_data=f"delete_{product_id}"))
    return builder.adjust(1).as_markup()
