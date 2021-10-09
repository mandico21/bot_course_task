import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hide_link

from tgbot.handlers.tools import tools_menu
from tgbot.keyboards.inline.iadmins import AdminsInlineMarkup
from tgbot.keyboards.inline.itools import ToolsInlineMarkup
from tgbot.misc.states import EditProductStorage
from tgbot.models.products import Product
from tgbot.models.users import User


async def edit_product_search(call: CallbackQuery, callback_data: dict, state: FSMContext):
    sessionmaker = call.bot.get('db')

    check_product = await Product.get_product(sessionmaker, int(callback_data['item_id']))
    if check_product is None:
        return await call.message.answer('❌ Ошибка!\nТовар который вы заращиваете не найден')

    await state.finish()
    await call.message.edit_text(f'{hide_link(check_product.url_img)}'
                                 f'📫 Артикл: <b><i>{check_product.item_id}</i></b>\n'
                                 f'📌 Название: <b><i>{check_product.name}</i></b>\n'
                                 f'💎 Количество: <b><i>{check_product.quantity}</i></b>\n'
                                 f'📝 Описание: <b><i>{check_product.description}</i></b>\n'
                                 f'💰 Цена: <b><i>{check_product.price} ₽</i></b>',
                                 reply_markup=AdminsInlineMarkup().edit())
    await state.update_data(product_editing=check_product,
                            b_msg=call.message.message_id)


async def first_edit_product_name(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['b_msg']

    await call.bot.edit_message_reply_markup(call.message.chat.id, msg)
    await call.message.answer('✏️ Укажите новое название товара')
    await EditProductStorage.edit_product_name.set()


async def edit_product_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        product = data['product_editing']

    sessionmaker = message.bot.get('db')
    await Product.update_product(sessionmaker, int(product.item_id),
                                 updated_fields={"name": message.text})
    await message.answer('✅ Вы успешно изменили название товара!')
    await state.finish()
    await tools_menu(message, User)


async def first_edit_product_description(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['b_msg']

    await call.bot.edit_message_reply_markup(call.message.chat.id, msg)
    await call.message.answer('✏️ Укажите новое описание товара')
    await EditProductStorage.edit_product_description.set()


async def edit_product_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        product = data['product_editing']

    sessionmaker = message.bot.get('db')
    await Product.update_product(sessionmaker, int(product.item_id),
                                 updated_fields={"description": message.text})
    await message.answer('✅ Вы успешно изменили описание товара!')
    await state.finish()
    await tools_menu(message, User)


async def catching_editing(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['b_msg']

    await call.bot.edit_message_reply_markup(call.message.chat.id, msg)
    await call.message.answer(f'🔺 Чтобы увеличить кол-во товара, напишите число\n'
                              f'Например: 2, кол-во товара станет на 2 единицы больше\n'
                              f'🔻 Чтобы уменьшить кол-во товара, напишите число с отрицательным знаком \n'
                              f'Например: -2, кол-во товара станет на 2 единицы меньше')

    await EditProductStorage.edit_product_quantity.set()


async def catching_editing_quantity(message: Message, state: FSMContext):
    if not re.fullmatch(r'[-]?\d+', message.text):
        return await message.answer(f'❌ Ошибка\nПопробуйте снова!')

    async with state.proxy() as data:
        product = data['product_editing']

    sessionmaker = message.bot.get('db')
    await Product.update_product(sessionmaker, int(product.item_id),
                                 updated_fields={"quantity": product.quantity + int(message.text)})

    await message.answer('✅ Вы успешно изменили количество товара!')
    await state.finish()
    await tools_menu(message, User)


async def first_edit_product_price(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        msg = data['b_msg']

    await call.bot.edit_message_reply_markup(call.message.chat.id, msg)
    await call.message.answer('✏️ Укажите новую цену товара')
    await EditProductStorage.edit_product_price.set()


async def edit_product_price(message: Message, state: FSMContext):
    if not message.text.isnumeric():
        return await message.answer('❌ Ошибка\n'
                                    'Укажите только цифры, без пробелом и других символов')

    async with state.proxy() as data:
        product = data['product_editing']

    sessionmaker = message.bot.get('db')
    await Product.update_product(sessionmaker, int(product.item_id),
                                 updated_fields={"price": int(message.text)})
    await message.answer('✅ Вы успешно изменили цену товара!')
    await state.finish()
    await tools_menu(message, User)


def register_edit_product(dp: Dispatcher):
    dp.register_callback_query_handler(edit_product_search, ToolsInlineMarkup.edit_call.filter())
    dp.register_callback_query_handler(first_edit_product_name, text='edit_name')
    dp.register_message_handler(edit_product_name, state=EditProductStorage.edit_product_name)
    dp.register_callback_query_handler(first_edit_product_description, text='edit_description')
    dp.register_message_handler(edit_product_description, state=EditProductStorage.edit_product_description)
    dp.register_callback_query_handler(catching_editing, text='edit_quantity')
    dp.register_message_handler(catching_editing_quantity, state=EditProductStorage.edit_product_quantity)
    dp.register_callback_query_handler(first_edit_product_price, text='edit_price')
    dp.register_message_handler(edit_product_price, state=EditProductStorage.edit_product_price)
