from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = KeyboardButton("🏠 Asosiy menyu")

malumotlar_markup = ReplyKeyboardMarkup(resize_keyboard=True)
malumotlar_markup.add(KeyboardButton("📂 Sizning ma'lumotlaringiz"), KeyboardButton("➕ Ma'lumot qo'shish"))
malumotlar_markup.add(KeyboardButton("🔍 Ma'lumot qidirish"))
malumotlar_markup.add(main)

add_markup = ReplyKeyboardMarkup(resize_keyboard=True)
add_markup.add(KeyboardButton("➕📝Matn qo'shish"), KeyboardButton("➕🖼 Rasm qo'shish"))
add_markup.add(main)