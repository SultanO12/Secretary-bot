from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.malumotalar_mark import malumotlar_markup

@dp.message_handler(text="🗂 Ma'lumotlar")
async def do_malumotlar(message: types.Message, state: FSMContext):
    await message.answer("Siz <b>\"Ma'lumotlar\"</b> bo'limidasiz:", reply_markup=malumotlar_markup)