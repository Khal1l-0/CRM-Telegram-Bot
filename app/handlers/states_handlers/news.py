from aiogram.dispatcher import FSMContext
from aiogram.types import Message

# === Локальные модули ===
import logging
from app import dp, bot, translate
from app.keyboards import adminMenu
from app.states import News
from app import database as db
from app import keyboards as kb


@dp.message_handler(state=News.text)
async def SendNews(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    try:
        async with state.proxy() as data:
            text = data['text'] = message.text

        ids = []
        for x in db.getAllGroupTgId():
            ids.append(x)

        for x in db.getAllUserTgId():
            ids.append(x)

        for x in ids:
            await bot.send_message(x[0], f'{text}')

        await message.answer(f"{translate(f'{lang}', 'news_send_successfully')}", reply_markup=adminMenu(lang))
        await state.finish()
    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.adminMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
        await state.finish()
