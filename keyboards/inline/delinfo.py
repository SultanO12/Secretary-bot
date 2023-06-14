from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_inline = InlineKeyboardMarkup(row_width=2)
check_inline.add(InlineKeyboardButton(text="✅ Ha", callback_data='yes'), InlineKeyboardButton(text="❌ Yo'q", callback_data='no'))