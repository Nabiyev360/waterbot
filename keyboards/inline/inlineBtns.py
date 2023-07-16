from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cancel_enter_count(product_id):
    button = InlineKeyboardMarkup()
    button.add(InlineKeyboardButton(text='🔙 Orqaga', callback_data=f'product-{product_id}'))
    return button

logout_accept = InlineKeyboardMarkup()
logout_accept.add()
logout_accept.insert(InlineKeyboardButton(text="🙅‍♂ Yo'q", callback_data='logout-cancel'))