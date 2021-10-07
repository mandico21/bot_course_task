from aiogram import Dispatcher

from tgbot.handlers.users.user import register_start


def setup_users(dp: Dispatcher):
    register_start(dp)