from aiogram.dispatcher import FSMContext
from aiogram.types import Message

# === Локальные модули ===
import logging
from app import dp, bot
from app.states import Reason
from app import database as db
from app import keyboards as kb

@dp.message_handler(state=Reason.reason)
async def CancelLessonReason(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            reason = data['reason'] = message.text

        db.cancelAllLesson()
        lessons = db.getTodayLesson()
        for x in lessons:
            await bot.send_message(db.getTgId(x[0]), f"😔 К сожалению, урок на сегодня был отменен\nПричина: {reason} ")
        await message.answer(f'Уроки у всех групп на сегодня были отменены, и все были предупреждены. 🚫📚')
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer(
            f"❗ Ошибка: {e}\nПопробуйте снова. \nЕсли ошибка не исчезает , пожалуйста, свяжитесь с администратором. Мы быстро решим все вопросы! 🔧")
        logging.error(f"Произошла ошибка: {e}")
