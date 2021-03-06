from aiogram.dispatcher.filters.state import StatesGroup, State


class StorageUsers(StatesGroup):
    invite_code = State()
    register_user = State()
    feedback_admin = State()
    feedback_statement = State()


class MailingStorage(StatesGroup):
    mailing_start = State()
    progressing = State()


class FeedbackStorage(StatesGroup):
    feedback_start = State()
    feedback_statement = State()


class StorageAdmin(StatesGroup):
    start_add_money = State()
    add_money = State()
    speak_specify_user_id = State()
    speak_remove_user_id = State()


class AddProductStorage(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()
    expectations = State()


class BuyProductStorage(StatesGroup):
    beginning_product = State()
    get_delivery_adress = State()
    payment_product = State()
    check_payment = State()


class EditProductStorage(StatesGroup):
    edit_product_search = State()
    edit_product_all = State()
    edit_product_quantity = State()
    edit_product_name = State()
    edit_product_description = State()
    edit_product_price = State()


class SettingsUserStorage(StatesGroup):
    edit_users_price = State()
