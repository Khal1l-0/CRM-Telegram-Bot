from datetime import datetime, date
from . import db, cur

# === Уроки ===
def getNearLesson():
    now = datetime.now()
    # Получаем ближайшие занятия
    cur.execute('''SELECT id, group_id, lesson_time, lesson_date, reminder_sent_hour, reminder_sent_15min, status
    FROM schedule 
    WHERE lesson_date >= ? 
    ORDER BY lesson_date, lesson_time
    ''', (now.strftime('%d.%m.%Y'),))
    lessons = cur.fetchall()
    return lessons

def getSubjects():
    cur.execute('''SELECT * FROM subjects''')
    subjects = cur.fetchall()
    subjectsList = [(subject[1], subject[2]) for subject in subjects]
    return subjectsList

def getMaxLessson(subject):
    cur.execute('''SELECT max_lessons FROM subjects WHERE id_name = ?''', (subject,))
    max_lessons = cur.fetchone()[0]
    return max_lessons

def getSubjectById(subject):
    cur.execute('''SELECT name FROM subjects WHERE id_name = ?''', (subject,))
    name = cur.fetchone()[0]
    return name

# === Админ ===
def getTodayLesson():
    today = date.today().strftime('%d.%m.%Y')
    cur.execute('''SELECT group_id, lesson_date, lesson_time, teacher_id FROM schedule WHERE lesson_date = ? AND status = 'active' ORDER BY lesson_date, lesson_time''',(today,))
    lessons = cur.fetchall()
    return lessons

# === Учитель ===
def getTeachersGroups(tg_id):
    cur.execute('''SELECT id FROM users WHERE tg_id = ?''', (tg_id,))
    id = cur.fetchone()[0]
    cur.execute('''SELECT name_id FROM teachers WHERE user_id = ?''', (id,))
    teacher_id = cur.fetchone()[0]
    cur.execute('''SELECT * FROM groups WHERE teacher = ?''', (teacher_id,))
    groups = cur.fetchall()
    groups = [x[1] for x in groups]
    return groups

def getTodayTeachersLesson(user_id):
    today = date.today().strftime('%d.%m.%Y')
    cur.execute('''SELECT id FROM users WHERE tg_id = ?''', (user_id,))
    user_id = cur.fetchone()[0]
    cur.execute('''SELECT name_id FROM teachers WHERE user_id = ?''', (user_id,))
    teacher = cur.fetchone()[0]
    cur.execute(
        '''SELECT group_id, lesson_date, lesson_time FROM schedule WHERE lesson_date = ? AND status = 'active' AND teacher_id = ? ORDER BY lesson_date, lesson_time''',
        (today, teacher))
    lessons = cur.fetchall()
    return lessons

def getTeacherById(teacher):
    cur.execute('''SELECT user_id FROM teachers WHERE name_id = ?''', (teacher,))
    user_id = cur.fetchone()[0]
    cur.execute('''SELECT tg_id FROM users WHERE id = ?''', (user_id,))
    userTeach = cur.fetchone()[0]
    return userTeach

def getTeacherNameById(name_id):
    cur.execute('''SELECT name FROM teachers WHERE name_id = ?''', (name_id,))
    teacherName = cur.fetchone()[0]
    return teacherName

def getTeachersBySubject(subject=None):
    cur.execute('''SELECT * FROM teachers WHERE subject = ?''', (subject,))
    teachers = cur.fetchall()
    teachersList = [(x[2], x[4]) for x in teachers]
    return teachersList

def getNameById(name_id):
    cur.execute('''SELECT name FROM teachers WHERE name_id = ?''', (name_id,))
    name = cur.fetchone()[0]
    return name

# === Пользователи ===
def getUserLang(tg_id):
    cur.execute('''SELECT lang FROM users WHERE tg_id = ?''', (tg_id, ))
    lang = cur.fetchone()[0]
    return lang

def getAllUserTgId():
    cur.execute('''SELECT tg_id FROM users WHERE role = 'user' ''')
    ids = cur.fetchall()
    return ids

def getUserPhoneById(user_id):
    cur.execute('''SELECT phone from users WHERE tg_id = ?''', (user_id,))
    phone = cur.fetchone()[0]
    return phone

def getUsers():
    cur.execute('''SELECT * FROM users WHERE tg_id IS NOT NULL''')
    users = cur.fetchall()
    return users

# === Группы ===
def getGroupsName():
    cur.execute('''SELECT name FROM groups''')
    dataGroup = cur.fetchall()
    dataGroup = [x[0] for x in dataGroup]
    return dataGroup

def getGroup(i):
    cur.execute('''SELECT * FROM groups WHERE name = ?''', (i,))
    group = cur.fetchall()
    return group

def getGroupByName(group_name):
    cur.execute('''SELECT date, time, subject, teacher, lang, group_mode, link_to_tg FROM groups WHERE name = ?''',
                (group_name,))
    group = cur.fetchall()
    return group

def getGroupById(group_id):
    cur.execute('''SELECT name, teacher, subject FROM groups WHERE id = ?''', (group_id,))
    info = cur.fetchall()
    return info

def getGroupLangById(group_id):
    cur.execute('''SELECT lang FROM groups WHERE id = ?''', (group_id,))
    lang = cur.fetchone()[0]
    return lang

def getGroupIdByName(group_name):
    cur.execute('''SELECT id FROM groups WHERE name = ?''', (group_name,))
    id = cur.fetchone()[0]
    return id

def getTgId(group_id):
    cur.execute('''SELECT tg_group_id FROM groups WHERE id = ?''', (group_id,))
    tg_group_id = cur.fetchone()[0]
    return tg_group_id

def getGroupByTgId(tg_id):
    cur.execute('''SELECT * FROM groups WHERE tg_group_id = ?''', (tg_id, ))
    group = cur.fetchall()
    return group

def getAllGroupTgId():
    cur.execute('''SELECT tg_group_id FROM groups''')
    ids = cur.fetchall()
    return ids

# === ? ===
def getTeacherByTg(chat_id):
    cur.execute('''SELECT teacher FROM groups WHERE tg_grop_id = ?''', (chat_id,))
    teacher = cur.fetchone()[0]
    cur.execute('''SELECT user_id FROM teachers WHERE tg_grop_id = ?''', (teacher,))
    user_id = cur.fetchone()[0]
    cur.execute('''SELECT tg_id FROM users WHERE id = ?''', (user_id,))
    userTeach = cur.fetchone()[0]
    return userTeach

# ======

# === Заявки ===
def getApplications():
    cur.execute('''SELECT * FROM applications''')
    data = cur.fetchall()
    return data


# === Функция поиска ===
def findUserByPhone(phone):
    cur.execute('''SELECT * FROM users WHERE phone = ?''', (phone,))
    user = cur.fetchone()
    return user

# === Проверка ===
def getUserRole(user_id):
    cur.execute('''SELECT role FROM users WHERE tg_id = ?''', (user_id,))
    user = cur.fetchone()
    return user