import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from data.config import api_url


@dp.message_handler(text="ℹ Ma'lumotlarim", state='*')
async def product_handler(msg: types.Message, state: FSMContext):
    await state.finish()
    client_id = db.get_client_id(msg.from_user.id)
    res = requests.get(f"{api_url}/api/client/client-info?client_id={client_id}").json()

    txt = f"<b>Ism:</b> {res['fullname']}\n<b>Balans:</b> {res['balance']}\n<b>Idish qarzlar:</b> {res['container']}\n<b>Telefon raqam:</b> <span class=\"tg-spoiler\">{res['phone']}</span>\n<b>Organizatisya:</b> {res['organization']['name']}"

    await msg.answer(text=txt)