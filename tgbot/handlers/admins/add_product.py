from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message, ContentType

from tgbot.keyboards.inline.itools import ToolsInlineMarkup
from tgbot.keyboards.inline.iusers import UsersInlineMarkup
from tgbot.misc.photo import photo_url
from tgbot.misc.states import AddProductStorage
from tgbot.models.products import Product
from tgbot.models.users import User


async def add_product_db(call: CallbackQuery, state: FSMContext):
    """Добавляем товары в Базу Данных"""
    await call.answer()
    await call.message.edit_text('✏️ Укажите название товара', reply_markup=ToolsInlineMarkup().cancel())
    await AddProductStorage.name.set()
    async with state.proxy() as data:
        data['bot_message'] = call.message.message_id


async def add_get_name(message: Message, state: FSMContext):
    bms = await message.answer('✏ Укажите описание товара', reply_markup=ToolsInlineMarkup().cancel())

    async with state.proxy() as data:
        msg = data['bot_message']
        data['product_name'] = message.text
        data['bot_message'] = bms.message_id
    await message.bot.edit_message_reply_markup(message.chat.id, msg)
    await AddProductStorage.description.set()


async def get_description(message: Message, state: FSMContext):
    bms = await message.answer('✏ Укажите стоимость товара.\nБез пробелов и других символов',
                               reply_markup=ToolsInlineMarkup().cancel())
    async with state.proxy() as data:
        msg = data['bot_message']
        data['product_description'] = message.text
        data['bot_message'] = bms.message_id
    await message.bot.edit_message_reply_markup(message_id=msg, chat_id=message.chat.id)
    await AddProductStorage.price.set()


async def get_price(message: Message, state: FSMContext):
    if message.text.isnumeric():
        bms = await message.answer('✏️️ Отправьте фотографию товара', reply_markup=ToolsInlineMarkup().cancel())
        await AddProductStorage.photo.set()
    else:
        bms = await message.answer('❌ Ошибка\n'
                                   'Укажите только цифры, без пробелом и других символов',
                                   reply_markup=ToolsInlineMarkup().cancel())
    async with state.proxy() as data:
        msg = data['bot_message']
        data['product_price'] = message.text
        data['bot_message'] = bms.message_id
    await message.bot.edit_message_reply_markup(message_id=msg, chat_id=message.chat.id)


async def get_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    url = await photo_url(photo)
    data = await state.get_data()
    bms = await message.answer_photo(url,
                                     f'<i>Информация которую указали:</i>\n\n'
                                     f'Наименование товара: <b><i>{data.get("product_name")}</i></b>\n'
                                     f'Описание товара: <b><i>{data.get("product_description")}</i></b>\n'
                                     f'Цена товара: <b><i>{data.get("product_price")}</i></b>\n'
                                     f'<b><i>Добавить товар?</i></b>',
                                     reply_markup=ToolsInlineMarkup().negotiate())
    async with state.proxy() as data:
        msg = data['bot_message']
        data['product_url'] = url
        data['bot_message'] = bms.message_id
    await message.bot.edit_message_reply_markup(message_id=msg, chat_id=message.chat.id)
    await AddProductStorage.expectations.set()


async def add_product_expectations(call: CallbackQuery, state: FSMContext, user: User):
    sessionmaker = call.bot.get('db')
    action = call.data.split("_")[1]
    data = await state.get_data()

    if action == 'cancel':
        await call.bot.edit_message_reply_markup(call.message.chat.id, data.get('bot_message'))
        await call.message.answer('❌ Вы отменили добавление товара!\n',
                                  reply_markup=UsersInlineMarkup().menu(user.admin))
    elif action == 'confirm':
        await Product.add_product(sessionmaker,
                                  name=data.get('product_name'),
                                  description=data.get('product_description'),
                                  price=int(data.get('product_price')),
                                  url_img=data.get('product_url'))

        await call.bot.edit_message_reply_markup(call.message.chat.id, data.get('bot_message'))
        await call.message.answer('✅ Товар успешно был добавлен!', reply_markup=UsersInlineMarkup().menu(user.admin))
    await state.finish()


def register_add_product(dp: Dispatcher):
    dp.register_callback_query_handler(add_product_db, text="add_product")
    dp.register_message_handler(add_get_name, state=AddProductStorage.name)
    dp.register_message_handler(get_description, state=AddProductStorage.description)
    dp.register_message_handler(get_price, state=AddProductStorage.price)
    dp.register_message_handler(get_photo, content_types=ContentType.PHOTO,
                                state=AddProductStorage.photo)
    dp.register_callback_query_handler(add_product_expectations, Text(startswith='nego_'),
                                       state=AddProductStorage.expectations)
