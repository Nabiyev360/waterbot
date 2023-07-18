import re
import requests
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from keyboards.default.mainBoard import main_menu, sign_in_up, sendboard
from loader import dp, db
from data.config import api_url
from states.authStates import LoginStates as Ls, RegisterStates as Rs


@dp.message_handler(CommandStart(), state='*')
async def bot_start(msg: types.Message, state: FSMContext):
    await state.finish()

    if db.is_available(msg.from_user.id):
        await msg.answer('Asosiy menyu', reply_markup=main_menu)
    else:
        await msg.answer(f"<b>Salom, {msg.from_user.full_name}!</b>\nBotdan foydalanishni boshlash uchun"
                         f"waternet.uz saytida ro'yxatdan o'tgan <b>login</b>ingizni kiriting, "
                         f"")
        await Ls.input_login.set()


# @dp.message_handler(state=Ls.choose_sign)
# async def choose_handler(msg: types.Message, state: FSMContext):
#     if msg.text == '🔸 KIRISH 🔸':
#         await msg.answer('Loginni kiriting:')
#         await Ls.input_login.set()
#     elif msg.text == "🔹 RO'YXATDAN O'TISH 🔹":
#         await msg.answer("To'liq ism sharifingizni kiriting:")
#         await Rs.input_fullname.set()

### Logins
@dp.message_handler(state=Ls.input_login)
async def password_handler(msg: types.Message, state: FSMContext):
    await state.update_data(login=msg.text)
    await Ls.input_password.set()
    await dp.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    await dp.bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id-1, text='Parolni kriting:')


@dp.message_handler(state=Ls.input_password)
async def process_info(msg: types.Message, state: FSMContext):
    await state.update_data(password=msg.text)
    login_data = await state.get_data()

    await dp.bot.delete_message(msg.chat.id, msg.message_id)
    await dp.bot.edit_message_text(chat_id=msg.chat.id,
        message_id=msg.message_id-2,
        text='Qabul qilindi, iltimos kutib turing...')

    login_url = f"{api_url}/api/auth/client/login"
    res = requests.post(login_url, json=login_data)

    if res.status_code == 200:
        response = res.json()

        client_id = response.get('id')
        fullname = response.get('fullname')
        balance = response.get('balance')
        container = response.get('container')
        phone = response.get('phone')
        org_name = response.get('organization').get('name')

        await dp.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id - 2)
        await msg.answer(text=f"To'liq ism-sharifingizni kiriting:")

        # add to database
        user = msg.from_user
        db.add_user(user.id, user.full_name, user.username,
                    login_data['login'], login_data['password'],
                    client_id, balance, container, phone, org_name)

        await Rs.input_fullname.set()
        await state.update_data(client_id=client_id)

    else:
        await dp.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id-2)
        await msg.answer("❌ Login yoki parol xato! Iltimos tekshirib qaytadan urinib ko'ring", reply_markup=types.ReplyKeyboardRemove())
        await msg.answer("Loginni kiriting:")
        await Ls.input_login.set()


@dp.message_handler(state=Rs.input_fullname)
async def fullname_handler(msg: types.Message, state: FSMContext):
    await state.update_data(fullname = msg.text)
    await msg.answer('Telefon raqamingizni kiriting:\nFormat: <i>901234567</i>', reply_markup=sendboard)
    await Rs.input_phone.set()


@dp.message_handler(state=Rs.input_phone, content_types=types.ContentTypes.ANY)
async def fullname_handler(msg: types.Message, state: FSMContext):
    phone_number = None
    if msg.contact:
        phone_data = msg.contact.phone_number

        try:
            if phone_data[0] == '+':
                phone_number = phone_data.split('+998')[1]
            elif phone_data[0] == '9':
                phone_number = phone_data.split('998')[1]
            if not re.search(pattern='^[012345789][0-9]{8}$', string=phone_number):
                await msg.answer("Telefon raqam formati noto'g'ri. Iltimos tekshirib qaytatdan yuboring.\n<b>Format: <i>901234567</i></b>")
        except:
            await msg.answer("Telefon raqam formati noto'g'ri. Iltimos tekshirib qaytatdan yuboring.\n<b>Format: <i>901234567</i></b>")
            return

    elif re.search(pattern='^[012345789][0-9]{8}$', string=msg.text):
        phone_number = msg.text
    else:
        await msg.answer("Telefon raqam formati noto'g'ri. Iltimos tekshirib qaytatdan yuboring.\n<b>Format: <i>901234567</i></b>")
        return

    state_data = await state.get_data()
    fullname = state_data['fullname']
    client_id = state_data['client_id']
    data = {
        "fullname" : fullname,
        "phone": phone_number,
        "chat_id" : msg.chat.id
    }
    res = requests.post(f'http://waternet.uz/api/client/registration/{client_id}', data=data, verify=False)
    if res.status_code == 200:
        await msg.answer(f'Salom {fullname}! Botdan foydalanishingiz mumkin.', reply_markup=main_menu)
    else:
        await msg.answer('Xatolik!', reply_markup=types.ReplyKeyboardRemove())

    await state.finish()