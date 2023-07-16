from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime


def order_board(res):
    order_list = InlineKeyboardMarkup()

    for order in res:
        product_id = order['id']
        product_name = order['product']['name']
        product_count = order['product_count']
        cd = order['created_at']
        created = datetime.strptime(cd[:10], "%Y-%m-%d").strftime("%d-%m-%Y")

        txt = f"{product_name}  |  {product_count} dona  | {created}"

        order_list.add(InlineKeyboardButton(text=txt, callback_data=f'order_detail-{product_id}'))

    order_list.add(InlineKeyboardButton(text='✖', callback_data='cross'))

    return order_list


def order_detail_keyboard(order_id, product_id):
    detailboard = InlineKeyboardMarkup()
    detailboard.add(InlineKeyboardButton(text="✏ Miqdorni o'zgartirish",
                                         callback_data=f'update {order_id} {product_id}'))
    detailboard.add(InlineKeyboardButton(text="❌ Buyurtmani o'chirish",
                                         callback_data=f'delete_order-{order_id}'))
    detailboard.add(InlineKeyboardButton(text="🔙 Ro'yxatga qaytish",
                                         callback_data='back-to-list'))
    return detailboard


back_to_list = InlineKeyboardMarkup().add(InlineKeyboardButton(text="🔙 Ro'yxatga qaytish", callback_data='back-to-list'))
orders_inline = InlineKeyboardMarkup().add(InlineKeyboardButton(text="📑 Buyurtmalarim", callback_data='back-to-list'))