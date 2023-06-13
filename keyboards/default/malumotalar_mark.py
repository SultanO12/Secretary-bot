from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = KeyboardButton("🏠 Asosiy menyu")

malumotlar_markup = ReplyKeyboardMarkup(resize_keyboard=True)
malumotlar_markup.add(KeyboardButton("📂 Sizning ma'lumotlaringiz"), KeyboardButton("🔍 Ma'lumot qidirish"))
malumotlar_markup.add(main)