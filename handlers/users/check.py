from loader import dp, bot
from data.config import CHANNELS
from utils.misc import subscription
from aiogram import types
from keyboards.inline.subscription import check_button
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
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

@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    final_status = True
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            final_status *= status
            result += f"✅ <b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        
        else:
            final_status *= False
            invite_link = await channel.export_invite_link()
            result += (f"❌ <a href='{invite_link}'><b>{channel.title}</b></a> kanaliga obuna bo'lmagansiz.\n\n")
    
    if final_status:
        await call.message.delete()
        full_name = call.from_user.full_name
        user = await db.select_user(telegram_id=call.from_user.id)
        if call.message.text != "🏠 Asosiy menyu":
          await call.message.answer(f"Xush kelibsiz, {make_title(full_name)}\!", parse_mode=types.ParseMode.MARKDOWN_V2)
          user = await db.select_user(telegram_id=int(call.from_user.id))
          reg_user = await db.select_reg_user(user_id=int(user['id']))
          signin_user = await db.select_signin_user(user_id=int(user['id']))
          if reg_user:
              await call.message.answer("Sizni qiziqtirgan bo'limni tanlang:", reply_markup=main_markup)
          elif signin_user:
              await call.message.answer("Siz muvaffaqiyatli tizimga kirdingiz!", reply_markup=main_markup_signin)
          else:
              await call.message.answer("Siz hali tizimga kirmagansiz!", reply_markup=log_markup)
    else:
        await call.message.delete()
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=check_button)