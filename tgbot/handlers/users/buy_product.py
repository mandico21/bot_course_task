from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from tgbot.config import Config
from tgbot.keyboards.inline.itools import ToolsInlineMarkup
from tgbot.keyboards.inline.iusers import UsersInlineMarkup
from tgbot.misc.qiwi import create_payment, check_payment
from tgbot.misc.states import BuyProductStorage
from tgbot.models.products import Product
from tgbot.models.users import User


async def beginning_purchase_products(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        data['item_id'] = callback_data['item_id']

    await call.message.edit_text('✏️ Укажите количество товара')
    await BuyProductStorage.beginning_product.set()


async def get_quantity(message: Message, state: FSMContext, user: User):
    if message.text.isnumeric() and int(message.text) > 0:
        async with state.proxy() as data:
            item_id = data['item_id']
            data['product_quantity'] = message.text
        sessionmaker = message.bot.get('db')
        quantity = await Product.get_product(sessionmaker, int(item_id))

        if int(message.text) <= quantity.quantity:
            await message.answer('🏠 Укажите адрес доставки\nГород, улицу, дом')
            await BuyProductStorage.get_delivery_adress.set()
        else:
            await message.answer(f'❌ Ошибка!\nНе хватает товара на складе\nВ наличие {quantity.quantity} шт')
            if quantity.quantity == 0:
                await state.finish()
                await message.answer(f'🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))
    else:
        await message.answer('❌ Ошибка!\nУкажите верное количество товара')


async def get_address(message: Message, state: FSMContext, user: User):
    if message.text.isnumeric():
        return await message.answer('❌ Ошибка!\nАдрес не может состоять только из цифр!')

    await message.answer(f'✅ Отлично!\nОсталось оплатить товар!\n\n💰 Ваш баланс: {user.balance} ₽',
                         reply_markup=ToolsInlineMarkup().product_payment())
    async with state.proxy() as data:
        data['product_address'] = message.text
    await BuyProductStorage.payment_product.set()


async def send_message_admin(product, obj, quantity, address, user_mention):
    config: Config = obj.bot.get('config').tg_bot

    for admin in config.admin_ids:
        await obj.bot.send_message(admin,
                                   f'🎉 Новая покупка!\n'
                                   f'👤 Покупатель: {user_mention}\n'
                                   f'🏠 Адрес доставки: {address}\n'
                                   f'📫 Артикл: <b><i>{product.item_id}</i></b>\n'
                                   f'📌 Название: <b><i>{product.name}</i></b>\n'
                                   f'💎 Количество: <b><i>{quantity}</i></b>\n'
                                   f'💰 Цена: <b><i>{product.price * quantity} ₽</i></b>')


async def payment_product(call: CallbackQuery, state: FSMContext, user: User):
    async with state.proxy() as data:
        item_id = data['item_id']
        quantity = data['product_quantity']
        address = data['product_address']

    sessionmaker = call.bot.get('db')
    await call.answer()
    product = await Product.get_product(sessionmaker, int(item_id))
    amount = int(product.price) * int(quantity)
    action = call.data.split("_")[2]

    if action != "qiwi":
        if user.balance >= int(amount):
            await user.update_user(sessionmaker, updated_fields={'balance': user.balance - int(amount)})
            await Product.update_product(sessionmaker, product.item_id,
                                         updated_fields={'quantity': int(product.quantity) - int(quantity)})
            await call.message.edit_text(f'🎉 Поздравляем с покупкой!\n'
                                         f'✅ Товар <b><i>{product.name}</i></b> успешно был оплачен!\n'
                                         f'🕑 Ожидайте доставку товара по адресу {address}')
            await call.message.answer(f'🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))
            await state.finish()
            await send_message_admin(product, call, int(quantity), address, call.from_user.get_mention())
            return

        await call.message.answer('❌ Ошибка!\nНа вашем балансе недостаточно средвст!')

    if int(amount - user.balance) <= 0:
        payment = await create_payment(amount=1, obj=call)
        await call.message.edit_text(f'📌 Оплата через Qiwi!\n'
                                     f'💳 Сумма к оплате: <b><i>{1} ₽</i></b>\n\n'
                                     f'❗️ <i>У Вас есть 10 минут, чтобы оплатить товар</i>',
                                     reply_markup=ToolsInlineMarkup().product_payment_qiwi(payment.pay_url,
                                                                                           payment.bill_id))
    else:
        payment = await create_payment(amount=int(amount - user.balance), obj=call)
        await call.message.edit_text(f'📌 Оплата через Qiwi!\n'
                                     f'💳 Сумма к оплате: <b><i>{amount - user.balance} ₽</i></b>\n\n'
                                     f'❗️ <i>У Вас есть 10 минут, чтобы оплатить товар</i>',
                                     reply_markup=ToolsInlineMarkup().product_payment_qiwi(payment.pay_url,
                                                                                           payment.bill_id))
    await BuyProductStorage.check_payment.set()


async def check_payment_product(call: CallbackQuery, state: FSMContext, callback_data: dict, user: User):
    async with state.proxy() as data:
        item_id = data['item_id']
        quantity = data['product_quantity']
        address = data['product_address']

    sessionmaker = call.bot.get('db')
    bill_id = callback_data['bill_id']
    check = await check_payment(bill_id, call)
    product = await Product.get_product(sessionmaker, int(item_id))
    amount = int(product.price) * int(quantity)

    if check != 'PAID':
        return await call.answer(f'❌ Оплата не найдена!', show_alert=True)

    await user.update_user(sessionmaker, updated_fields={'balance': user.balance - amount})
    await Product.update_product(sessionmaker, product.item_id, updated_fields={'quantity': product.quantity - quantity})
    await call.message.edit_text(f'🎉 Поздравляем с покупкой!\n'
                                 f'✅ Товар <b><i>{product.name}</i></b> успешно был оплачен!\n'
                                 f'🕑 Ожидайте доставку товара по адресу {address}')
    await call.message.answer(f'🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))
    await state.finish()
    await send_message_admin(product, call, int(quantity), address, call.from_user.get_mention())


def register_buy_product(dp: Dispatcher):
    dp.register_callback_query_handler(beginning_purchase_products, ToolsInlineMarkup.buy_pod.filter())
    dp.register_message_handler(get_quantity, state=BuyProductStorage.beginning_product)
    dp.register_message_handler(get_address, state=BuyProductStorage.get_delivery_adress)
    dp.register_callback_query_handler(payment_product, Text(startswith="to_pay"),
                                       state=BuyProductStorage.payment_product)
    dp.register_callback_query_handler(check_payment_product, ToolsInlineMarkup.bill_cd.filter(),
                                       state=BuyProductStorage.check_payment)
