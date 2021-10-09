from aiogram import Dispatcher
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
    db_session = query.bot.get('db')
    check_show_items = int(query.offset) if query.offset else 0
    item_check = await Product.get_all_product(db_session, query.query, check_show_items)
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


def register_istart(dp: Dispatcher):
    dp.register_inline_handler(show_inline_products, state="*")
