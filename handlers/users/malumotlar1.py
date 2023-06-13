from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.malumotalar_mark import malumotlar_markup, add_markup
from keyboards.default.sign import log_markup
from states.add_malumot import AddMalumot

@dp.message_handler(text="🗂 Ma'lumotlar")
async def do_malumotlar(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id=int(message.from_user.id))
    check_reg = await db.select_reg_user(user_id=int(user['id']))
    if check_reg:
      await message.answer("Siz <b>\"Ma'lumotlar\"</b> bo'limidasiz:", reply_markup=malumotlar_markup)
    else:
       await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

@dp.message_handler(text="📂 Sizning ma'lumotlaringiz")
async def do_get_my_info(message: types.Message, state: FSMContext):
   await state.finish()
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   if check_reg:
      malumotlar = await db.select_malumotlar(reg_user_id=int(check_reg['id']))
      if malumotlar:
        await message.answer("<b>Ma'lumotlar:</b>")
        for malumot in malumotlar:
          if malumot['img']: 
            await message.answer_photo(malumot['img'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")
        
        for malumot in malumotlar:
           if malumot['malumot_text']:
            await message.answer(f"{malumot['malumot_text']}\n\n<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")
      else:
         await message.answer("Sizda hali saqlangan ma'lumotlar yo'q!")
   else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

@dp.message_handler(text="➕ Ma'lumot qo'shish")
async def add_malumot(message: types.Message, state: FSMContext):
   await message.answer("Qo'shmoqchi bo'lgan narsani tanlang:", reply_markup=add_markup)

@dp.message_handler(text="➕📝Matn qo'shish")
async def add_text(message: types.Message, state: FSMContext):
   await state.finish()
   await message.answer("Qo'shmoqchi bo'lgan matnni yuboring:", reply_markup=ReplyKeyboardRemove())
   await AddMalumot.text.set()

@dp.message_handler(text="➕🖼 Rasm qo'shish")
async def add_img(message: types.Message, state: FSMContext):
   await state.finish()
   await message.answer("Qo'shmoqchi bo'lgan rasimingizni yuboring:", reply_markup=ReplyKeyboardRemove())
   await AddMalumot.img.set()

@dp.message_handler(state=AddMalumot.text)
async def get_text(message: types.Message, state: FSMContext):
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   await db.add_malumot(user_id=int(user['id']), reg_user_id=int(check_reg['id']), malumot_text=message.text)
   await message.answer("<b>Matn muvaffaqiyatli yozildi!</b> ✅")
   await state.finish()
   await message.answer("Qo'shmoqchi bo'lgan narsani tanlang:", reply_markup=add_markup)

@dp.message_handler(content_types=['photo'], state=AddMalumot.img)
async def get_img(message: types.Message, state: FSMContext):
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   await db.add_malumot(user_id=int(user['id']), reg_user_id=int(check_reg['id']), img=message.photo[-1]['file_id'])
   await message.answer("<b>Rasm muvaffaqiyatli yozildi!</b> ✅")
   await state.finish()
   await message.answer("Qo'shmoqchi bo'lgan narsani tanlang:", reply_markup=add_markup)