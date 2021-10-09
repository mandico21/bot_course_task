from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.inline.itools import ToolsInlineMarkup
from tgbot.misc.states import AddProductStorage


async def add_get_name(call: CallbackQuery, state: FSMContext):
    """Добавляем товары в Базу Данных"""
    await call.answer()
    await call.message.edit_text(f'✏️ Укажите название товара', reply_markup=ToolsInlineMarkup().cancel())
    await AddProductStorage.name.set()
    async with state.proxy() as data:
        data['bot_message'] = call.message.message_id


async def get_description(message: Message, state: FSMContext):
    bms = await message.answer(f'✏️ Укажите название описание', reply_markup=ToolsInlineMarkup().cancel())

    async with state.proxy() as data:
        msg = data['bot_message']
        data['product_name'] = message.text
        data['bot_message'] = bms.message_id
    await message.bot.edit_message_reply_markup(message.chat.id, msg)
    await AddProductStorage.description.set()


async def get_price(message: Message, state: FSMContext):
    bms = await message.answer('✏️ Введите стоимость товара', reply_markup=ToolsInlineMarkup().cancel())
    async with state.proxy() as data:
        msg = data['bot_message']
        data['product_description'] = message.text
        data['bot_message'] = bms.message_id
    await message.bot.edit_message_reply_markup(message_id=msg, chat_id=m.chat.id)
    await AddProductStorage.price.set()


async def get_photo(message: Message, state: FSMContext):
    if message.text.isnumeric():
        bms = await message.answer('✏️ Отправьте фотографию товара', reply_markup=ToolsInlineMarkup().cancel())
        await AddItem.photo.set()
    else:
        bms = await message.answer('✏️ Введите верную стоимость товара', reply_markup=ToolsInlineMarkup().cancel())
    async with state.proxy() as data:
        msg = data['bot_message']
        data['product_price'] = message.text
        data['bot_message'] = bms.message_id
    await message.bot.edit_message_reply_markup(message_id=msg, chat_id=m.chat.id)


def register_add_product(dp: Dispatcher):
    dp.register_callback_query_handler(add_get_name, text="add_product")
    dp.register_message_handler(get_description, state=AddProductStorage.name)
    dp.register_message_handler(get_price, state=AddProductStorage.description)
    dp.register_message_handler(get_photo, state=AddProductStorage.price)
