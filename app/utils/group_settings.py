from datetime import datetime

from aiogram.types import InputFile
from pyrogram.errors import UserPrivacyRestricted
from pyrogram.types import ChatPrivileges

# === Локальные молули ===
from app import bot, app, translate
from app.bot import BOT_LINK
from app import database as db


async def create_supergroup(name, date, time, subject, teacher, lang, group_mode) -> str:
    new_group = await app.create_supergroup(f'GROUP {name}', f"{translate(f'{lang}', 'group_desc').format(date=date, time=time, teacher=db.getTeacherNameById(teacher))}")
    tg_group_id = new_group.id
    get_link = await app.create_chat_invite_link(tg_group_id)
    link = get_link.invite_link

    bot_user = await app.get_users(BOT_LINK)
    await app.add_chat_members(tg_group_id, bot_user.id)
    privileges = ChatPrivileges(
        can_manage_chat=True,
        can_change_info=True,  # Разрешение изменять информацию о группе
        can_delete_messages=True,  # Разрешение удалять сообщения
        can_restrict_members=True,  # Разрешение блокировать участников
        can_invite_users=True,  # Разрешение приглашать пользователей
        can_pin_messages=True,  # Разрешение закреплять сообщения
        can_promote_members=True,  # Запрет назначать других администраторов
        is_anonymous=False  # Администратор не является анонимным
    )
    await app.promote_chat_member(chat_id=tg_group_id, user_id=bot_user.id, privileges=privileges)

    photo_path = 'app/res/pattern/group-photo.png'
    photo = InputFile(photo_path)
    await bot.set_chat_photo(chat_id=tg_group_id, photo=photo)

    teacher_id = db.getTeacherById(teacher)
    user_lang = db.getUserLang(teacher_id)

    day = datetime.strptime(date, "%d.%m.%Y")
    day = datetime.weekday(day)
    days = ''
    if day in (0, 2, 4):
        days = '0-2-4'
    elif day in (1, 3, 5):
        days = '1-3-5'

    max_lessons = db.getMaxLessson(subject)
    db.AddGroup(name, date, days, time, subject, teacher, lang, group_mode, link, tg_group_id, max_lessons)

    try:
        await app.add_chat_members(tg_group_id, teacher_id)
        await app.promote_chat_member(chat_id=tg_group_id, user_id=teacher_id, privileges=privileges)
        await bot.send_message(teacher_id, f"{translate(f'{user_lang}', 'add_to_group').format(name=name, link=link)}")

    except UserPrivacyRestricted:
        await bot.send_message(teacher_id, f"{translate(f'{user_lang}', 'error_to_add_group').format(name=name, link=link)}", parse_mode='HTML')

    finally:
        return link