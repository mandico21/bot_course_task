from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.inline.iusers import UsersInlineMarkup
from tgbot.models.users import User


async def tools_cancel(call: CallbackQuery, state: FSMContext, user: User):
    await call.answer('❌ Отменено', show_alert=True)
    await state.finish()
    await call.message.edit_text('🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))


async def tools_back(call: CallbackQuery, state: FSMContext, user: User):
    await call.answer()
    await state.finish()
    await call.message.edit_text('🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))


async def tools_menu(message: Message, user: User):
    await message.answer('🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))


def setup_tools(dp: Dispatcher):
    dp.register_callback_query_handler(tools_cancel, text=["cancel", "nego_cancel"], state="*")
    dp.register_callback_query_handler(tools_back, text="back_button", state="*")
    dp.register_message_handler(tools_menu, commands=["menu"])
