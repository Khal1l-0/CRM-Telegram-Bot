from aiogram.types import Message, InputFile
from aiogram.dispatcher import FSMContext

from app import dp, bot, translate
from app import database as db
from app import keyboards as kb
from app.states import GenCer
from app import gen_certificate


@dp.message_handler(state=GenCer.name)
async def GenCerName(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    async with state.proxy() as data:
        name = data['name'] = message.text

    await gen_certificate(name)
    cer_path = f'app/res/certificates/{name}.jpg'
    file = InputFile(cer_path)
    await bot.send_document(message.from_user.id, file, caption=f'{name}', reply_markup=kb.adminMenu(lang))
    await state.finish()

# @dp.message_handler(state=GenCer.date)
# async def GenCerDate(message: Message, state: FSMContext):
#     lang = db.getUserLang(message.from_user.id)
#
#     async with state.proxy() as data:
#         data['date'] = message.text
#
#
#     await message.answer(f"{translate(f'{lang}', 'cer_date', 'admin')}")