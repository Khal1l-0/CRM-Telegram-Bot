import logging
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from googletrans import Translator

# === Локальные модули ===
from app import dp, translate
from app.states import AddSubject
from app import database as db
from app import keyboards as kb


@dp.message_handler(state=AddSubject.name)
async def AddSub(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(f"{translate(f'{lang}', 'course_max_lessons')}")
    await AddSubject.next()

@dp.message_handler(state=AddSubject.max_lessons)
async def AddSubLes(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    try:
        async with state.proxy() as data:
            max_lessons = data['max_lessons'] = int(message.text)
            message_text = data['name']

        trans = Translator()
        name = message_text
        translated = trans.translate(name, src="ru", dest="en")
        id_name = str(translated.text).lower()[:4]

        db.AddSubject(name, id_name, max_lessons)
        await state.finish()
        await message.answer(f"{translate(f'{lang}', 'add_subject_successfully')}", reply_markup=kb.ceoMenu(lang))
    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.adminMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
        await state.finish()
