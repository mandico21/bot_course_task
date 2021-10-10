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


async def show_profile_user(message: Message, user: User, state: FSMContext, deep_link):
    sessionmaker = message.bot.get('db')
    user_id = int(deep_link[0].split('-')[1])
    check_user = await user.get_user(sessionmaker, user_id)

    if check_user is None:
        return await message.answer('❌ Ошибка!\nПользователя с данным ID не найдено')

    await message.answer(f'ID: <b><i>{check_user.telegram_id}</i></b>\n'
                         f'ФИО: <b><i>{check_user.full_name}</i></b>\n'
                         f'Имя пользователя: <b><i>{check_user.username}</i></b>\n'
                         f'Код приглашения: <b><i>{check_user.invite_code}</i></b>\n'
                         f'Баланс: <b><i>{check_user.balance}</i></b>\n'
                         f'Админка: <b><i>{check_user.admin}</i></b>\n'
                         f'Регистрация: <b><i>{check_user.passed}</i></b>\n'
                         f'Дата начала: <b><i>{check_user.created_at.strftime("%d-%m-%Y")}</i></b>\n',
                         reply_markup=AdminsInlineMarkup().user(check_user.admin))
    await state.update_data(customer=check_user)


async def first_add_money(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(f'🔺 Чтобы увеличить кол-во денег, напишите число\n'
                                 f'Например: 2, кол-во денег станет на 2 рубля больше\n'
                                 f'🔻 Чтобы уменьшить кол-во денег, напишите число с отрицательным знаком \n'
                                 f'Например: -2, кол-во денег станет на 2 рубля меньше',
                                 reply_markup=ToolsInlineMarkup().cancel())
    await SettingsUserStorage.edit_users_price.set()
    await state.update_data(b_msg=call.message.message_id)


async def add_money_user(message: Message, state: FSMContext, user: User):
    async with state.proxy() as data:
        msg = data['b_msg']
        customer = data['customer']

    if re.fullmatch(r'[-]?\d+', message.text):
        sessionmaker = message.bot.get('db')
        await message.bot.edit_message_reply_markup(message.chat.id, msg)
        await user.update_user(sessionmaker, telegram_id=customer.telegram_id,
                               updated_fields={'balance': customer.balance + int(message.text)})
        await message.answer(f'✅ Вы успешно отредактировали баланс пользователю '
                             f'<a href="tg://user?id={customer.telegram_id}">{customer.full_name}</a>!',
                             reply_markup=UsersInlineMarkup().menu(user.admin))
        await state.finish()
    else:
        await message.bot.edit_message_reply_markup(message.chat.id, msg)
        b_msg = await message.answer('❌ Ошибка\nУкажите верное кол-во денег!', reply_markup=ToolsInlineMarkup().cancel())
        await state.update_data(b_msg=b_msg.message_id)


def register_settings_user(dp: Dispatcher):
    dp.register_message_handler(show_profile_user, CommandStart(deep_link=re.compile(r'^user_id-\d+$')))
    dp.register_callback_query_handler(first_add_money, text="user_add_money")
    dp.register_message_handler(add_money_user, state=SettingsUserStorage.edit_users_price)
