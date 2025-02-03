from aiogram.dispatcher import FSMContext
from aiogram.types import Message

# === Локальные модули ===
import logging
from app import dp, translate
from app.states import Application
from app import database as db
from app import keyboards as kb


@dp.message_handler(state=Application.text)
async def Application(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    try:
        async with state.proxy() as data:
            text = data['text'] = message.text
        user_name = message.from_user.first_name

        user_phone = db.getUserPhoneById(message.from_user.id)

        db.AddApplication(user_name, user_phone, text)
        await message.answer(f"{translate(f'{lang}', 'application_text')}", reply_markup=kb.userMenu(lang))
        await state.finish()

    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.userMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
        await state.finish()

