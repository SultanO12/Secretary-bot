from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.main_mark import main_markup
from keyboards.default.malumotalar_mark import main_menu
from states.getfikr import GetFikr

@dp.message_handler(text="Fikr bildirish ✍️", state='*')
async def get_fikr(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Fikringizni yozib qoldiring:", reply_markup=main_menu)
    await GetFikr.fikr.set()
  
@dp.message_handler(state=GetFikr.fikr)
async def send_fikr(message: types.Message, state: FSMContext):
  if message.text:
    chat_id = '-1001978431216'
    message_fikr = f"<b>Full name:</b> {message.from_user.full_name}\n<b>Username:</b> @{message.from_user.username}\n<b>User_id:</b> {message.from_user.id}\n\n<b>Fikr:</b> <i>{message.text}</i>"
    await bot.send_message(chat_id=chat_id, text=message_fikr)
    await bot.send_message(chat_id=message.from_user.id, text="<b>Fikr muvaffaqiyatli yuborildi!</b> ✅", reply_markup=main_markup)
    await state.finish()
  else:
     await message.answer("Fikrni matn sifatida yuboring!", reply_markup=main_menu)

