from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from googletrans import Translator

# === Локальные модули ===
import logging
from app import dp, translate
from app.states import AddStuff
from app import database as db
from app import keyboards as kb

@dp.message_handler(state=AddStuff.name)
async def AddStuffName(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    try:
        async with state.proxy() as data:
            data['name'] = message.text
        await message.answer(f"{translate(f'{lang}', 'write_phone')}")
        await AddStuff.next()
    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.ceoMenu())
        logging.error(f"{translate(f'{lang}', 'error')}")
        await state.finish()
        
@dp.message_handler(state=AddStuff.phone)
async def AddStuffPhone(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    async with state.proxy() as data:
        phone = data['phone'] = message.text

    try:
        user = db.findUserByPhone(int(phone))
        if user:
            user_role = user[5]
            # Если пользователь существует как сотрудник
            if user_role == 'admin' or user_role == 'teacher':
                await message.answer(f"{translate(f'{lang}', 'employee_in_db').format(role=user_role.capitalize())}",
                                     reply_markup=kb.ceoMenu(lang))
                await state.finish()

            # Если пользователь не сотрудник
            else:
                await message.answer(f"{translate(f'{lang}', 'choose_employee_role')}", reply_markup=kb.roleMenu(lang))
                await AddStuff.next()

        # Если нету такого пользователя
        else:
            await message.answer(f"{translate(f'{lang}', 'choose_employee_role')}", reply_markup=kb.roleMenu(lang))
            await AddStuff.next()

    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.ceoMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
        await state.finish()


@dp.callback_query_handler(state=AddStuff.role)
async def AddStuffRole(callback: CallbackQuery, state: FSMContext):
    lang = db.getUserLang(callback.from_user.id)
    async with state.proxy() as data:
        name = data['name']
        role = data['role'] = callback.data
        phone = data['phone']
    # Если учитель
    if role == 'teacher':
        await callback.message.delete()
        await callback.message.answer(f"{translate(f'{lang}', 'group_subject')}", reply_markup=kb.subjectsList())
        await AddStuff.next()
    # Если просто админ
    if role == 'admin':
        user = db.findUserByPhone(phone)
        if user:
            db.UpdateStuff(name, phone, role)
        else:
            db.AddStuff(name, phone, role)
        await state.finish()
        await callback.message.delete()
        await callback.message.answer(f"{translate(f'{lang}', 'add_employee_successfully')}", reply_markup=kb.ceoMenu(lang))

@dp.callback_query_handler(state=AddStuff.subject)
async def AddStuffSubject(callback: CallbackQuery, state: FSMContext):
    lang = db.getUserLang(callback.from_user.id)
    async with state.proxy() as data:
        subject = data['subject'] = callback.data[8:]
        name = data['name']
        phone = data['phone']
        role = data['role']
    
    trans = Translator()
    translated = trans.translate(name, src="ru", dest="en")
    name_id = subject + '_' + str(translated.text).lower()
    user = db.findUserByPhone(phone)
    if user:
        db.UpdateStuff(name, phone, role, subject, name_id)
    else:
        db.AddStuff(name, phone, role, subject, name_id)
    await state.finish()
    await callback.message.delete()
    await callback.message.answer(f"{translate(f'{lang}', 'add_employee_successfully')}", reply_markup=kb.ceoMenu(lang))
            