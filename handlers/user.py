from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile, LabeledPrice

from kb import menu, category, generate_product_kb
from database import add_user, get_product
from core.config import PAYMASTER

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    image = FSInputFile('assets/welcome.png')
    await message.answer_photo(image, caption='Добро пожаловать в наш магазин!\nЧто вас интересует?',
                               reply_markup=menu)
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)


@router.message(F.text == '🗂 Каталог')
async def catalog_handler(message: Message):
    await message.answer('💻 Выберите необходимый сервис для покупки', reply_markup=await category())


@router.callback_query(F.data == 'catalog')
async def catalog_data_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('💻 Выберите необходимый сервис для покупки',
                                  reply_markup=await category())


@router.message(F.text == '👤 Поддержка')
async def support(message: Message):
    await message.answer('Тех. поддержка - @ZimRem | Время работы 10:00-22:00')


@router.message(F.text == '📌 О нас')
async def about(message: Message):
    await message.answer(
        'Мы великий телеграмм магазин с продажей самых лучших товаров\n\nНаши истоки уходят в глубокие истории')


@router.callback_query(F.data.startswith('product_'))
async def show_product_card(callback: CallbackQuery):
    await callback.message.delete()
    short_name = callback.data.split('_')[1]
    name, description, photo, price = await get_product(short_name)
    await callback.message.answer_photo(photo=photo,
                                        caption=f'<b>{name}</b>\n\n{description}\n\n<b>Цена:</b> {price} ₽',
                                        reply_markup=generate_product_kb(short_name))


@router.callback_query(F.data.startswith('buy_'))
async def view_product(callback: CallbackQuery):
    await callback.message.delete()
    short_name = callback.data.split('_')[1]
    name, _, _, price = await get_product(short_name)
    prices = [LabeledPrice(label='RUB', amount=price * 100)]

    await callback.message.answer_invoice(
        title=short_name,
        description=name,
        payload=f'order_{short_name}_{callback.from_user.id}',
        provider_token=PAYMASTER,
        currency='RUB',
        prices=prices,
        start_parameter='buy_product'
    )
