from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def rate_ballboard(order_id):
    markup = InlineKeyboardMarkup(row_width=3)
    for i in range(0, 6):
        markup.insert(InlineKeyboardButton(text=str(i), callback_data=f'Rate{i} {order_id}'))

    return markup