import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline.iadmins import AdminsInlineMarkup
from tgbot.keyboards.inline.itools import ToolsInlineMarkup
from tgbot.keyboards.inline.iusers import UsersInlineMarkup
from tgbot.misc.states import SettingsUserStorage
from tgbot.models.users import User


def show_text(profile):
    text = f'📌 ID: <b><i>{profile.telegram_id}</i></b>\n' \
           f'🔹 ФИО: <b><i>{profile.full_name}</i></b>\n' \
           f'🔸 Имя пользователя: <b><i>{profile.username}</i></b>\n' \
           f'🎟 Код приглашения: <b><i>{profile.invite_code}</i></b>\n' \
           f'💰 Баланс: <b><i>{profile.balance}</i></b>\n' \
           f'👤 Админка: <b><i>{profile.admin}</i></b>\n' \
           f'♻️ Регистрация: <b><i>{profile.passed}</i></b>\n' \
           f'🕐 Дата начала: <b><i>{profile.created_at.strftime("%d-%m-%Y")}</i></b>\n'
    return text


async def show_profile_user(message: Message, user: User, state: FSMContext, deep_link):
    sessionmaker = message.bot.get('db')
    user_id = int(deep_link[0].split('-')[1])
    check_user = await user.get_user(sessionmaker, user_id)

    if check_user is None:
        return await message.answer('❌ Ошибка!\nПользователя с данным ID не найдено')

    await message.answer(text=show_text(check_user),
                         reply_markup=AdminsInlineMarkup().user(check_user.admin))
    await state.update_data(customer=check_user)


async def settings_admin_user(call: CallbackQuery, user: User, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        customer = data['customer']
    sessionmaker = call.bot.get('db')

    if call.data == 'add_admin_user':
        await user.update_user(sessionmaker, telegram_id=int(customer.telegram_id),
                               updated_fields={'admin': True})
        await call.message.edit_text(f'✅ Вы успешно назначили администратором '
                                     f'<a href="tg://user?id={customer.telegram_id}">{customer.full_name}</a>!')
    elif call.data == 'delete_admin_user':
        await user.update_user(sessionmaker, telegram_id=int(customer.telegram_id),
                               updated_fields={'admin': False})
        await call.message.edit_text(f'✅ Вы успешно отобрали права администратора у '
                                     f'<a href="tg://user?id={customer.telegram_id}">{customer.full_name}</a>!')

    customer = await user.get_user(sessionmaker, int(customer.telegram_id))
    await call.message.answer(text=show_text(customer),
                              reply_markup=AdminsInlineMarkup().user(customer.admin))


async def first_add_money(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Укажите <b>баланс</b> для пользователя',
                                 reply_markup=ToolsInlineMarkup().cancel())
    await SettingsUserStorage.edit_users_price.set()
    await state.update_data(b_msg=call.message.message_id)


async def add_money_user(message: Message, state: FSMContext, user: User):
    async with state.proxy() as data:
        msg = data['b_msg']
        customer = data['customer']

    try:
        int(message.text)
    except ValueError:
        await message.bot.edit_message_reply_markup(message.chat.id, msg)
        b_msg = await message.answer('❌ Ошибка\n🔖 Количество товара должно быть в цифрах!',
                                     reply_markup=ToolsInlineMarkup().cancel())
        await state.update_data(b_msg=b_msg.message_id)
        return

    sessionmaker = message.bot.get('db')
    message.text = int(message.text)
    await message.bot.edit_message_reply_markup(message.chat.id, msg)
    await user.update_user(sessionmaker, telegram_id=int(customer.telegram_id),
                           updated_fields={'balance': message.text})
    await message.answer(f'✅ Вы успешно отредактировали баланс пользователю '
                         f'<a href="tg://user?id={customer.telegram_id}">{customer.full_name}</a>!')
    customer = await user.get_user(sessionmaker, int(customer.telegram_id))
    await message.answer(text=show_text(customer),
                         reply_markup=AdminsInlineMarkup().user(customer.admin))
    await state.reset_state(with_data=False)


def register_settings_user(dp: Dispatcher):
    dp.register_message_handler(show_profile_user, CommandStart(deep_link=re.compile(r'^user_id-\d+$')))
    dp.register_callback_query_handler(settings_admin_user, text={"add_admin_user", "delete_admin_user"})
    dp.register_callback_query_handler(first_add_money, text="user_add_money")
    dp.register_message_handler(add_money_user, state=SettingsUserStorage.edit_users_price)
