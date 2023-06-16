from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.sign import log_markup

@dp.message_handler(text="Bot haqida ℹ️", state='*')
async def do_info_bot(message: types.Message, state: FSMContext):
    await state.finish()
    user = await db.select_user(telegram_id=int(message.from_user.id))
    check_reg = await db.select_reg_user(user_id=int(user['id']))
    if check_reg:
        await message.answer("🤖 Bot kotibi o'z serverida saqlanadigan maxfiy ma'lumotlarni yuqori darajada himoya qiladi, u nafaqat matnli ma'lumotlarni, balki voqealar fotosuratlari, ko'rsatmalar va talab qilinishi mumkin bo'lgan boshqa manbalarni ham saqlashi mumkin.\nVa nihoyat, ushbu bot kotibi nafaqat ma'lumotni saqlashda,\nbalki uni boshqarishda ham yordam beradi. ✅")
    else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)