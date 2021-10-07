from aiogram import Dispatcher

from tgbot.handlers.users.referral import register_referral
from tgbot.handlers.users.start import register_start


def setup_users(dp: Dispatcher):
    register_start(dp)
    register_referral(dp)