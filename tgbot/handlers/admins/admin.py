from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline.inline import AdminsInlineMarkup
from tgbot.models.users import User


async def admin_panel(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text('<b>🎛 Адменистративная паналь</b>',
                                 reply_markup=AdminsInlineMarkup().menu())


async def appoint_admin(message: Message, user: User):
    config: Config = message.bot.get('config')
    if str(message.from_user.id) in config.tg_bot.admin_ids:
        if user.admin:
            return await message.answer('Вы уже являетесь администратором')

        db_session = message.bot.get('db')
        await message.answer('Вы назначали себя администратором')
        await user.update_user(db_session, updated_fields={'admin': True})
        return


def register_admin_start(dp: Dispatcher):
    dp.register_message_handler(appoint_admin, commands=["appoint_admin"], state="*")
    dp.register_callback_query_handler(admin_panel, text="admin_panel")