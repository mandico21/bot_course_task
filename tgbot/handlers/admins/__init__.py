from aiogram import Dispatcher

from tgbot.handlers.admins.add_product import register_add_product
from tgbot.handlers.admins.admin import register_admin_start
from tgbot.handlers.admins.mailing import register_mailing


def setup_admins(dp: Dispatcher):
    register_admin_start(dp)
    register_mailing(dp)
    register_add_product(dp)