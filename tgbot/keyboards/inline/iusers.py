from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.markup_constructor.inline import InlineMarkupConstructor


class UsersInlineMarkup(InlineMarkupConstructor):

    def menu(self, is_admin: bool) -> InlineKeyboardMarkup:
        schema = [2, 1]
        actions = [
            {'text': '🛒 Каталог', 'switch_inline_query_current_chat': ''},
            {'text': '📨 Обратная свзяь', 'callback_data': 'feedback_user'},
            {'text': '🌐 Рефералка', 'callback_data': 'referrer_user'},
        ]
        if is_admin:
            schema = [2, 1, 1]
            actions.append({'text': '🔐 Административная панель', 'callback_data': 'admin_panel'})
        return self.markup(actions, schema)

    def referral(self, condition: str) -> InlineKeyboardMarkup:
        schema = [1]
        actions = [
            {'text': '◀️ Назад', 'callback_data': 'back_button'},
        ]
        if condition is None:
            schema = [1, 1]
            actions.insert(0, {'text': '🔐 Установить код приглашения', 'callback_data': 'install_referral_code'})
        return self.markup(actions, schema)

    def register(self) -> InlineKeyboardMarkup:
        schema = [1]
        actions = [
            {'text': '🔑 Код приглашения', 'callback_data': 'invitation_code'},
        ]
        return self.markup(actions, schema)
