from aiogram import F, Router
from database import update_product_statistics
from aiogram.types import Message, PreCheckoutQuery

from core.config import ADMIN_ID

router = Router()


@router.pre_checkout_query()  # Подтверждение оплаты PayMaster
async def process_pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)


@router.message(F.successful_payment)  # Обработка успешной оплаты
async def successful_payment_handler(message: Message):
    payment = message.successful_payment
    amount = payment.total_amount / 100
    user_id = message.from_user.id
    username = message.from_user.username
    short_name = payment.invoice_payload.split('_')[1]

    await message.answer('<b>✅ Спасибо за оплату!</b>\n\n'
                         f'🛍️ <b>Товар: </b>{payment.invoice_payload}\n'
                         f'💳 <b>Сумма: </b>{amount} {payment.currency}\n\n'
                         'Мы свяжемся с вами или отправим товар в течение 24 часов!')

    for admin in ADMIN_ID:
        await message.bot.send_message(chat_id=admin, text=
        '<b>📬 Новая покупка!</b>\n\n'
        f'🛍️ <b>Товар: </b>{payment.invoice_payload}\n'
        f'💳 <b>Сумма: </b>{amount} {payment.currency}\n\n'
        f'👤 <b>Покупатель:</b> @{username} | ID: {user_id}')

    await update_product_statistics(short_name)
