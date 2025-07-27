# handlers/admin/add_product.py

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from core.states.states import ProductCreation
from kb import product_confirm_kb, abort_creation
from database import add_product


router = Router()

@router.callback_query(F.data == 'add_product')
async def add_short_name_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ProductCreation.short_name)
    await callback.message.edit_text(
        '<b>Вам будут заданы 5 вопросов:</b>\n\n'
        '1. Короткое имя товара (пример - Spotify)\n'
        '2. Полное имя товара (пример - 🎬 Netflix Premium – 30 дней)\n'
        '3. Описание\n'
        '4. Картинка\n'
        '5. Цену\n\n'
        '1/5 Введите короткое название нового товара (оно будет использоваться на кнопках)',
        reply_markup=abort_creation)

@router.message(ProductCreation.short_name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(short_name=message.text)
    await state.set_state(ProductCreation.name)
    await message.answer('2/5 Введите полное название с преимуществами нового товара\n\nПример: 🎬 Netflix Premium – 30 дней',
                         reply_markup=abort_creation)

@router.message(ProductCreation.name)
async def add_product_description(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ProductCreation.description)
    await message.answer('3/5 Введите описание нового товара', reply_markup=abort_creation)

@router.message(ProductCreation.description)
async def add_product_photo(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(ProductCreation.photo)
    await message.answer('4/5 Скиньте фотку в формате 16:9 для товара', reply_markup=abort_creation)

@router.message(ProductCreation.photo, F.photo)
async def add_product_price(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await state.set_state(ProductCreation.price)
    await message.answer('5/5 Сколько будет стоить один товар? (напишите <b>только</b> число)', reply_markup=abort_creation)

@router.message(ProductCreation.price)
async def product_example(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await message.answer('Как будет выглядеть карточка товара:')
    await message.answer_photo(
        data['photo'],
        f"<b>{data['name']}</b>\n\n{data['description']}\n\nЦена: {data['price']} ₽",
        reply_markup=product_confirm_kb)

@router.callback_query(F.data == 'confirm_product')
async def confirm_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await add_product(data['short_name'], data['name'], data['description'], data['photo'], data['price'])
    await callback.message.delete()
    await callback.message.answer("✔️ Карточка товара успешно добавлена!")
    await callback.answer()

@router.callback_query(F.data == 'cancel_product')
async def cancel_product(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("❌ Добавление товара отменено")
    await callback.answer()
