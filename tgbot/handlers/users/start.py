from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline.inline import UsersInlineMarkup
from tgbot.misc.states import StorageUsers
from tgbot.models.users import User


async def user_start(message: Message, user: User, state: FSMContext):
    """Начало работы бота с пользователем"""

    if user.passed:
        return await message.answer(f"Здравствуйте, {message.from_user.get_mention()}!\n",
                                    reply_markup=UsersInlineMarkup().menu(user.admin))

    sessionmaker = message.bot.get('db')
    code = message.text if not message.is_command() else message.get_args()
    if not code or code == "connect_user":
        return await message.answer(f'❌ У Вас нет доступа!\n'
                                    f'Чтобы использовать этого бота введите код приглашения, '
                                    f'либо пройдите по реферальной ссылке\n',
                                    reply_markup=UsersInlineMarkup().register())

    if not code.isdigit():
        return await message.answer('❌ Ошибка\nДанная ссылка недействительна.',
                                    reply_markup=UsersInlineMarkup().register())

    check_user = await user.get_user(sessionmaker, int(code))
    if int(code) == user.telegram_id or check_user is None:
        return await message.answer('❌ Ошибка\nДанная ссылка недействительна.',
                                    reply_markup=UsersInlineMarkup().register())

    await state.update_data(referrer_user=check_user)
    await StorageUsers.register_user.set()
    await user_registration(message, state, user)


async def invite_code_input(call: CallbackQuery):
    """Пользователь начал вводить код приглашения"""
    await call.message.edit_text("✏️ Введите код приглашения:")
    await StorageUsers.invite_code.set()


async def invite_code_check(message: Message, state: FSMContext, user: User):
    """Проверяем код приглашения пользователя"""
    sessionmaker = message.bot.get('db')
    invite_code = await user.get_user_code(sessionmaker, message.text)

    if invite_code is None or message.text == user.invite_code:
        await state.finish()
        return await message.answer("❌ Ошибка\nДанный код не был найден, проверьте на правильность его ввода",
                                    reply_markup=UsersInlineMarkup().register())

    await state.update_data(referrer_user=invite_code)
    await StorageUsers.register_user.set()
    await user_registration(message, state, user)


async def user_registration(message: Message, state: FSMContext, user: User):
    """Завершения регистрации пользователя"""
    sessionmaker = message.bot.get('db')
    data = await state.get_data()
    bot_username = (await message.bot.me).username
    invite_user = data.get("referrer_user")

    await user.update_user(sessionmaker, updated_fields={'passed': True})
    await user.update_user(sessionmaker, telegram_id=int(invite_user.telegram_id),
                           updated_fields={'balance': invite_user.balance + 10})
    await Referral.add_user(sessionmaker, message.from_user.id, invite_user.telegram_id)
    await message.bot.send_message(invite_user.telegram_id,
                                   f'Вы получили 10 бонус рублей!\n'
                                   f'За приглашеного пользователя {message.from_user.get_mention()}\n'
                                   f'Ваш баланс: {invite_user.balance + 10} ₽')

    await message.answer(f'Поздравляю, вы получили доступ! 🎉\n'
                         f'Вы были приглашены пользователем '
                         f'<a href="tg://user?id={invite_user.telegram_id}">{invite_user.full_name}</a>\n'
                         f'Вы можете получить 10 бонусых рублей, если пригласите рефералов\n'
                         f'Ваша реферальная ссылка: t.me/{bot_username}?start={message.from_user.id}',
                         reply_markup=await get_user_menu(user.admin))
    await state.finish()


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_callback_query_handler(invite_code_input, text="invitation_code")
    dp.register_message_handler(invite_code_check, state=StorageUsers.invite_code)
    dp.register_message_handler(user_registration, state=StorageUsers.register_user)
