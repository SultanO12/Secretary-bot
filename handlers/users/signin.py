from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.reg_user import SignIn
from time import sleep
from keyboards.default.sign import log_markup
from keyboards.default.main_mark import main_markup_signin
from keyboards.inline.delinfo import check_inline
from states.del_infor import DelSignin


@dp.message_handler(state=SignIn.phone_number)
async def get_info_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number[:4] == "+998" and 9 < len(phone_number) <= 15:
        await state.update_data({"phone_number":phone_number})
        await message.answer("<b>Parolni kiriting</b>:")
        await SignIn.password.set()
    else:
        await message.answer("Telefon raqami no-to'g'ri kiritildi!")

@dp.message_handler(state=SignIn.password)
async def get_info_password(message: types.Message, state: FSMContext):
    password = message.text
    if 8 <= len(password) <= 255 and password != "12345678":
        load = await message.answer("Iltimos kuting...")
        data = await state.get_data()
        check_user = await db.select_info_reg_user(phone_number=str(data['phone_number']), password=str(password))
        
        sleep(2)
        await bot.delete_message(chat_id=message.from_user.id, message_id=load.message_id)

        if check_user:
            user = await db.select_user(telegram_id=int(message.from_user.id))
            await db.add_signin_user(user_id=int(user['id']), reg_user_id=int(check_user['id']), phone_number=str(data['phone_number']), password=str(password))
            await message.answer("✅")
            await message.answer("Siz muvaffaqiyatli tizimga kirdingiz!", reply_markup=main_markup_signin)
           
            await state.finish()
        else:
            await state.finish()
            await message.answer("Login yoki parol noto'g'ri kiritilgan ❌", reply_markup=log_markup)
    else:
        await message.answer("Login yoki parol noto'g'ri kiritilgan ❌", reply_markup=log_markup)


@dp.message_handler(text="🗂 Ma'lumotni o'qish")
async def send_malumot(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id=int(message.from_user.id))
    if user:
            sign_user = await db.select_signin_user(user_id=int(user['id']))
            if sign_user:
                phone_number = sign_user['phone_number']
                password = sign_user['password']
                check_info_reg = await db.select_info_reg_user(phone_number=str(phone_number), password=str(password))
                if check_info_reg:
                    malumotlar = await db.select_malumotlar(reg_user_id=int(check_info_reg['id']))
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
    else:
        await message.answer("ERROR - /start")

@dp.message_handler(text="🔝 Tizimdan chiqish")
async def send_malumot(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id=int(message.from_user.id))
    if user:
            sign_user = await db.select_signin_user(user_id=int(user['id']))
            if sign_user:
                phone_number = sign_user['phone_number']
                password = sign_user['password']
                check_info_reg = await db.select_info_reg_user(phone_number=str(phone_number), password=str(password))
                if check_info_reg:
                   await message.answer("Siz aniq tizimdan chiqishni xohlaysizmi?", reply_markup=check_inline)
                   await DelSignin.check.set()
            else:
                await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)
    else:
        await message.answer("ERROR - /start")

@dp.callback_query_handler(text=['yes', 'no'], state=DelSignin.check)
async def exit_acc(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == 'yes':
        user = await db.select_user(telegram_id=int(call.from_user.id))
        await db.delete_sign_user(user_id=int(user['id']))
        await call.message.answer("<b>Siz tizimdan muvaffaqiyatli chiqdingiz!</b> ✅", reply_markup=log_markup)
        await state.finish()
    else:
        await call.message.answer("<b>Siz asosiy menyudasiz!</b>", reply_markup=main_markup_signin)   
        await state.finish() 