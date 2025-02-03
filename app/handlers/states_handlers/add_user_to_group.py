from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType

# === Локальные модули ===
import logging
from app import dp, translate
from app.states import AddUsertoGroup
from app.utils import add_user_by_excel
from app import database as db


@dp.callback_query_handler(state=AddUsertoGroup.name)
async def GroupNameHangler(callback: CallbackQuery, state: FSMContext):
    lang = db.getUserLang(callback.from_user.id)
    try:
        async with state.proxy() as data:
            data['name'] = callback.data[7:]
        await callback.message.delete()
        await callback.message.answer(f"{translate(f'{lang}', 'send_excel_text')}")
        await AddUsertoGroup.next()
    except Exception as e:
        await callback.message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.adminMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
        await state.finish()

@dp.message_handler(state=AddUsertoGroup.get_doc, content_types=ContentType.DOCUMENT)
async def AddUserByExcel(message: Message, state: FSMContext):
    async with state.proxy() as data:
        group_name = data['name']

    await add_user_by_excel(group_name, message)
    await state.finish()

