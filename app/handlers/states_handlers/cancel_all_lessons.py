from aiogram.dispatcher import FSMContext
from aiogram.types import Message

# === Локальные модули ===
import logging
from app import dp, bot, translate
from app.states import CancelAllLessons
from app import database as db
from app import keyboards as kb

@dp.message_handler(state=CancelAllLessons.reason)
async def CancelLessonReason(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    try:
        async with state.proxy() as data:
            reason = data['reason'] = message.text

        lessons = db.getTodayLesson()
        db.cancelAllLesson()

        for x in lessons:
            await bot.send_message(db.getTgId(x[0]), f"{translate(f'{db.getGroupLangById(x[0])}', 'groups_warning_text').format(reason=reason)}")
        await message.answer(f"{translate(f'{lang}', 'all_groups_warning').format(reason=reason)}")
        await state.finish()
    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.adminMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
        await state.finish()
