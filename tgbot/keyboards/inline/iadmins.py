from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.markup_constructor.inline import InlineMarkupConstructor


class AdminsInlineMarkup(InlineMarkupConstructor):

    def menu(self) -> InlineKeyboardMarkup:
        schema = [2, 1]
        actions = [
            {'text': '🎁 Добавить товар', 'callback_data': 'add_product'},
            {'text': '📢 Рассылка', 'callback_data': 'mailing'},
            {'text': '🗂 Главное меню', 'callback_data': 'back_button'},
        ]
        return self.markup(actions, schema)

    def edit(self) -> InlineKeyboardMarkup:
        schema = [1, 1, 1, 1, 1]
        actions = [
            {'text': '📌 Редактировать название', 'callback_data': 'edit_name'},
            {'text': '📝 Редактировать описание', 'callback_data': 'edit_description'},
            {'text': '💎 Редактировать количество', 'callback_data': 'edit_quantity'},
            {'text': '💰 Редактировать цену', 'callback_data': 'edit_price'},
            {'text': '❌ Отмена', 'callback_data': 'cancel'},
        ]
        return self.markup(actions, schema)
