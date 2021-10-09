from aiogram import Dispatcher

from tgbot.handlers.inline.istart import register_istart


def setup_inline(dp: Dispatcher):
    register_istart(dp)
