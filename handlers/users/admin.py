import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from aiogram.dispatcher import FSMContext
from states.send_message import SendMessage

@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = await db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[-1])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)

@dp.message_handler(text="/get", user_id=ADMINS)
async def get1(message: types.Message):
    infor = await db.select_all_infor()
    for info in infor:
        if info['malumot_text']:
            await message.answer(info['malumot_text'])
        elif info['img']:
            await message.answer_photo(info['img'])
        elif info['video']:
            await message.answer_video(info['video'])
            
@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
        users = await db.select_all_users()
        for user in users:
            user_id = user[-1]
            try:
                await bot.send_message(chat_id=user_id, text="@LifeC0der kanaliga obuna bo'ling!")
                await asyncio.sleep(0.05)
            except:
                await bot.send_message(chat_id=message.from_user.id, text=f"User: {user} - blocked")

    
@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("Baza tozalandi!")

@dp.message_handler(text="/send_message", user_id=ADMINS)
async def get_message(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Введите сообщение:")
    await SendMessage.text.set()

@dp.message_handler(state=SendMessage.text)
async def send(message: types.Message, state: FSMContext):
        users = await db.select_all_users()
        for user in users:
            user_id = user[-1]
            try:
                await bot.send_message(chat_id=int(user_id), text=str(message.text))
                await asyncio.sleep(0.05)
            except:
                await bot.send_message(chat_id=message.from_user.id, text=f"User: {user} - blocked")
        await bot.send_message(chat_id=message.from_user.id, text="Successfully!")
        await state.finish()