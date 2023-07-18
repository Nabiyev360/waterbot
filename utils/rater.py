import requests
import asyncio

from data.config import api_url
from loader import dp
from keyboards.inline.ballboard import rate_ballboard


async def api_request():
    while True:
        res = requests.get(f"{api_url}/api/client/order-rates", verify=False).json()
        try:
            for data in res['messages'][0]['data']:
                txt = data['message']
                ID = data['id']
                chat_id = data['chat_id']
                rate_msg = data['rate_msg']
                await dp.bot.send_message(chat_id=1589351394, text=txt)
                await asyncio.sleep(1)
                await dp.bot.send_message(chat_id=1589351394, text=rate_msg, reply_markup=rate_ballboard(ID))
                await asyncio.sleep(1)
        except Exception as err:
            print(err)
        try:
            for data in res['messages'][1]['data']:
                txt = data['message']
                chat_id = data['chat_id']
                photo = data['photo']
                await dp.bot.send_photo(chat_id=chat_id, photo=photo, caption=txt)
        except Exception as err:
            print(err)

        await asyncio.sleep(60)



# {
#     "messages": [
#         {
#             "type": "rate",
#             "data": [
#                 {
#                     "id": 1,
#                     "message": "Получено - 50000, Доставлено - 5, Возврат тар - 0, Предоплата -10000. Спасибо за покупки!",
#                     "chat_id": "5011373330",
#                     "rate_msg": "Доставшик хизматини бахоланг ..."
#                 },
#                 {
#                     "id": 2,
#                     "message": "Получено - 50000, Доставлено - 10, Возврат тар - 15, Предоплата -10000. Спасибо за покупки!",
#                     "chat_id": "5011373330",
#                     "rate_msg": "Доставшик хизматини бахоланг ..."
#                 }
#             ]
#         },
#         {
#             "type": "newMessage",
#             "data": [
#                 {
#                     "message": "message",
#                     "chat_id": "5011373330",
#                     "photo": "https://yobte.ru/uploads/posts/2019-11/devushki-v-lesu-75-foto-62.jpg"
#                 },
#                 {
#                     "message": "message",
#                     "chat_id": "5011373330",
#                     "photo": "https://yobte.ru/uploads/posts/2019-11/devushki-v-lesu-75-foto-62.jpg"
#                 },
#                 {
#                     "message": "message",
#                     "chat_id": "5011373330",
#                     "photo": "https://yobte.ru/uploads/posts/2019-11/devushki-v-lesu-75-foto-62.jpg"
#                 }
#             ]
#         }
#     ]
# }