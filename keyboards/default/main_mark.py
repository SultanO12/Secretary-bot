from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add(KeyboardButton("🗂 Ma'lumotlar"))
main_markup.row("Fikr bildirish ✍️", "Bot haqida ℹ️")

get_phone_markup = ReplyKeyboardMarkup(resize_keyboard=True)
get_phone_markup.add(KeyboardButton("📞 Telefon raqamini yuborish" ,request_contact=True))


main_markup_signin = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup_signin.add(KeyboardButton("🗂 Ma'lumotni o'qish"))
