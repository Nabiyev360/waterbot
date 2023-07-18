import requests
from aiogram import types

from loader import dp, db
from data.config import api_url

from keyboards.inline.orderBoard import order_board


@dp.callback_query_handler(text_contains='Rate')
async def delete_handler(call: types.CallbackQuery):
    rate = call.data[4]
    rate_id = call.data[5:]
    res = requests.put(api_url + f'/api/client/order-rates/{rate_id}/update', verify=False,
                       data={"rate" : int(rate), "comment" : "izoh"})
    print(res.status_code)

    await call.message.delete()