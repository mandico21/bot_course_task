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

class AdminsInlineMarkup(InlineMarkupConstructor):

    def menu(self) -> InlineKeyboardMarkup:
        schema = [2, 1, 1]
        actions = [
            {'text': '🎁 Добавить товар', 'callback_data': 'add_product'},
            {'text': '🛠 Редактировать товар', 'callback_data': 'edit_product'},
            {'text': '📢 Рассылка', 'callback_data': 'mailing'},
            {'text': '🗂 Главное меню', 'callback_data': 'back_button'},
        ]
        return self.markup(actions, schema)


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


