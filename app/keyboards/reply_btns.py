from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app import translate

def send_contact(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton(f"{translate(f'{lang}', 'share_contact')}", request_contact=True)
    keyboard.add(btn)
    return keyboard

#Менюшки для сотрудников 
def ceoMenu(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    role = 'ceo'
    btn_1 = KeyboardButton(translate(f'{lang}', 'add_employee', f'{role}'))
    btn_2 = KeyboardButton(translate(f'{lang}', 'add_subject', f'{role}'))

    keyboard.add(btn_1)
    keyboard.add(btn_2)
    return keyboard

def adminMenu(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    role = 'admin'
    btn_1 = KeyboardButton(translate(f'{lang}', 'groups', f'{role}'))
    btn_2 = KeyboardButton(translate(f'{lang}', 'today_lessons', f'{role}'))
    btn_3 = KeyboardButton(translate(f'{lang}', 'news', f'{role}'))
    btn_4 = KeyboardButton(translate(f'{lang}', 'add_member', f'{role}'))
    btn_5 = KeyboardButton(translate(f'{lang}', 'cancel_lesson', f'{role}'))
    btn_6 = KeyboardButton(translate(f'{lang}', 'applications', f'{role}'))
    btn_7 = KeyboardButton(translate(f'{lang}', 'cancel_all_lessons', f'{role}'))
    btn_8 = KeyboardButton(translate(f'{lang}', 'gen_cer', f'{role}'))
    # deleteCert = KeyboardButton('Удалить мусор🗑')

    keyboard.add(btn_8)
    keyboard.add(btn_1, btn_2)
    keyboard.add(btn_3)
    keyboard.add(btn_4,btn_5)
    keyboard.add(btn_6)
    keyboard.add(btn_7)
    
    return keyboard

def godMenu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    stat = KeyboardButton('📊 Статистика бота 🔍')
    delAllGroups = KeyboardButton('🔥 Время для глобальной чистки! 💣') # TODO: убери пока не пошло по пизде
    getLogs = KeyboardButton('🔥 Получить логи')
    beCeo = KeyboardButton('💡 Стать CEO')
    beAdmin = KeyboardButton('⚙️ Стать админом')
    getUsersInDetail = KeyboardButton('🤖 Покажи мне всех, кто здесь!')
    
    keyboard.add(getUsersInDetail)
    keyboard.add(stat)
    keyboard.add(beCeo,beAdmin)
    keyboard.add(getLogs)
    keyboard.add(delAllGroups)
    
    return keyboard

def teacherMenu(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    role = 'teacher'
    btn_1 = KeyboardButton(translate(f'{lang}', 'my_groups', f'{role}'))
    btn_2 = KeyboardButton(translate(f'{lang}', 'today_lessons', 'admin'))

    keyboard.add(btn_1,btn_2)

    return keyboard

def userMenu(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    role = 'user'
    btn_1 = KeyboardButton(translate(f'{lang}', 'info'))
    btn_2 = KeyboardButton(translate(f'{lang}', 'application', f'{role}'))
    keyboard.add(btn_1)
    keyboard.add(btn_2)
    
    return keyboard



def groupTime():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    time_1 = KeyboardButton('10:30')
    time_2 = KeyboardButton('12:00')
    time_3 = KeyboardButton('13:30')
    time_4 = KeyboardButton('16:00')
    
    keyboard.add(time_1, time_2)
    keyboard.add(time_3, time_4)
    
    return keyboard



