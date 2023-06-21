from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.malumotalar_mark import malumotlar_markup, add_markup, main_back_markup, del_malumot, del_create_markups, get_info_markup
from keyboards.default.sign import log_markup
from keyboards.inline.delinfo import check_inline
from states.add_malumot import AddMalumot
from states.del_infor import Delinfo
from states.send_info import SearchInfo
from datetime import datetime

@dp.message_handler(text='⬅️ Orqaga', state=[AddMalumot.text, AddMalumot.img, AddMalumot.video])
async def back_2(message: types.Message, state: FSMContext):
   await state.finish()
   await message.answer("Qo'shmoqchi bo'lgan narsani tanlang:", reply_markup=add_markup)

@dp.message_handler(text="⬅️ Orqaga", state=Delinfo.data)
async def back_3(message: types.Message, state: FSMContext):
   await state.finish()
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   if check_reg:
      malumotlar = await db.select_malumotlar(reg_user_id=int(check_reg['id']))
      if malumotlar:
        await message.answer("<b>Ma'lumotlar:</b>", reply_markup=del_malumot)

        for malumot in malumotlar:
           if malumot['video']:
              await message.answer_video(malumot['video'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")

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

@dp.message_handler(text='⬅️ Orqaga')
@dp.message_handler(text="🗂 Ma'lumotlar", state='*')
async def do_malumotlar(message: types.Message, state: FSMContext):
    await state.finish()
    user = await db.select_user(telegram_id=int(message.from_user.id))
    check_reg = await db.select_reg_user(user_id=int(user['id']))
    if check_reg:
      await message.answer("Siz <b>Ma'lumotlar</b> bo'limidasiz:", reply_markup=malumotlar_markup)
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
        await message.answer("<b>Ma'lumotlar:</b>", reply_markup=get_info_markup)
        
      else:
         await message.answer("Sizda hali saqlangan ma'lumotlar yo'q!")
   else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

@dp.message_handler(text=['📝 Matnlar', "🖼 Fotosuratlar", "📹 Videolar", "📂 Barcha ma'lumotlar"])
async def get_info_types(message: types.Message, state: FSMContext):
   await state.finish()

   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   if check_reg:
      malumotlar = await db.select_malumotlar(reg_user_id=int(check_reg['id']))
      if message.text == "📂 Barcha ma'lumotlar":
         await message.answer("<b>Ma'lumotlar:</b>")
         for malumot in malumotlar:
            if malumot['video']:
               await message.answer_video(malumot['video'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")

         for malumot in malumotlar:
            if malumot['img']: 
               await message.answer_photo(malumot['img'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")
         
         for malumot in malumotlar:
            if malumot['malumot_text']:
               await message.answer(f"{malumot['malumot_text']}\n\n<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")
      elif message.text == "📝 Matnlar":
          await message.answer("<b>Ma'lumotlar:</b>")
          for malumot in malumotlar:
            if malumot['malumot_text']:   
               await message.answer(f"{malumot['malumot_text']}\n\n<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")
            else:
               await message.answer("Sizda matnli ma'lumotlar yo'q!")
      elif message.text == "🖼 Fotosuratlar":
         await message.answer("<b>Ma'lumotlar:</b>")
         for malumot in malumotlar:
            if malumot['img']: 
               await message.answer_photo(malumot['img'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")
            else:
               await message.answer("Sizda fotosuratlar yo'q!")
      elif message.text == "📹 Videolar":
         await message.answer("<b>Ma'lumotlar:</b>")
         for malumot in malumotlar:
            if malumot['video']:
               await message.answer_video(malumot['video'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")
            else:
               await message.answer("Sizda video ma'lumotlar yo'q!")
   else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

@dp.message_handler(text="🗑 Ma'lumot o'chirish", state='*')
async def del_info(message: types.Message, state: FSMContext):
   await state.finish()
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   if check_reg:
      malumotlar = await db.select_malumotlar(reg_user_id=int(check_reg['id']))
      if malumotlar:
         await message.answer("<b>Ma'lumotlar:</b>")
         for malumot in malumotlar:
            if malumot['video']:
               await message.answer_video(malumot['video'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")

         for malumot in malumotlar:
            if malumot['img']: 
               await message.answer_photo(malumot['img'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")
         
         for malumot in malumotlar:
            if malumot['malumot_text']:
               await message.answer(f"{malumot['malumot_text']}\n\n<b><i>Ma'lumot yozilgan sana:</i></b> {str(malumot['created_at'])[:19]}")

         markup = await del_create_markups(check_reg['id'])
         await message.answer("O'chirish uchun ma'lumotnig sanasini tanlang:", reply_markup=markup)
         await state.update_data({"reg_id":check_reg['id']})
         await Delinfo.data.set()
      else:
         await message.answer("Sizda hali saqlangan ma'lumotlar yo'q!")
   else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

@dp.message_handler(state=Delinfo.data)
async def get_data_del_info(message: types.Message, state: FSMContext):
   data_ret = message.text.split()
   time = f"{data_ret[1]} {data_ret[2]}"
   data = await state.get_data()
   date_format = "%Y-%m-%d %H:%M:%S.%f"
   date_object = datetime.strptime(time, date_format)
   infor = await db.select_malumotlar(reg_user_id=int(data['reg_id']))

   
   for info in infor:
      if info['created_at'] == date_object:
         text = info['malumot_text']
         img = info['img']
         video = info['video']
         if text:
            await message.answer(f"<b>Malumot:</b> {info['malumot_text']}\n\n<b><i>Ma'lumot yozilgan sana:</i></b> {str(info['created_at'])[:19]}")
            await message.answer("Tanlangan ma'lumotlarni o'chirib tashlaysizmi?", reply_markup=check_inline)
            await state.update_data({"date_object":date_object})
         elif img:
            await message.answer_photo(photo=info['img'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(info['created_at'])[:19]}")
            await message.answer("Tanlangan ma'lumotlarni o'chirib tashlaysizmi?", reply_markup=check_inline)
            await state.update_data({"date_object":date_object})
         elif video:
            await message.answer_video(video=info['video'], caption=f"<b><i>Ma'lumot yozilgan sana:</i></b> {str(info['created_at'])[:19]}")
            await message.answer("Tanlangan ma'lumotlarni o'chirib tashlaysizmi?", reply_markup=check_inline)
            await state.update_data({"date_object":date_object})
         await Delinfo.check.set()

@dp.callback_query_handler(text=['yes', 'no'], state=Delinfo.check)
async def get_check_del_info(call: types.CallbackQuery, state: FSMContext):
   if call.data == 'yes':
      user = await db.select_user(telegram_id=int(call.from_user.id))
      check_reg = await db.select_reg_user(user_id=int(user['id']))
      data = await state.get_data()
      await db.delete_malumot(reg_user_id=int(check_reg['id']), created_at=data['date_object'])
      await call.message.answer("<b>Ma'lumot muvaffaqiyatli o'chirildi! ✅</b>", reply_markup=malumotlar_markup)
      await state.finish()
   else:
      await call.message.answer("<b>Ma'lumot o'chirilmadi!</b>", reply_markup=malumotlar_markup)
      await state.finish()

@dp.message_handler(text="➕ Ma'lumot qo'shish")
async def add_malumot(message: types.Message, state: FSMContext):
   await state.finish()
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   if check_reg:
      await message.answer("Qo'shmoqchi bo'lgan narsani tanlang:", reply_markup=add_markup)
   else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

@dp.message_handler(text="➕📝 Matn qo'shish", state='*')
async def add_text(message: types.Message, state: FSMContext):
   await state.finish()
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   if check_reg:
      await message.answer("Qo'shmoqchi bo'lgan matnni yuboring:", reply_markup=main_back_markup)
      await AddMalumot.text.set()
   else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

@dp.message_handler(text="➕🖼 Rasm qo'shish", state='*')
async def add_img(message: types.Message, state: FSMContext):
   await state.finish()
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   if check_reg:
      await message.answer("Qo'shmoqchi bo'lgan rasimingizni yuboring:", reply_markup=main_back_markup)
      await AddMalumot.img.set()
   else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

@dp.message_handler(text="➕📹 Video qo'shish", state='*')
async def add_img(message: types.Message, state: FSMContext):
   await state.finish()
   user = await db.select_user(telegram_id=int(message.from_user.id))
   check_reg = await db.select_reg_user(user_id=int(user['id']))
   if check_reg:
      await message.answer("Qo'shmoqchi bo'lgan videoni yuboring:", reply_markup=main_back_markup)
      await AddMalumot.video.set()
   else:
      await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)

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

@dp.message_handler(content_types=['video'], state=AddMalumot.video)
async def get_img(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id=int(message.from_user.id))
    check_reg = await db.select_reg_user(user_id=int(user['id']))
    video_message = message.video.file_id
    # получаем ID видео и выводим его в терминале
    video_id = video_message
    await db.add_malumot(user_id=int(user['id']), reg_user_id=int(check_reg['id']), video=video_id)

    await message.answer("<b>Rasm muvaffaqiyatli yozildi!</b> ✅")
    await state.finish()
    await message.answer("Qo'shmoqchi bo'lgan narsani tanlang:", reply_markup=add_markup)


