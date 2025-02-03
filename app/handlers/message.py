import os
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

# === Локальные модули ===
from app import dp
from app import database as db
from app import keyboards as kb
from app import bot, DEV
from app.states import *
from app import translate

async def main_menu(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAEMjkFmpmYJWMyEztqxF_ks75RP9w3mRQAC0wADVp29CvUyj5fVEvk9NQQ')
    user = db.getUserRole(message.from_user.id)[0]
    lang = db.getUserLang(message.from_user.id)
    if user == 'ceo':
        await message.answer(text=f"{translate(f'{lang}', 'welcome', 'ceo')}", reply_markup=kb.ceoMenu(lang))
    elif user == 'admin':
        await message.answer(text=f"{translate(f'{lang}', 'welcome', 'admin')}", reply_markup=kb.adminMenu(lang))
    elif user == 'teacher':
        await message.answer(text=f"{translate(f'{lang}', 'welcome', 'teacher')}", reply_markup=kb.teacherMenu(lang))
    elif user == 'god':
        await message.answer(text=f'📚 Добро пожаловать мой Создатель !', reply_markup=kb.godMenu())
    else:
        await message.answer(text=f"{translate(f'{lang}', 'welcome', 'user')}" + f'{message.from_user.first_name}' + '👋', reply_markup=kb.userMenu(lang))

@dp.message_handler(content_types=['contact'], state=SetLanguage)
async def register_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lang = data['lang']
    tg_id = message.from_user.id
    if message.contact.user_id != tg_id:
        await message.reply(f"{translate(f'{lang}', 'send_your_contact')}")
    else:
        username = message.from_user.username
        name = message.from_user.first_name
        phone = message.contact.phone_number
        userbyphone = db.findUserByPhone(phone)
        if userbyphone:
            db.UpdateStuffByPhone(tg_id, username, lang, phone)
        else:
            db.AddUser(tg_id, name, phone, username, lang)
        await state.finish()
        await message.answer(f"{translate(f'{lang}', 'authorization')}")
        await main_menu(message)

@dp.message_handler(commands=['start'], state='*')
async def start_command(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    if message.chat.type in 'private':
        await state.finish()
        user= db.getUserRole(tg_id)
        if user:
            lang = db.getUserLang(tg_id)
            await message.answer(translate(f'{lang}', 'authorization'))
            await main_menu(message)
        else:
            await message.answer('Пожалуйста, выберите удобный язык.\nPlease select your preferred language.\nIltimos, qulay tilni tanlang.', reply_markup=kb.setUserLang())
            await SetLanguage.lang.set()

# @dp.message_handler(commands=['getGroupInfo'])
# async def get_group_info_command(message: Message):
#     if message.chat.type in ['group', 'supergroup']:
#         group = db.getGroupByTgId(message.chat.id)
#         group = group[0]
#         day = ''
#         if group[3] == '1-3-5':
#             day = 'Пн • Ср • Пт'
#         elif group[3] == '0-2-4':
#             day = 'Вт • Чт • Сб'
#         await message.reply(f'🎓 Информация о группе\n╔═══════════════════╗\n🔥 Группа: GROUP {group[1]}\n🆔 ID: {group[0]}\n📅 Старт: {group[2]}\n⏰ Время: {group[4]} (GMT+5)\n📚 Дни: {day}\n✏️ Предмет: {db.getSubjectById(group[5][:4])}\n👨‍🏫 Преподаватель: {db.getNameById(group[6])}\n🌍 Язык: {group[7].capitalize()}\n🔗 Формат: {group[8].capitalize()}\n╚═══════════════════╝\n')

@dp.message_handler(commands=['godMode'])
async def god_command(message: Message):
    if message.from_user.id == int(DEV):
        db.changeRoleForGod(message.from_user.id)
        await message.answer('Режим Бога включено⚡️', reply_markup=kb.godMenu())
    else:
        await message.answer('Не понятно🤷‍♂️')

@dp.message_handler(commands=['godModeOff'])
async def god_command(message: Message):
    if message.from_user.id == int(DEV):
        db.changeRoleForUser(message.from_user.id)
        await message.answer('Режим Бога отключено❌', reply_markup=kb.userMenu('ru'))
    else:
        await message.answer('Не понятно🤷‍♂️')


# === ===
async def fallback(message: Message, lang):
    await message.reply(f"{translate(f'{lang}', 'idk')}")

async def admin_commands(message: Message, lang):
    if message.text == translate(f'{lang}', 'groups', 'admin'):
        await message.answer(f"{translate(f'{lang}', 'groups', 'admin')}", reply_markup=kb.groupsMenu(0))
    elif message.text == translate(f'{lang}', 'add_member', 'admin'):
        await message.answer(f"{translate(f'{lang}', 'choose_group_to_add', 'admin')}", reply_markup=kb.AddMemberGroup(0))
        await AddUsertoGroup.name.set()
    
    elif message.text == translate(f'{lang}', 'today_lessons', 'admin'):
        data = ''
        lessons = db.getTodayLesson()
        for x in lessons:
            name = db.getGroupById(x[0])[0]
            teacher = db.getTeacherNameById(x[3])
            subject = db.getGroupById(x[0])[0]
            time = x[2]
            data += f"{translate(f'{lang}', 'group_info_text', 'admin').format(name=name[0], subject=db.getSubjectById(subject[2]), teacher=teacher, time=time)}\n"
        if len(lessons) <= 0:
            await message.answer(f"{translate(f'{lang}', 'no_lessons_text', 'admin')}", reply_markup=kb.adminMenu(lang), parse_mode='HTML')
        else:
            await message.answer(f"{translate(f'{lang}', 'today_lessons_text', 'admin')}" + f"{data}", reply_markup=kb.adminMenu(lang),parse_mode='HTML')
                         
    elif message.text == translate(f'{lang}', 'cancel_lesson', 'admin'):
        if not kb.todayGroups().inline_keyboard:
            await message.answer(f"{translate(f'{lang}','no_lessons_text', 'admin')}", reply_markup=kb.adminMenu(lang), parse_mode='HTML')
        else:
            await message.answer(f"{translate(f'{lang}', 'choose_group_to_cancel', 'admin')}", reply_markup=kb.todayGroups())
            await CancelLesson.group_id.set()

    elif message.text == translate(f'{lang}','news', 'admin'):
        await message.answer(f"{translate(f'{lang}', 'text_for_news', 'admin')}")
        await News.text.set()

    elif message.text == translate(f'{lang}', 'cancel_all_lessons', 'admin'):
        await message.answer(f"{translate(f'{lang}', f'reason', 'admin')}")
        await CancelAllLessons.reason.set()

    elif message.text == translate(f'{lang}','gen_cer', 'admin'):
        await message.answer(f"{translate(f'{lang}', 'student_name')}")
        await GenCer.name.set()

    # elif message.text == 'Удалить мусор🗑':
        # fileOfCer = os.listdir('res/certificates')
        # count = int(sum(os.path.isfile(os.path.join('res/certificates', f)) for f in fileOfCer))
        # shutil.rmtree('res/certificates/')
        # os.mkdir(os.path.join('res', 'certificates') )
        # if count % 10 == 1 and count % 100 != 11:
        #     await message.answer(f'Удалено {count} файл✅', reply_markup=kb.adminMenu())
        # elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        #     await message.answer(f'Удалено {count} файла✅', reply_markup=kb.adminMenu())
        # else:
        #     await message.answer(f'Удалено {count} файлов ✅',reply_markup=kb.adminMenu())

    elif message.text == f"{translate(f'{lang}', 'applications', 'admin')}":
        txt = f"{translate(f'{lang}', 'applications', 'admin')}" + "\n━━━━━━━━━━━━━━━━━━━\n"
        applications = db.getApplications()
        if len(applications) <= 0:
            txt += f"{translate(f'{lang}', 'no_applications_text', 'admin')}"
        else:
            for x in db.getApplications():
                txt += f"{translate(f'{lang}', 'applications_text', 'admin').format(name=x[1], phone=x[2], application=x[3])}\n"
        await message.reply(txt, parse_mode='HTML')
    
    else:
        await fallback(message, lang)

async def ceo_commands(message: Message, lang):
    if message.text == translate(f'{lang}', 'add_employee', 'ceo'):
        await message.answer(f"{translate(f'{lang}', 'employee_name')}")
        await AddStuff.name.set() 
    elif message.text == translate(f'{lang}', 'add_subject', 'ceo'):
        await message.answer(f"{translate(f'{lang}', 'add_subject_text')}")
        await AddSubject.name.set()
    else:
        await fallback(message, lang)

async def teacher_commands(message: Message, lang):
    if message.text == translate(f'{lang}', 'my_groups', 'teacher'):
        my_id = message.from_user.id
        await message.answer(translate(f'{lang}', 'my_groups', 'teacher'), reply_markup=kb.getMyGroups(my_id))
    elif message.text == translate(f'{lang}', 'today_lessons', 'admin'):
        data = ''
        lessons = db.getTodayTeachersLesson(message.from_user.id)
        for x in lessons:
            name = db.getGroupById(x[0])[0]
            subject = db.getGroupById(x[0])[0]
            time = x[2]
            data += f"{translate(f'{lang}', 'today_lessons', 'teacher').format(name=name[0], subject=db.getSubjectById(subject[2]), time=time)}"
        
        if len(lessons) <= 0:
            await message.answer(f"{translate(f'{lang}', 'no_lessons_text', 'admin')}", reply_markup=kb.teacherMenu(lang), parse_mode='HTML')
        else:
            await message.answer(f"{translate(f'{lang}', 'today_lessons_text', 'admin')}" + f"{data}", reply_markup=kb.teacherMenu(lang), parse_mode='HTML')
            
    else:
        await fallback(message, lang)

async def user_commands(message: Message, lang):
    if message.text == translate(f'{lang}', 'info'):
        await message.answer(f"{translate(f'{lang}', 'info_about_center')}")
    elif message.text == translate(f'{lang}', 'application', 'user'):
        await message.answer(f"{translate(f'{lang}', 'application_text', 'user')}")
        await Application.text.set()
    else:
        await fallback(message, lang)

async def god_commands(message: Message):
    if message.text == '📊 Статистика бота 🔍':
       groups = db.getGroupsName()
       users = db.getUsers()
       await message.reply(f'<b>📊 Статистика бота:</b>\n━━━━━━━━━━━━━━━━━━━\n\n👤 Пользователей: {len(users)}\n👥 Групп: {len(groups)}', parse_mode='HTML')
        
    elif message.text == '🔥 Время для глобальной чистки! 💣':
        await message.answer('💥 Мощное очищение! 💨')
        try:
            group_id = db.getAllGroupTgId()
            for x in group_id:
                await bot.leave_chat(x[0])
            with open('app/logs/bot.log', 'w'):
                pass
            await message.answer('Сделано✅')
        except Exception as e:
            await message.answer(f'Ошибка: {e}')
    
    elif message.text == '🔥 Получить логи':
        today = datetime.today()
        caption = f"Вот логи за {today.strftime('%d.%m.%Y')}"
        if os.stat('app/logs/bot.log').st_size != 0:
            with open('app/logs/bot.log', 'rb') as file:
                await bot.send_document(DEV, file, caption=caption)
        else:
            await message.answer('Там пусто 📜', reply_markup=kb.godMenu())
            
    elif message.text == '💡 Стать CEO':
        db.changeRoleForCeo(message.from_user.id)
        await message.answer('🚀 Поздравляю, ты теперь CEO! 👑\n🌍 Время вести компанию к вершинам успеха, принимать стратегические решения и вдохновлять свою команду на большие достижения! 💼💡', reply_markup=kb.ceoMenu(lang='ru'))
       
        
    elif message.text == '⚙️ Стать админом':
        db.changeRoleForAdmin(message.from_user.id)
        await message.answer('🚀 Поздравляю, ты теперь админ! 🎉\n🔧 Теперь ты тот, кто держит систему под контролем!\n💻 Ответственность — твоя сила, и ты можешь управлять всем, от настройки до безопасности!\n💥 Время делать всё идеально, управлять процессами и следить за тем, чтобы всё работало как часы! ⏰', reply_markup=kb.adminMenu(lang='ru'))
    
    elif message.text == '🤖 Покажи мне всех, кто здесь!':
        users = db.getUsers()
        txt = '<b>📜 Информация о пользователях</b>\n━━━━━━━━━━━━━━━━━━━\n\n\n'
        for x in users:
            txt += f'🆔 ID: {x[0]}\n📲 Telegram ID: {x[1]}\n👤 Имя: {x[2]}\n📞 Телефон: {x[3]}\n🏷️ Юзернейм: @{x[4]}\n🎭 Роль: {x[5].capitalize()}\n━━━━━━━━━━━━━━━━━━━\n\n'
        await message.reply(txt, parse_mode='HTML')

@dp.message_handler()
async def handler_message(message: Message):
    role = db.getUserRole(message.from_user.id)[0]
    lang = db.getUserLang(message.from_user.id)
    if message.chat.type == 'private':
        if role == 'admin':
            await admin_commands(message, lang)

        elif role == 'ceo':
            await ceo_commands(message, lang)
        
        elif role == 'teacher':
            await teacher_commands(message, lang)
        
        elif role == 'user':
            await user_commands(message, lang)

        elif role == 'god':
            await god_commands(message)
