import os
import logging
import pandas as pd

# === Локальные модули ===
from app import app, translate
from app import database as db
from app import keyboards as kb


def read_contacts_from_excel(file_path, lang):
    data = pd.read_excel(file_path)
    if not {'Имя', 'Юзернейм'}.issubset(data.columns):
        raise ValueError(f"{translate(f'{lang}', 'columns_excel')}")
    return data

async def add_user_by_excel(group_name, message):
    user_lang = db.getUserLang(message.from_user.id)
    group = db.getGroupByName(group_name)
    document = message.document
    group = group[0]
    date = group[0]
    time = group[1]
    subject = group[2]
    teacher = group[3]
    lang = group[4]
    group_mode = group[5]
    link = group[6]
    if not document.file_name.endswith('.xlsx'):
        await message.reply(f"{translate(f'{lang}', 'wrong_excel')}")
        return
    file_path = f"res/groups/{document.file_name}"
    await document.download(destination_file=file_path)
    try:
        contacts = read_contacts_from_excel(file_path, user_lang)

        for _, row in contacts.iterrows():
            name = row['Имя']
            username = str(row['Юзернейм'])
            try:
                message_text = f"{translate(f'{lang}', 'send_message_text').format(name=name, subject=db.getSubjectById(subject), date=date, time=time,teacher=db.getTeacherNameById(teacher), lang=lang.capitalize(), group_mode=group_mode.capitalize(), link=link)}"
                username = await app.get_users(username)
                await app.send_message(chat_id=username.id, text=message_text)

            except Exception:
                await message.answer(f"{translate(f'{user_lang}', 'error_with_sending').format(name=name, username=username)}")

        await message.reply(f"{translate(f'{user_lang}', 'send_message_successfully')}", reply_markup=kb.adminMenu(user_lang))
    except Exception as e:
        await message.answer(f"{translate(f'{lang}', 'error_text')}", reply_markup=kb.adminMenu(lang))
        logging.error(f"{translate(f'{lang}', 'error')}" + f"{e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
