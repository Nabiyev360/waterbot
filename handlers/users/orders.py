import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from data.config import api_url
from keyboards.inline.orderBoard import order_board, order_detail_keyboard
from keyboards.default.mainBoard import main_menu
from states.buyingStates import BuyStates


@dp.message_handler(text='📑 Buyurtmalarim', state='*')
async def product_handler(msg: types.Message, state: FSMContext):
    await state.finish()
    client_id = db.get_client_id(msg.from_user.id)
    res = requests.get(f"{api_url}/api/client/orders?client_id={client_id}").json()

    try:
        await msg.answer(text="<b>🧾 Buyurtmalar ro'yxati</b>", reply_markup=order_board(res))
    except:
        await msg.answer(text="Buyurtmalar bo'sh 📤")


@dp.callback_query_handler(text_contains='order_detail-')
async def order_detail(call: types.CallbackQuery):
    order_id = call.data[13:]

    client_id = db.get_client_id(call.from_user.id)
    response = requests.get(f"{api_url}/api/client/orders?client_id={client_id}").json()
    order = None
    for r in response:
        if r['id'] == int(order_id):
            order = r

    txt = f"<b>Mahsulot nomi:</b> {order['product']['name']}\n<b>Miqdori: {order['product_count']} dona</b>\n<b>Narxi:</b> {order['product']['price']} so'm"

    await call.message.edit_text(text=txt, reply_markup=order_detail_keyboard(order_id=order_id,
                                                                              product_id=order['product']['id']))


@dp.callback_query_handler(text='back-to-list')
async def order_back(call: types.CallbackQuery):
    client_id = db.get_client_id(call.from_user.id)
    res = requests.get(f"{api_url}/api/client/orders?client_id={client_id}").json()

    ### Buyurtma bo'sh bo'lsa ###

    await call.message.edit_text(text="<b>🧾 Buyurtmalar ro'yxati</b>", reply_markup=order_board(res))


@dp.callback_query_handler(text='cross')
async def cross_handler(call: types.CallbackQuery):
    await call.message.answer('Asosiy menyu', reply_markup=main_menu)
    await call.message.delete()


@dp.callback_query_handler(text_contains='update')
async def delete_handler(call: types.CallbackQuery, state: FSMContext):
    order_id = call.data.split()[1]
    product_id = call.data.split()[2]
    await call.message.edit_text('Yangi miqdorni kiriting:')

    await BuyStates.wait_updating_count.set()
    await state.update_data(order_id=order_id, product_id=product_id)


@dp.message_handler(state=BuyStates.wait_updating_count)
async def new_count_handler(msg: types.Message, state: FSMContext):
    try:
        new_count = int(msg.text)
    except:
        await msg.answer("Noto'g'ri format! 'Buyurtma qilinayotgan mahsulot <b>(dona)</b> miqdorini kiring:\n(Masalan: 1, 4, 50 ...)'")
        return

    datas = await state.get_data()
    client_id = db.get_client_id(msg.from_user.id)

    res = requests.put(
        url=api_url + '/api/client/order/update',
        data={"client_id": client_id, "order_id": datas['order_id'], "product_id": datas['product_id'],
              "count": new_count})
    if res.status_code == 200:
        await msg.answer(text='✅ ' + res.json()['message'], reply_markup=main_menu)
    else:
        print(res)


    res = requests.get(f"{api_url}/api/client/orders?client_id={client_id}").json()
    try:
        await msg.answer(text="<b>🧾 Buyurtmalar ro'yxati</b>", reply_markup=order_board(res))
    except:
        await msg.answer(text="Buyurtmalar bo'sh 📤")


    await state.finish()



@dp.callback_query_handler(text_contains='delete_order-')
async def delete_handler(call: types.CallbackQuery):
    order_id = call.data[13:]
    res = requests.delete(api_url + '/api/client/order/delete?order_id=' + order_id)
    if res.status_code == 200:
        await call.answer(res.json()['message'], show_alert=True)

    client_id = db.get_client_id(call.from_user.id)
    res = requests.get(f"{api_url}/api/client/orders?client_id={client_id}").json()
    try:
        await call.message.edit_text(text="<b>🧾 Buyurtmalar ro'yxati</b>", reply_markup=order_board(res))
    except:
        await call.message.edit_text(text="Buyurtmalar bo'sh 📤")
