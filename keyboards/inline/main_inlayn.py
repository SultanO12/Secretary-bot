from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

get_info_reg_user = InlineKeyboardMarkup()
get_info_reg_user.add(InlineKeyboardButton(text="To'gri", callback_data="yes"), InlineKeyboardButton(text="No'togri", callback_data="no"))