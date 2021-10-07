from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline.inline import UsersInlineMarkup
from tgbot.models.users import User


async def tools_cancel(call: CallbackQuery, state: FSMContext, user: User):
    await call.answer('❌ Отменено', show_alert=True)
    await call.message.edit_text(f'🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))
    await state.finish()


async def tools_back(call: CallbackQuery, state: FSMContext, user: User):
    await call.answer()
    await call.message.edit_text(f'🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))
    await state.finish()


def setup_tools(dp: Dispatcher):
    dp.register_callback_query_handler(tools_cancel, text="cancel", state="*")
    dp.register_callback_query_handler(tools_back, text="back_button", state="*")
