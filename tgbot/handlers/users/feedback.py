from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType

from tgbot.handlers.tools import tools_menu
from tgbot.keyboards.inline.itools import ToolsInlineMarkup
from tgbot.keyboards.inline.iusers import UsersInlineMarkup
from tgbot.misc.states import FeedbackStorage
from tgbot.models.users import User


async def start_feedback(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(
        '📨 Задай свой вопрос\n👥 Администраторы ответят Вам в течение 24 часов.\n\nОтправлять можно только текст❗️',
        reply_markup=ToolsInlineMarkup().back())

    async with state.proxy() as data:
        data['bot_id'] = call.message.message_id
    await FeedbackStorage.feedback_start.set()


async def feedback_statement_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        bot_message = data['bot_id']
        data['message'] = message.message_id

    await message.bot.edit_message_reply_markup(message.chat.id, bot_message, reply_markup=None)
    await message.answer(f'📩 Вы хотите отправить данное сообщения:\n▶ <code>{message.text}</code>',
                         reply_markup=ToolsInlineMarkup().negotiate())
    await FeedbackStorage.feedback_statement.set()


async def feedback_statement(call: CallbackQuery, state: FSMContext, user: User):
    config = call.bot.get('config')
    async with state.proxy() as data:
        user_message = data['message']

    await call.message.edit_text('📩 <b>Сообщение отправлено ожидайте ответа </b>☑')
    await call.bot.forward_message(chat_id=config.tg_bot.tech_groups, from_chat_id=call.message.chat.id,
                                   message_id=user_message)
    await state.finish()
    await call.message.answer('🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))


async def response_from_admins(message: Message):
    """Отправляем ответ пользователю"""
    if message.reply_to_message:
        await message.bot.send_message(chat_id=message.reply_to_message.forward_from.id,
                                       text='<b><i>----=== Ответ от администраторов ===----</i></b>\n\n' + message.text)
    else:
        await message.bot.send_message(chat_id=message.chat.id, text='Сделай Ответ, чтобы ответить автору')


def register_feedback(dp: Dispatcher):
    config = dp.bot.get('config')
    dp.register_callback_query_handler(start_feedback, text="feedback_user")
    dp.register_message_handler(feedback_statement_message, content_types=ContentType.TEXT,
                                state=FeedbackStorage.feedback_start)
    dp.register_callback_query_handler(feedback_statement, text="nego_confirm",
                                       state=FeedbackStorage.feedback_statement)
    dp.register_message_handler(response_from_admins, chat_id=config.tg_bot.tech_groups)
