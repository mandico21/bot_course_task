from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.markup_constructor.inline import InlineMarkupConstructor


class AdminsInlineMarkup(InlineMarkupConstructor):

    def menu(self) -> InlineKeyboardMarkup:
        schema = [1, 1, 2]
        actions = [
            {'text': '🎁 Добавить товар', 'callback_data': 'add_product'},
            {'text': '🛠 Редактировать товар', 'callback_data': 'edit_product'},
            {'text': '📢 Рассылка', 'callback_data': 'mailing'},
            {'text': '🗂 Главное меню', 'callback_data': 'back_button'},
        ]
        return self.markup(actions, schema)
