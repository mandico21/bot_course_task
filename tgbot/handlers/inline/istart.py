from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.markdown import hide_link

from tgbot.keyboards.inline.itools import ToolsInlineMarkup
from tgbot.models.products import Product
from tgbot.models.users import User


async def show_inline_products(query: InlineQuery, user: User):
    if not user.passed:
        return await query.answer(
            results=[],
            switch_pm_text='Бот недоступен. Подключите бота',
            switch_pm_parameter='connect_user',
            cache_time=5)
    sessionmaker = query.bot.get('db')
    check_show_items = int(query.offset) if query.offset else 0
    item_check = await Product.get_all_product(sessionmaker, query.query, check_show_items)
    list_item = [InlineQueryResultArticle(
        id=items.item_id,
        title=items.name,
        description=f'{items.price} ₽',
        thumb_url=items.url_img,
        input_message_content=InputTextMessageContent(
            message_text=f'{hide_link(items.url_img)}'
                         f'📌 Название: <b><i>{items.name}</i></b>\n'
                         f'📝 Описание: <b><i>{items.description}</i></b>\n'
                         f'💰 Цена: <b><i>{items.price} ₽</i></b>'
        ), reply_markup=ToolsInlineMarkup().show_product(str((await query.bot.get_me()).username), str(items.item_id))
    ) for items in item_check]
    await query.answer(
        results=list_item,
        cache_time=60,
        next_offset=str(check_show_items + 20)
    )


async def show_inline_users(query: InlineQuery, user: User):
    if not user.passed:
        return await query.answer(
            results=[],
            switch_pm_text='Бот недоступен. Подключите бота',
            switch_pm_parameter='connect_user',
            cache_time=5)
    action = query.query.split("-")[1]
    sessionmaker = query.bot.get('db')
    users_check = await user.get_all_user(sessionmaker, action)
    list_item = [InlineQueryResultArticle(
        id=users.telegram_id,
        title=users.full_name,
        description=f'Админ: {users.admin}/ Регистрация: {users.passed}',
        input_message_content=InputTextMessageContent(
            message_text=f'💰 ID: <b><i>{users.telegram_id}</i></b>\n'
                         f'📌 Имя: <b><i>{users.full_name}</i></b>'
        ), reply_markup=ToolsInlineMarkup().check_user(str((await query.bot.get_me()).username), str(users.telegram_id))
    ) for users in users_check]
    await query.answer(
        results=list_item,
        cache_time=60
    )


def register_istart(dp: Dispatcher):
    dp.register_inline_handler(show_inline_users, Text(startswith="users-"), is_admin=True)
    dp.register_inline_handler(show_inline_products)
