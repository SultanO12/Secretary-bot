from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

log_markup = ReplyKeyboardMarkup(resize_keyboard=True)
log_markup.add(KeyboardButton("📋 Ro'yxatdan o'tish"), KeyboardButton("🔐 Kirish"))