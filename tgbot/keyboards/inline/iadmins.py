from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.misc.markup_constructor.inline import InlineMarkupConstructor


class AdminsInlineMarkup(InlineMarkupConstructor):
    product_call = CallbackData('edit_call', 'button', 'item_id')

    def menu(self) -> InlineKeyboardMarkup:
        schema = [2, 1, 1]
        actions = [
            {'text': '🎁 Добавить товар', 'callback_data': 'add_product'},
            {'text': '📢 Рассылка', 'callback_data': 'mailing'},
            {'text': '👥 Пользователи', 'switch_inline_query_current_chat': 'users-'},
            {'text': '🗂 Главное меню', 'callback_data': 'back_button'},
        ]
        return self.markup(actions, schema)

    def edit(self, item_id: int) -> InlineKeyboardMarkup:
        schema = [1, 1, 1, 1, 1]
        actions = [
            {'text': '📌 Редактировать название',
             'callback_data': self.product_call.new(button='name', item_id=item_id)},
            {'text': '📝 Редактировать описание',
             'callback_data': self.product_call.new(button='description', item_id=item_id)},
            {'text': '💎 Редактировать количество',
             'callback_data': self.product_call.new(button='quantity', item_id=item_id)},
            {'text': '💰 Редактировать цену',
             'callback_data': self.product_call.new(button='price', item_id=item_id)},
            {'text': '❌ Отмена', 'callback_data': 'cancel'},
        ]
        return self.markup(actions, schema)

    def user(self, admin: bool) -> InlineKeyboardMarkup:
        schema = [1, 1, 1]
        actions = [
            {'text': '💸 Редактировать баланс', 'callback_data': 'user_add_money'},
            {'text': '👤 Назаначить админом', 'callback_data': 'add_admin_user'},
            {'text': '❌ Отмена', 'callback_data': 'cancel'},
        ]
        if admin:
            schema = [1, 1, 1]
            actions.insert(1, {'text': '🗣 Удалить админа', 'callback_data': 'delete_admin_user'})
            actions.remove({'text': '👤 Назаначить админом', 'callback_data': 'add_admin_user'})
        return self.markup(actions, schema)
