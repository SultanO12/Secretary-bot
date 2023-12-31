from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.handler import CancelHandler
from loader import dp, db, bot
from data.config import ADMINS
from utils.extra_datas import make_title
from aiogram.dispatcher import FSMContext
from states.reg_user import RegUser, SignIn
from keyboards.default.main_mark import get_phone_markup, main_markup
from keyboards.default.sign import log_markup
from keyboards.default.main_mark import main_markup_signin
from keyboards.inline.main_inlayn import get_info_reg_user
from aiogram.types import ReplyKeyboardRemove
from data.config import CHANNELS
from keyboards.inline.subscription import check_button
from filters import IsPrivate
from utils.misc.subscription import check
import logging


@dp.message_handler(text="🏠 Asosiy menyu", state='*')
@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    """
            MARKDOWN V2                     |     HTML
    link:   [Google](https://google.com/)   |     <a href='https://google.com/'>Google</a>
    bold:   *Qalin text*                    |     <b>Qalin text</b>
    italic: _Yotiq shriftdagi text_         |     <i>Yotiq shriftdagi text</i>



                    **************     Note     **************
    Markdownda _ * [ ] ( ) ~ ` > # + - = | { } . ! belgilari to'g'ridan to'g'ri ishlatilmaydi!!!
    Bu belgilarni ishlatish uchun oldidan \ qo'yish esdan chiqmasin. Masalan  \.  ko'rinishi . belgisini ishlatish uchun yozilgan.
    """


    full_name = message.from_user.full_name
    user = await db.select_user(telegram_id=message.from_user.id)

    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=full_name,
            username=message.from_user.username,
        )
        
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"[{make_title(user['full_name'])}](tg://user?id={user['telegram_id']}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\."
        await bot.send_message(chat_id=ADMINS[0], text=msg, parse_mode=types.ParseMode.MARKDOWN_V2)
    else:
        await bot.send_message(chat_id=ADMINS[0], text=f"[{make_title(full_name)}](tg://user?id={message.from_user.id}) bazaga oldin qo'shilgan", disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN_V2)

    
    
    if message.text != "🏠 Asosiy menyu":
        # 

        logging.info(user)
        final_status = True
        for channel in CHANNELS:
            status = await check(user_id=message.from_user.id, channel=channel)
            final_status *= status

        if not final_status:    

            channels_format = str()
            for channel in CHANNELS:
                chat = await bot.get_chat(channel)
                invite_link = await chat.export_invite_link()
                # logging.info(invite_link)
                channels_format += f"➡️ <a href='{invite_link}'><b>{chat.title}</b></a>\n"

            await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n\n"
                                f"{channels_format}",
                                reply_markup=check_button,
                                disable_web_page_preview=True)
        # 
        else:
            user = await db.select_user(telegram_id=int(message.from_user.id))
            reg_user = await db.select_reg_user(user_id=int(user['id']))
            signin_user = await db.select_signin_user(user_id=int(user['id']))
            if reg_user:
                await message.answer("Sizni qiziqtirgan bo'limni tanlang:", reply_markup=main_markup)
            elif signin_user:
                await message.answer("Siz muvaffaqiyatli tizimga kirdingiz!", reply_markup=main_markup_signin)
            else:
                await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)
    else:
            user = await db.select_user(telegram_id=int(message.from_user.id))
            reg_user = await db.select_reg_user(user_id=int(user['id']))
            signin_user = await db.select_signin_user(user_id=int(user['id']))
            if reg_user:
                await message.answer("Sizni qiziqtirgan bo'limni tanlang:", reply_markup=main_markup)
            elif signin_user:
                await message.answer("Siz muvaffaqiyatli tizimga kirdingiz!", reply_markup=main_markup_signin)
            else:
                await message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)
    
        

@dp.message_handler(text=["📋 Ro'yxatdan o'tish", "🔐 Kirish"])
async def sig(message: types.Message, state: FSMContext):
    user = await db.select_user(telegram_id=int(message.from_user.id))
    check_sign = await db.select_signin_user(user_id=int(user['id']))
    check_reg_user = await db.select_reg_user(user_id=int(user['id']))
    if check_sign:
        await message.answer("<b>Siz tizimdasiz!</b>")
    elif check_reg_user:
        await message.answer("<b>Siz tizimdasiz!</b>")
    else:
        if message.text == "📋 Ro'yxatdan o'tish":
            await message.answer("<b>Iltimos, telefon raqamini kiriting:</b>\n\nYoki  \"<b>📞 Telefon raqamini yuborish</b>\"  tugmasini bosing:\n\n<i>Masalan: +998912345678</i>", reply_markup=get_phone_markup)
            await RegUser.phone_number.set()
        else:
            
            await message.answer("Tizimga kirish uchun iltimos <b>telefon raqamingizni kiriting</b>:", reply_markup=ReplyKeyboardRemove())
            await SignIn.phone_number.set()
        

@dp.message_handler(content_types=['contact'], state=RegUser.phone_number)
@dp.message_handler(state=RegUser.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    if message.text:
        phone_number = message.text
        if phone_number[:4] == "+998" and 9 < len(phone_number) <= 15:
            check_number = await db.select_reg_user(phone_number=str(phone_number))
            if not check_number:
                await state.update_data({"phone_numer":phone_number})
                await message.answer("Iltimos, <b>xavfsiz parol</b> o'ylab to'ping:", reply_markup=ReplyKeyboardRemove())
                await RegUser.password.set()
            else:
                await message.answer("Siz kiritgan raqam tizimda mavjud!")
        else:
            await message.answer("Noto'g'ri telefon raqam kiritgansiz\n\nIltimos, haqiqiy <b>telefon raqamingizni</b> kiriting\n\n<i>Masalan: +998912345678</i>")
    elif message.contact:
        phone_number = message.contact.phone_number
        if phone_number[:3] == "998" or phone_number[:4] == "+998" and 9 < len(phone_number) <= 15:
             await state.update_data({"phone_numer":phone_number})
             await message.answer("Iltimos, <b>xavfsiz parol</b> o'ylab to'ping:", reply_markup=ReplyKeyboardRemove())
             await RegUser.password.set()
        else:
            await message.answer("Noto'g'ri telefon raqam yubordingiz\n\nIltimos, haqiqiy <b>telefon raqamingizni</b> kiriting\n\n<i>Masalan: +998912345678</i>")
        
@dp.message_handler(state=RegUser.password)
async def get_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = data['phone_numer']
    password = message.text
    if 8 <= len(password) <= 255 and password != "12345678":
        check_passoword = await db.select_reg_user(password=str(password))
        if not check_passoword:
            await message.answer(f"<b>Telefon raqam:</b> {phone_number}\n<b>Parol:</b> {password}\n\nMa'lumotlarning to'g'riligini tekshiring:", reply_markup=get_info_reg_user) 
            await state.update_data({"password":password})
            await RegUser.check.set()
        else:
            await message.answer("Ushbu parol allaqachon kiritilgan iltimos, boshqa parolni kiriting:")
    else:
        await message.answer("Parolingizda kamida 8 ta belgi bo'lishi kerak!")

@dp.callback_query_handler(text = ['yes', "no"], state=RegUser.check)
async def checkg(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == 'yes':
        data = await state.get_data()
        phone_number = data['phone_numer']
        password = data['password']
        user = await db.select_user(telegram_id=int(call.from_user.id))
        await db.add_reg_user(user_id=int(user['id']), phone_number=phone_number, password=password)
        await call.message.answer("🥳")
        await call.message.answer("<b>Siz muvaffaqiyatli ro'yxatdan o'tdingiz ✅</b>\n\nSizni qiziqtirgan bo'limni tanlang:", reply_markup=main_markup)
    else:
        await call.message.answer("Ma'lumotlar o'chirildi!")
        await call.message.answer("Qayta ro'yxatdan o'tish uchun /start - tugmasini bosing!")
        await state.finish()