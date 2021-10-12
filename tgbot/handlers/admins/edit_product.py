from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hide_link

from tgbot.keyboards.inline.iadmins import AdminsInlineMarkup
from tgbot.keyboards.inline.itools import ToolsInlineMarkup
from tgbot.misc.states import EditProductStorage
from tgbot.models.products import Product


def show_product_text(product_id):
    text = f'{hide_link(product_id.url_img)}' \
           f'📫 Артикл: <b><i>{product_id.item_id}</i></b>\n' \
           f'📌 Название: <b><i>{product_id.name}</i></b>\n' \
           f'💎 Количество: <b><i>{product_id.quantity}</i></b>\n' \
           f'📝 Описание: <b><i>{product_id.description}</i></b>\n' \
           f'💰 Цена: <b><i>{product_id.price} ₽</i></b>'
    return text


async def edit_product_search(call: CallbackQuery, callback_data: dict, state: FSMContext):
    sessionmaker = call.bot.get('db')

    check_product = await Product.get_product(sessionmaker, int(callback_data['item_id']))
    if check_product is None:
        return await call.message.answer('❌ Ошибка!\nТовар который вы заращиваете не найден')

    await call.message.delete()
    await call.message.answer_photo(check_product.url_img,
                                    show_product_text(check_product),
                                    reply_markup=AdminsInlineMarkup().edit(int(check_product.item_id)))
    await state.update_data(old=check_product)


async def edit_product_all(call: CallbackQuery, callback_data: dict, state: FSMContext):
    product_id = callback_data.get('item_id')
    button = callback_data.get('button')
    prefix = {'name': 'е <b>название</b>',
              'description': 'е <b>описание</b>',
              'price': 'ю <b>стоимость</b>',
              'quantity': 'е <b>количество</b>'}

    await call.message.delete()
    await call.message.answer(f'✏ Укажите ново{prefix[button]} товара')
    await state.update_data(button=button,
                            product_id=product_id)
    await EditProductStorage.edit_product_all.set()


async def edit_product_(message: Message, state: FSMContext):
    data = await state.get_data()
    if data['button'] == 'name':
        if len(message.text) > 100:
            await message.answer('❌ Ошибка\n🔖 Слишком длинное название. Максимальная длина 100 символов')
            return
    elif data['button'] == 'description':
        if len(message.text) > 600:
            await message.answer('❌ Ошибка\n🔖 Слишком длинное описание. Максимальная длина 600 символов')
            return
    elif data['button'] == 'quantity':
        try:
            int(message.text)
        except ValueError:
            await message.answer('❌ Ошибка\n🔖 Количество товара должно быть в цифрах!')
            return
        message.text = int(message.text)
    elif data['button'] == 'price':
        try:
            int(message.text)
        except ValueError:
            await message.answer('❌ Ошибка\n🔖 Стоимоть товара должна быть в цифрах!')
            return
        message.text = int(message.text)

    sessionmaker = message.bot.get('db')
    await Product.update_product(sessionmaker, int(data['product_id']), updated_fields={data['button']: message.text})
    product = await Product.get_product(sessionmaker, int(data['product_id']))
    prefix = {'name': '<b>название</b>',
              'description': '<b>описание</b>',
              'price': '<b>стоимость</b>',
              'quantity': '<b>количество</b>'}
    await message.answer(f'✅ Вы успешно изменили {prefix[data["button"]]} товара')
    await message.answer_photo(product.url_img,
                               show_product_text(product),
                               reply_markup=AdminsInlineMarkup().edit(int(product.item_id)))
    await state.finish()


def register_edit_product(dp: Dispatcher):
    dp.register_callback_query_handler(edit_product_search, ToolsInlineMarkup.edit_call.filter())
    dp.register_callback_query_handler(edit_product_all, AdminsInlineMarkup.product_call.filter())
    dp.register_message_handler(edit_product_, state=EditProductStorage.edit_product_all)
