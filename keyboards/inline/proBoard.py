from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def product_board(res):
    product_list = InlineKeyboardMarkup()

    for product in res:
        product_id = product['id']
        name = product['name']
        price = product['price']
        product_list.add(InlineKeyboardButton(text=f"{name}  |  {price} so'm", callback_data=f'product-{product_id}'))

    product_list.add(InlineKeyboardButton(text='✖', callback_data='cross'))

    return product_list


def detail_board(product_id):
    d_board = InlineKeyboardMarkup()
    d_board.add(InlineKeyboardButton(text="📥 Buyurtma berish", callback_data=f'create-order-{product_id}'))
    d_board.add(InlineKeyboardButton(text="🔙 Ro'yxatga qaytish", callback_data='back-to-products'))
    return d_board

pr_or_order = InlineKeyboardMarkup()
pr_or_order.add(InlineKeyboardButton(text='🛍 Davom etish', callback_data='back-to-products'))
pr_or_order.add(InlineKeyboardButton(text='📑 Buyurtmalarim', callback_data='back-to-list'))
