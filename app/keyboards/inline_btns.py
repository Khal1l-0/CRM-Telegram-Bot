from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

from googletrans import Translator

from app import database as db
from app.dictionary import translate

def getMyGroups(tg_id):
    btn = [InlineKeyboardButton(text, callback_data=f'group-{text}') for text in db.getTeachersGroups(tg_id)]
    keyboard = InlineKeyboardMarkup(row_width=4).add(*btn)

    return keyboard
    
def getTeachersBySubject(subject):
    teachersList = db.getTeachersBySubject(subject)
    btn = [InlineKeyboardButton(name, callback_data=name_id) for (name, name_id) in teachersList]
    keyboard = InlineKeyboardMarkup(row_width=1).add(*btn)
    
    return keyboard

def subjectsList():
    btn = [InlineKeyboardButton(name, callback_data=f'subject-{id_name}') for (name, id_name) in db.getSubjects()]
    keyboard = InlineKeyboardMarkup(row_width=2).add(*btn)
    
    return keyboard

def setUserLang():
    keyboard = InlineKeyboardMarkup(row_width=3)
    ru = InlineKeyboardButton('Ру 🇷🇺', callback_data='lang-ru')
    en = InlineKeyboardButton('En 🇺🇸', callback_data='lang-en')
    uz = InlineKeyboardButton('Uz 🇺🇿', callback_data='lang-uz')
    keyboard.add(ru, en, uz)
    return keyboard


#Выбор языка сертификата
def certMenu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    cert_ru = InlineKeyboardButton('Рус 🇷🇺', callback_data='cert-ru')
    cert_uz = InlineKeyboardButton('Узб 🇺🇿', callback_data='cert-uz')
    keyboard.add(cert_ru, cert_uz)
    return keyboard

def roleMenu(lang):
    keyboard = InlineKeyboardMarkup(row_width=1)
    admin = InlineKeyboardButton(f"{translate(f'{lang}', 'role_admin')}", callback_data='admin')
    teacher = InlineKeyboardButton(f"{translate(f'{lang}', 'role_teacher')}", callback_data='teacher')
    keyboard.add(admin, teacher)
    return keyboard


# Календарь
def getCalendar(year: int, month: int, lang):
    keyboard = InlineKeyboardMarkup(row_width=7)

    # Навигация и заголовок с месяцем и годом
    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    prev_year = year if month > 1 else year - 1
    next_year = year if month < 12 else year + 1

    prev_button = InlineKeyboardButton('<<', callback_data=f'calendar:{prev_year}:{prev_month}:nav')
    next_button = InlineKeyboardButton('>>', callback_data=f'calendar:{next_year}:{next_month}:nav')

    month_name = datetime(year, month, 1).strftime('%B')
    # if lang != 'en':
    #     translator = Translator()
    #     month_name = translator.translate(month_name, src='en', dest=lang).text.capitalize()

    header_button = InlineKeyboardButton(f"{month_name} {year}", callback_data='ignore')
    keyboard.row(prev_button, header_button, next_button)

    # Заголовок с днями недели
    days_of_week = {
        'ru': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
        'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'uz': ["Du", "Se", "Chor", "Pay", "Jum", "Sha", "Yak"],

    }
    keyboard.row(*[InlineKeyboardButton(day, callback_data='ignore') for day in days_of_week[f'{lang}']])

    # Генерация календаря
    first_day = datetime(year, month, 1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Вычисление отступов для первого дня
    start_offset = (first_day.weekday() + 0) % 7  # Сдвиг для начала недели с понедельника
    days = []

    # Добавление пустых кнопок до начала месяца
    days.extend([InlineKeyboardButton(' ', callback_data='ignore')] * start_offset)

    # Добавление кнопок для каждого дня месяца
    for day in range(1, last_day.day + 1):
        days.append(InlineKeyboardButton(str(day), callback_data=f'calendar:{year}:{month}:{day}'))

    # Добавление пустых кнопок до завершения строки
    while len(days) % 7 != 0:
        days.append(InlineKeyboardButton(' ', callback_data='ignore'))

    # Формирование строк для InlineKeyboardMarkup
    for i in range(0, len(days), 7):
        keyboard.row(*days[i:i + 7])

    return keyboard

# === Группы ===
def groupsMenu(page: int):
    groups_per_page = 8
    start_idx = page * groups_per_page
    end_idx = start_idx + groups_per_page
    btn = [InlineKeyboardButton(text, callback_data=f'group-{text}') for text in db.getGroupsName()[start_idx:end_idx]]
    keyboard = InlineKeyboardMarkup(row_width=4).add(*btn)
    
    
    keyboard.add(InlineKeyboardButton('➕', callback_data='add-group'))
    navBts = []
    if start_idx > 0:
        navBts.append(InlineKeyboardButton('⬅', callback_data=f"prev_{page - 1}"))
    if end_idx < len(db.getGroupsName()):
        navBts.append(InlineKeyboardButton("➡", callback_data=f"next_{page + 1}"))

    # Добавляем кнопки навигации к основным кнопкам
    if navBts:
        keyboard.add(*navBts)
        
        
    return keyboard

def todayGroups():
    keyboard = InlineKeyboardMarkup(row_width=3)
    lessons = db.getTodayLesson()
    btn = [InlineKeyboardButton(db.getGroupById(group[0])[0][0], callback_data=f'cancel-{db.getGroupById(group[0])[0][0]}') for group in lessons]
    keyboard.add(*btn)
    return keyboard

def AddMemberGroup(page: int):
    groups_per_page = 8    
    start_idx = page * groups_per_page
    end_idx = start_idx + groups_per_page
    btn = [InlineKeyboardButton(text, callback_data=f'member-{text}') for text in db.getGroupsName()[start_idx:end_idx]]
    keyboard = InlineKeyboardMarkup(row_width=4).add(*btn)
    
    
    navBts = []
    if start_idx > 0:
        navBts.append(InlineKeyboardButton('⬅', callback_data=f"mprev_{page - 1}"))
    if end_idx < len(db.getGroupsName()):
        navBts.append(InlineKeyboardButton("➡", callback_data=f"tnext_{page + 1}"))

    # Добавляем кнопки навигации к основным кнопкам
    if navBts:
        keyboard.add(*navBts)
        
        
    return keyboard
    
def groupMode(lang):
    role = 'admin'
    keyboard = InlineKeyboardMarkup(row_width=2)
    offline = InlineKeyboardButton(f"{translate(f'{lang}', 'offline', f'{role}')}", callback_data='offline')
    online = InlineKeyboardButton(f"{translate(f'{lang}', 'online', f'{role}')}", callback_data='online')
    keyboard.add(offline, online)
    return keyboard

def langList():
    keyboard = InlineKeyboardMarkup(row_width=2)
    group_ru = InlineKeyboardButton('Рус 🇷🇺', callback_data='group-ru')
    group_uz = InlineKeyboardButton('Uzb 🇺🇿', callback_data='group-uz')
    keyboard.add(group_ru, group_uz)
    return keyboard

def confirmGroup(lang):
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton(f"{translate(f'{lang}', 'confirm', 'admin')}", callback_data='confirm-group')
    btn_2 = InlineKeyboardButton(f"{translate(f'{lang}', 'cancel_group', 'admin')}", callback_data='cancel-group')
    keyboard.add(btn_2, btn)
    return keyboard

def backGroup(lang):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton(f"{translate(f'{lang}', 'back', 'admin') }", callback_data='back-to-group')
    keyboard.add(back)
    return keyboard
    