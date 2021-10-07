from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.inline.inline import UsersInlineMarkup
from tgbot.models.users import User


async def show_referral(call: CallbackQuery, user: User):
    await call.answer()
    sessionmaker = call.bot.get('db')
    bot_username = await call.bot.me
    count_referrals = await user.count_referrals(sessionmaker, user)

    await call.message.edit_text(f'💎 Количество рефералов: {count_referrals}\n'
                                 f'💰 Баланс: {user.balance} ₽\n'
                                 f'🎟 Ваш код приглашения: {user.invite_code}\n'
                                 f'🎫 Ваша реферальная ссылка: t.me/{bot_username.username}?start={call.from_user.id}\n',
                                 reply_markup=UsersInlineMarkup().referral(user.invite_code))


async def install_referral_code(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(f'✏️ Введите свое кодовое слово\n'
                              f'Максимальная длина кода 5 символов\n'
                              f'Код можно будет установить лишь 1 раз. Поменять или обновить его не получится!')
    await state.set_state('invite_install')


async def install_referral_code2(message: Message, state: FSMContext, user: User):
    if len(message.text) > 5:
        return await message.answer(f'❌ Ошибка\nДлина более 5 символов\n'
                                    f'Введите кодовое слово корректно!')

    sessionmaker = message.bot.get('db')
    code_check = await user.get_user_code(sessionmaker, str(message.text))
    if code_check is not None:
        return await message.answer(f'❌ Ошибка\nЭто кодовое слово уже занято!\n'
                                    f'Попробуйте придумать другое кодовое слово.\n')

    await user.update_user(sessionmaker, updated_fields={'invite_code': message.text})
    await message.answer(f'✅ Вы успешно установили кодовое слово!\n'
                         f'<i><b>➡️ {message.text}</b></i>')
    await message.answer(f'🗂 <b>Главное меню</b>', reply_markup=UsersInlineMarkup().menu(user.admin))
    await state.finish()


def register_referral(dp: Dispatcher):
    dp.register_callback_query_handler(show_referral, text="referrer_user")
    dp.register_callback_query_handler(install_referral_code, text="install_referral_code")
    dp.register_message_handler(install_referral_code2, state="invite_install")
