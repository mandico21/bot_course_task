from aiogram.dispatcher.filters.state import StatesGroup, State


class StorageUsers(StatesGroup):
    invite_code = State()
    register_user = State()
    feedback_admin = State()
    feedback_statement = State()


class MailingStorage(StatesGroup):
    mailing_start = State()
    progressing = State()