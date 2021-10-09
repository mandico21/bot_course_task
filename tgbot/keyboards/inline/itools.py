from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.markup_constructor.inline import InlineMarkupConstructor


class ToolsInlineMarkup(InlineMarkupConstructor):

    def negotiate(self) -> InlineKeyboardMarkup:
        schema = [2]
        actions = [
            {'text': '✅ Подтвердить', 'callback_data': 'nego_confirm'},
            {'text': '❌ Отменить', 'callback_data': 'nego_cancel'}
        ]
        return self.markup(actions, schema)


    def back(self) -> InlineKeyboardMarkup:
        schema = [1]
        actions = [
            {'text': '◀️ Назад', 'callback_data': 'back_button'},
        ]
        return self.markup(actions, schema)


    def cancel(self) -> InlineKeyboardMarkup:
        schema = [1]
        actions = [
            {'text': '❌ Отменить', 'callback_data': 'cancel'}
        ]
        return self.markup(actions, schema)


