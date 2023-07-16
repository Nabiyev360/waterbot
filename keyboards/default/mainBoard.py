from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("🛍 Mahsulotlar")
main_menu.add("ℹ Ma'lumotlarim")
main_menu.insert("📑 Buyurtmalarim")
main_menu.add('🔙 Profildan chiqish')

sign_in_up = ReplyKeyboardMarkup(resize_keyboard=True)
sign_in_up.add('🔸 KIRISH 🔸')
sign_in_up.add("🔹 RO'YXATDAN O'TISH 🔹")

sendboard = ReplyKeyboardMarkup(resize_keyboard=True)
sendboard.add(KeyboardButton("📲 Telefon raqamni jo'natish", request_contact=True))