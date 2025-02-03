from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

# === Локальные модули ===
import logging
from app import dp, bot, translate
from app.keyboards import adminMenu
from app.states import CancelLesson
from app import database as db
from app import keyboards as kb


@dp.callback_query_handler(state=CancelLesson.group_id)
async def CancelLessonName(callback: CallbackQuery, state: FSMContext):
    lang = db.getUserLang(callback.from_user.id)
    group_name = callback.data[7:]
    group_id = db.getGroupIdByName(group_name)
    async with state.proxy() as data:
        data['group_id'] = group_id
    await callback.message.delete()
    await callback.message.answer(f"{translate(f'{lang}', 'reason', 'admin')}")
    await CancelLesson.next()


@dp.message_handler(state=CancelLesson.reason)
async def CancelLessonReason(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    try:
        async with state.proxy() as data:
            reason = data['reason'] = message.text
            group_id = data['group_id']
        db.cancelTodayLesson(group_id)
        await bot.send_message(db.getTgId(group_id), f"{translate(f'{db.getGroupLangById(group_id)}', 'groups_warning_text').format(reason=reason)}")
        await message.answer(f"{translate(f'{lang}', 'one_group_warning').format(group=db.getGroupById(group_id)[0][0], reason=reason)}", reply_markup=adminMenu(lang))
        await state.finish()
    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.adminMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
        await state.finish()
