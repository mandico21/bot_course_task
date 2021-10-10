from aiogram import Dispatcher

from tgbot.handlers.admins.add_product import register_add_product
from tgbot.handlers.admins.admin_panel_ import register_admin_start
from tgbot.handlers.admins.edit_product import register_edit_product
from tgbot.handlers.admins.mailing import register_mailing
from tgbot.handlers.admins.settings_user import register_settings_user


def setup_admins(dp: Dispatcher):
    register_admin_start(dp)
    register_mailing(dp)
    register_add_product(dp)
    register_edit_product(dp)
    register_settings_user(dp)
