from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.reg_user import SignIn
from time import sleep
from keyboards.default.sign import log_markup
from keyboards.default.main_mark import main_markup_signin



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


            
