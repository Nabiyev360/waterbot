from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.inline.inlineBtns import logout_accept

@dp.message_handler(text='🔙 Profildan chiqish', state='*')
async def bot_start(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer('❓ Rostdan ham profildan chiqmoqchimisiz?', reply_markup=logout_accept)

@dp.callback_query_handler(text_contains='logout-', state='*')
async def logout_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if 'access' in call.data:
        await call.message.edit_text('Profildan chiqildi ✅\n')
        await call.message.answer('Qayta kirish uchun: 👉 /start', reply_markup=types.ReplyKeyboardRemove())
        db.logout_user(user_id=call.from_user.id)
    elif 'cancel' in call.data:
        await call.message.edit_text('Chiqish bekor qilindi.')