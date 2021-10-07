from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram_broadcaster import MessageBroadcaster

from tgbot.keyboards.inline.inline import ToolsInlineMarkup, UsersInlineMarkup
from tgbot.misc.states import MailingStorage
from tgbot.models.users import User


async def start_mailing(call: CallbackQuery):
    await call.message.edit_text('📢 <b>Введите текст для рассылки пользователям:</b>')
    await MailingStorage.mailing_start.set()


async def progressing_mailing(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['here_send_ad'] = message

    await message.answer(f'📢 Вы хотите отправить сообщение:\n'
                         f'▶ <code>{message.text}</code>\n',
                         reply_markup=ToolsInlineMarkup().negotiate())
    await MailingStorage.progressing.set()


async def mailing_launch(call: CallbackQuery, state: FSMContext, user: User):
    async with state.proxy() as data:
        text = data['here_send_ad']
    action = call.data.split("_")[1]
    sessionmaker = call.bot.get('db')

    if action == 'cancel':
        await state.finish()
        await call.message.edit_text(f'<b>❌ Вы отменили отправку рассылки</b>')
        await call.message.answer(f'<b>🎛 Административная панель</b>',
                                  reply_markup=UsersInlineMarkup().menu(user.admin))
    elif action == 'confirm':
        users = await user.get_all_user(sessionmaker)
        await call.answer('📢 Рассылка началась...', show_alert=True)

        broadcaster = MessageBroadcaster(users, message=text)
        await broadcaster.run()

        await call.message.delete()
        await call.message.answer(f'<b>🎛 Административная панель</b>',
                                  reply_markup=UsersInlineMarkup().menu(user.admin))
        await call.message.answer(f'📢 <b>Рассылка была завершена ☑</b>\n\n'
                                  f'👤 Пользователей получили сообщение: <code>{len(broadcaster._successful)}</code> ✅\n'
                                  f'👤 Пользователей заблокировали бота: <code>{int(len(broadcaster.chats) - len(broadcaster._successful))}</code> ❌')
        await state.finish()



def register_mailing(dp: Dispatcher):
    dp.register_callback_query_handler(start_mailing, text="mailing")
    dp.register_message_handler(progressing_mailing, state=MailingStorage.mailing_start)
    dp.register_callback_query_handler(mailing_launch, Text(startswith="nego_"), state=MailingStorage.progressing)