import os
import pandas as pd
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType

# === Локальные модули ===
import logging
from app import dp, app
from app.states import GroupName
from app import database as db
from app import keyboards as kb


def read_contacts_from_excel(file_path):
    data = pd.read_excel(file_path)
    if not {'Имя', 'Телефон'}.issubset(data.columns):
        raise ValueError("Файл должен содержать столбцы: 'Имя' и 'Телефон'")
    return data

@dp.callback_query_handler(state=GroupName.name)
async def GroupNameHangler(callback: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = callback.data[7:]
        await callback.message.delete()
        await callback.message.answer('📂 Отправьте Excel файл (.xlsx)')
        await GroupName.next()
    except Exception as e:
        await callback.message.answer(
            f"❗ Ошибка: {e}\nПопробуйте снова. \nЕсли ошибка не исчезает , пожалуйста, свяжитесь с администратором. Мы быстро решим все вопросы! 🔧")
        logging.error(f"Произошла ошибка: {e}")
        await state.finish()


@dp.message_handler(state=GroupName.mana, content_types=ContentType.DOCUMENT)
async def handle_file(message: Message, state: FSMContext):
    async with state.proxy() as data:
        group_name = data['name']

    group = db.getGroupByName(group_name)
    document = message.document
    group = group[0]
    date = group[0]
    time = group[1]
    subject = group[2]
    teacher = group[3]
    lang = group[4]
    type = group[5]
    link = group[6]
    if not document.file_name.endswith('.xlsx'):
        await message.reply("Пожалуйста, отправьте файл в формате Excel (.xlsx)")
        return
    file_path = f"res/groups/{document.file_name}"
    await document.download(destination_file=file_path)
    try:
        # Читаем контакты из Excel
        contacts = read_contacts_from_excel(file_path)
        # Запускаем Pyrogram для отправки сообщений
        for _, row in contacts.iterrows():
            name = row['Имя']
            phone = str(row['Юзернейм'])
            try:
                # Формируем персонализированное сообщение
                message_text = f"Здравствуйте, <b>{name}</b>! 🌟\nС радостью сообщаем, что ваша группа по курсу <b>{db.getSubjectById(subject)}</b> стартует <b>{date}</b> в <b>{time}</b>! ⏰\nВы будете учиться с нашим замечательным преподавателем — <b>{db.getTeacherNameById(teacher)}</b>, который проведет увлекательное занятие. 📚✨\nЯзык занятия: <b>{lang.capitalize()}</b>\nФормат: <b>{type.capitalize()}</b>\nА вот и ссылка на группу, где вы встретите свою команду и начнете путь к новым знаниям:\n🔗 <b>{link}</b>\nГотовы начать? Мы ждем вас с нетерпением! Если возникнут вопросы или потребуется помощь, не стесняйтесь обращаться. 😉\nУвидимся на занятии! 🚀"
                # Отправляем сообщение (найдите ID пользователя, если требуется)
                user = await app.get_users(phone)
                await app.send_message(chat_id=user.id, text=message_text)
            except Exception as e:
                await message.answer(f"Не возможно отправить сообщение для {name} ({phone})")

        await message.reply("📤 Сообщения успешно отправлены!")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
        logging.error(f"Произошла ошибка: {e}")
    finally:
        # Удаляем временный файл
        if os.path.exists(file_path):
            os.remove(file_path)

    await state.finish()
