from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

@dp.message_handler(text="Bot haqida ℹ️", state='*')
async def do_info_bot(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("🤖 Bot kotibi o'z serverida saqlanadigan maxfiy ma'lumotlarni yuqori darajada himoya qiladi, u nafaqat matnli ma'lumotlarni, balki voqealar fotosuratlari, ko'rsatmalar va talab qilinishi mumkin bo'lgan boshqa manbalarni ham saqlashi mumkin.\nVa nihoyat, ushbu bot kotibi nafaqat ma'lumotni saqlashda,\nbalki uni boshqarishda ham yordam beradi. ✅")