import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.inlineBtns import cancel_enter_count
from loader import dp, db
from data.config import api_url
from keyboards.inline.proBoard import product_board, detail_board, pr_or_order
from keyboards.inline.orderBoard import orders_inline
from states.buyingStates import BuyStates


@dp.message_handler(text="🛍 Mahsulotlar", state='*')
async def product_handler(msg: types.Message, state: FSMContext):
    await state.finish()
    res = requests.get(f"{api_url}/api/client/products?client_id={db.get_client_id(msg.from_user.id)}").json()
    await msg.answer("<b>Mahsulotlar ro'yxati</b>", reply_markup=product_board(res))


@dp.callback_query_handler(text_contains='product-', state='*')
async def product_detail(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    product_id = call.data[8:]
    res = requests.get(f"{api_url}/api/client/products?client_id={db.get_client_id(call.from_user.id)}").json()
    product = None

    for pr in res:
        if pr['id'] == int(product_id):
            product = pr

    txt = f"<b>Mahsulot nomi:</b> {product['name']}\n" \
          f"<b>Narxi:</b> {product['price']} so'm\n" \

    await call.message.edit_text(txt, reply_markup=detail_board(product['id']))


@dp.callback_query_handler(text_contains='create-order-')
async def buy_handler(call: types.CallbackQuery, state: FSMContext):
    product_id = call.data[13:]
    await call.message.edit_text('Buyurtma qilinayotgan mahsulot miqdorini kiriting.\nMasalan: 1, 4, 50, ...', reply_markup=cancel_enter_count(product_id))
    await BuyStates.wait_product_count.set()
    await state.update_data(product_id=product_id)

@dp.callback_query_handler(text_contains='back-to-products')
async def product_back(call: types.CallbackQuery):
    res = requests.get(f"{api_url}/api/client/products?client_id={db.get_client_id(call.from_user.id)}").json()
    await call.message.edit_text("<b>Mahsulotlar ro'yxati</b>", reply_markup=product_board(res))


@dp.message_handler(state=BuyStates.wait_product_count)
async def count_handler(msg: types.Message, state: FSMContext):
    try:
        count = int(msg.text)
    except:
        await msg.answer("Noto'g'ri format! 'Buyurtma qilinayotgan mahsulot <b>(dona)</b> miqdorini kiring:\n(Masalan: 1, 4, 50 ...)'")
        return

    datas = await state.get_data()

    data = {
        "client_id": db.get_client_id(msg.from_user.id),
        "product_id": datas.get('product_id'),
        "count": count
    }

    res = requests.post(api_url+'/api/client/create/order', json=data)

    if res.status_code == 422:
        await msg.answer(text=res.json()["message"], reply_markup=orders_inline)
    elif res.status_code == 200:
        await msg.answer(text='✅ Mahsulot buyurtma qilindi', reply_markup=pr_or_order)


    await state.finish()
