import logging
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

# === Локальные модули ===
from app import dp, translate
from app.states import AddGroup
from app import database as db
from app import keyboards as kb
from app.utils import create_supergroup


@dp.callback_query_handler(lambda callback: callback.data == 'confirm-group', state=AddGroup)
async def callback_confirm_group(callback: CallbackQuery, state: FSMContext):
    user_lang = db.getUserLang(callback.from_user.id)
    await callback.message.delete()
    async with state.proxy() as data:
        name = data.get('name')
        date = data.get('date')
        time = data.get('time')
        subject = data.get('subject')
        teacher = data.get('teacher')
        lang = data.get('lang')
        group_mode = data.get('group_mode')

    await state.finish()

    await callback.message.answer('⏳')
    link = await create_supergroup(name, date, time, subject, teacher, lang, group_mode)
    await callback.message.answer(f"{translate(f'{user_lang}', 'create_group').format(name=name, link=link)}", reply_markup=kb.adminMenu(user_lang))

@dp.callback_query_handler(lambda callback: callback.data == 'cancel-group', state=AddGroup)
async def callback_confirm_group(callback: CallbackQuery, state: FSMContext):
    user_lang = db.getUserLang(callback.from_user.id)

    await callback.message.delete()
    await state.finish()

    await callback.message.answer(f"{translate(f'{user_lang}', 'cancel_group')}", reply_markup=kb.adminMenu(user_lang))


@dp.message_handler(state=AddGroup.name)
async def AddGroupName(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)
    async with state.proxy() as data:
        data['name'] = message.text
    today = datetime.today()
    await message.answer(f"{translate(f'{lang}', 'group_date')}", reply_markup=kb.getCalendar(today.year, today.month, lang))
    await AddGroup.next()

@dp.callback_query_handler(lambda c: c.data.startswith('calendar'), state=AddGroup.date)
async def AddGroupDate(callback: CallbackQuery, state: FSMContext):
    lang = db.getUserLang(callback.from_user.id)
    data = callback.data.split(':')
    action = data[3] if len(data) > 3 else None
    if action == 'nav':  # Навигация по месяцам
        year, month = int(data[1]), int(data[2])
        # Исправление перехода между годами
        if month == 0:  # Если месяц стал 0, переходим на декабрь предыдущего года
            year -= 1
            month = 12
        elif month == 13:  # Если месяц стал 13, переходим на январь следующего года
            year += 1
            month = 1
        # Обновляем сообщение с новым календарём
        await callback.message.edit_reply_markup(reply_markup=kb.getCalendar(year, month, lang))

    else:  # Выбор даты
        try:
            year, month, day = map(int, data[1:])  # Преобразуем данные из callback
            selected_date = datetime(year, month, day)

            async with state.proxy() as data:
                data['date'] = selected_date.strftime('%d.%m.%Y')

            days = datetime.weekday(selected_date)
            await callback.message.delete()

            if days in (0, 1, 2, 3, 4, 5):
                await AddGroup.next()
                await callback.message.answer(f"{translate(f'{lang}', 'group_time')}", reply_markup=kb.groupTime())

            else:
                await callback.message.answer(f"{translate(f'{lang}', 'wrong_date')}",reply_markup=kb.adminMenu(lang))
                await state.finish()

        except Exception as e:
            await callback.message.answer(f"{translate(f'{lang}', 'error_text')}")
            logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")

@dp.message_handler(state=AddGroup.time)
async def AddGroupTime(message: Message, state: FSMContext):
    lang = db.getUserLang(message.from_user.id)

    async with state.proxy() as data:
        time = data['time'] = message.text

    try:
        time_obj = datetime.strptime(time, "%H:%M")
        await message.answer(f"{translate(f'{lang}', 'group_time')}", reply_markup=kb.subjectsList())
        await AddGroup.next()
    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.adminMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
        await state.finish()

@dp.callback_query_handler(state=AddGroup.subject)
async def AddGroupSubject(callback: CallbackQuery, state: FSMContext):
    lang = db.getUserLang(callback.from_user.id)
    await callback.message.delete()
    subject = callback.data[8:]
    db.getTeachersBySubject(subject)

    async with state.proxy() as data:
        data['subject'] = subject

    await callback.message.answer(f"{translate(f'{lang}', 'group_teacher')}", reply_markup=kb.getTeachersBySubject(subject))
    await AddGroup.next()

@dp.callback_query_handler(state=AddGroup.teacher)
async def AddGroupTeacher(callback: CallbackQuery, state: FSMContext):
    lang = db.getUserLang(callback.from_user.id)
    await callback.message.delete()
    async with state.proxy() as data:
        data['teacher'] = callback.data

    await callback.message.answer(f"{translate(f'{lang}', 'group_lang')}", reply_markup=kb.langList())
    await AddGroup.next()

@dp.callback_query_handler(state=AddGroup.lang)
async def AddGroupLang(callback: CallbackQuery, state: FSMContext):
    user_lang = db.getUserLang(callback.from_user.id)
    await callback.message.delete()
    lang = callback.data[6:]
    async with state.proxy() as data:
        data['lang'] = lang
    await callback.message.answer(f"{translate(f'{user_lang}', 'group_lang')}", reply_markup=kb.groupMode(user_lang))
    await AddGroup.next()

@dp.callback_query_handler(state=AddGroup.group_mode)
async def AddGroupType(callback: CallbackQuery, state: FSMContext):
    user_lang = db.getUserLang(callback.from_user.id)
    await callback.message.delete()
    async with state.proxy() as data:
        group_mode = data['group_mode'] = callback.data
        name = data['name']
        date = data['date']
        time = data['time']
        subject = data['subject']
        teacher = data['teacher']
        lang = data['lang']

    selected_day = datetime.strptime(date, "%d.%m.%Y")
    week_day = datetime.weekday(selected_day)
    day = ''
    if week_day in (0, 2, 4):
        day = 'Пн • Ср • Пт'
    elif week_day in (1, 3, 5):
        day = 'Вт • Чт • Сб'

    await callback.message.answer(f"{translate(f'{user_lang}', 'group_create_info').format(name=name, date=date, time=time, day=day, subject=db.getSubjectById(subject), teacher=db.getNameById(teacher), lang=lang.capitalize(),group_mode=group_mode.capitalize())}", reply_markup=kb.confirmGroup(user_lang), parse_mode='HTML')
