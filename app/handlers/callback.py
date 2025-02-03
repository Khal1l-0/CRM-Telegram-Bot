import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

# === Локальные модули ===
from app import dp, translate
from app import database as db
from app import keyboards as kb
from app.states import AddGroup, SetLanguage


@dp.callback_query_handler(lambda callback: callback.data == 'add-group')
async def callback_add_group(callback: CallbackQuery):
    await callback.message.delete()
    lang = db.getUserLang(callback.message.chat.id)
    await callback.message.answer(f"{translate(f'{lang}', 'group_name')}")
    await AddGroup.name.set()

@dp.callback_query_handler(lambda callback: callback.data == 'back-to-group')
async def callback_cert_uz(callback: CallbackQuery):
    lang = db.getUserLang(callback.message.chat.id)
    try:
        await callback.message.delete()
        my_id = callback.message.chat.id
        role = db.getUserRole(my_id)[0]
        if role == 'teacher':
            await callback.message.answer(translate(f'{lang}', 'my_groups', 'teacher'), reply_markup=kb.getMyGroups(my_id))
        else:
            await callback.message.answer(translate(f'{lang}', 'groups', 'admin'), reply_markup=kb.groupsMenu(0))

    except Exception as e:
        await callback.message.answer(f"{translate(f'{lang}', 'error_text')}")
        logging.error(f"{translate(f'{lang}', 'error')}")


@dp.callback_query_handler(lambda callback: callback.data.startswith('lang'), state=SetLanguage.lang)
async def callback_user_language(callback: CallbackQuery, state: FSMContext):
    lang = callback.data[5:]
    user = db.getUserRole(callback.message.from_user.id)
    async with state.proxy() as data:
        data['lang'] = lang

    if user:
        db.ChangeUserLang(callback.message.from_user.id, lang)
        await callback.message.delete()
        await callback.message.answer(f"{translate(f'{lang}', 'change_lang_success')}")
    else:
        await callback.message.delete()
        await callback.message.answer(f"{translate(f'{lang}','send_contact')}", reply_markup=kb.send_contact(lang))

@dp.callback_query_handler()
async def callback_group(callback: CallbackQuery):
    lang = db.getUserLang(callback.message.chat.id)
    try:
        data = callback.data
        for i in db.getGroupsName():
            if data == f'group-{i}':
                await callback.message.delete()
                group = db.getGroup(i)[0]
                if group[3] == '1-3-5':
                    day = f"{translate(f'{lang}', 'odd_days')}"
                elif group[3] == '0-2-4':
                    day = f"{translate(f'{lang}', 'even_days')}"
                await callback.message.answer(f"{translate(f'{lang}', 'group_info').format(name=group[1], group_id=group[0], date=group[2], time=group[4], day=day, subject= db.getSubjectById(group[5][:4]), teacher=db.getNameById(group[6]), lang=group[7].capitalize(), group_mode=group[8].capitalize(), link=group[9])}", parse_mode='HTML', reply_markup=kb.backGroup(lang))

        if data.startswith("prev_") or data.startswith("next_"):
            # Обработка навигации
            page = int(data.split('_')[1])
            await callback.message.edit_reply_markup(reply_markup=kb.groupsMenu(page))
        elif data.startswith("mprev_") or data.startswith("mnext_"):
            page = int(data.split('_')[1])
            await callback.message.edit_reply_markup(reply_markup=kb.AddMemberGroup(page))

    except Exception as e:
        await callback.message.answer(
            f"{translate(f'{lang}','error_text')}")
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
