from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

main = KeyboardButton("🏠 Asosiy menyu")
back = KeyboardButton("⬅️ Orqaga")

async def del_create_markups(reg_user_id):
    infor = await db.select_malumotlar(reg_user_id=int(reg_user_id))
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for info in infor:
        markup.insert(f"❌ {str(info['created_at'])} ❌")
    markup.add(back, main)
    return markup

malumotlar_markup = ReplyKeyboardMarkup(resize_keyboard=True)
malumotlar_markup.add(KeyboardButton("📂 Sizning ma'lumotlaringiz"), KeyboardButton("➕ Ma'lumot qo'shish"))
malumotlar_markup.add(main)

get_info_markup = ReplyKeyboardMarkup(resize_keyboard=True)
get_info_markup.add("📝 Matnlar")
get_info_markup.add(KeyboardButton("🖼 Fotosuratlar"), KeyboardButton("📹 Videolar"))
get_info_markup.add(KeyboardButton("📂 Barcha ma'lumotlar"), KeyboardButton("🗑 Ma'lumot o'chirish"))
get_info_markup.add(main, back)


add_markup = ReplyKeyboardMarkup(resize_keyboard=True)
add_markup.add(KeyboardButton("➕📝 Matn qo'shish"), KeyboardButton("➕🖼 Rasm qo'shish"))
add_markup.row("➕📹 Video qo'shish")
add_markup.add(main, back)

main_back_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_back_markup.add(main, back)

del_malumot = ReplyKeyboardMarkup(resize_keyboard=True)
del_malumot.add(KeyboardButton("🗑 Ma'lumot o'chirish"))
del_malumot.add(main, back)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(main)