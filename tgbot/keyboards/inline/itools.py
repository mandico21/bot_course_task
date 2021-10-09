from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.deep_linking import get_start_link

from tgbot.misc.markup_constructor.inline import InlineMarkupConstructor


class ToolsInlineMarkup(InlineMarkupConstructor):
    buy_pod = CallbackData('buy_product', 'item_id')
    edit_call = CallbackData('edit_coproduct', 'item_id')
    bill_cd = CallbackData('bill', 'bill_id')

    def negotiate(self) -> InlineKeyboardMarkup:
        schema = [2]
        actions = [
            {'text': '✅ Подтвердить', 'callback_data': 'nego_confirm'},
            {'text': '❌ Отменить', 'callback_data': 'nego_cancel'}
        ]
        return self.markup(actions, schema)

    def show_product(self, bot_username: str, item_id: str) -> InlineKeyboardMarkup:
        schema = [1]
        actions = [
            {'text': '🛍 Показать товар', 'url': f'https://t.me/{bot_username}?start=item_id-{item_id}'},
        ]
        return self.markup(actions, schema)

    def buy_product(self, item_id: str, is_admin: bool) -> InlineKeyboardMarkup:
        schema = [1]
        actions = [
            {'text': '🛒 Купить товар', 'callback_data': self.buy_pod.new(item_id=item_id)},
        ]
        if is_admin:
            schema = [1, 1]
            actions.append({'text': '🛠 Редактировать товар', 'callback_data': self.edit_call.new(item_id=item_id)})
        return self.markup(actions, schema)

    def product_payment(self) -> InlineKeyboardMarkup:
        schema = [2, 1]
        actions = [
            {'text': '💰 Оплата Балансом', 'callback_data': 'to_pay_bal'},
            {'text': '💳 Оплата Qiwi', 'callback_data': 'to_pay_qiwi'},
            {'text': '❌ Отменить', 'callback_data': 'cancel'},
        ]
        return self.markup(actions, schema)

    def product_payment_qiwi(self, url: str, bill_id: str) -> InlineKeyboardMarkup:
        schema = [2, 1]
        actions = [
            {'text': '💳 Оплатить', 'url': url},
            {'text': '🔄 Проверить', 'callback_data': self.bill_cd.new(bill_id=bill_id)},
            {'text': '❌ Отменить', 'callback_data': 'cancel'},
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
