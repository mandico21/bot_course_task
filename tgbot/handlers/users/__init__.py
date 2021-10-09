from aiogram import Dispatcher

from tgbot.handlers.users.buy_product import register_buy_product
from tgbot.handlers.users.feedback import register_feedback
from tgbot.handlers.users.referral import register_referral
from tgbot.handlers.users.start import register_start


def setup_users(dp: Dispatcher):
    register_start(dp)
    register_referral(dp)
    register_feedback(dp)
    register_buy_product(dp)
