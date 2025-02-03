from datetime import timedelta, datetime
from . import db, cur

def AddUser(tg_id, name, phone, username, lang):
    cur.execute('''INSERT INTO users(tg_id, name, phone, username, lang) VALUES(?, ?, ?, ?, ?)''', (tg_id, name, phone, username, lang))
    db.commit()

def AddApplication(name, phone, text):
    cur.execute('''INSERT INTO applications(name, phone, text) VALUES(?, ?, ?)''', (name, phone, text ))
    db.commit()

def AddSchedule(group_id, date, days, time, max_lessons, teacher_id):
    # Генерация расписания
    days_of_week = [int(day) for day in days.split('-')]
    start_date = datetime.strptime(date, '%d.%m.%Y')
    schedule_data = []
    current_date = start_date
    lesson_number = 1

    while lesson_number <= max_lessons:
        if current_date.weekday() in days_of_week:
            schedule_data.append((group_id, current_date.strftime('%d.%m.%Y'), time, teacher_id))
            lesson_number += 1
        current_date += timedelta(days=1)
    # Сохранение расписания в таблицу
    cur.executemany('''INSERT INTO schedule (group_id, lesson_date, lesson_time, reminder_sent_hour, reminder_sent_15min, teacher_id, status) VALUES (?, ?, ?, ?, ?, ?, ?)''', [(x[0], x[1], x[2], 0, 0, x[3], 'active') for x in schedule_data])
    db.commit()


def AddStuff(name, phone, role, subject=None, name_id=None):
    cur.execute('''INSERT INTO users(name, phone, role) VALUES(?,?,?)''', (name, phone, role))
    user_id = cur.lastrowid
    if role == 'teacher':
        cur.execute('''INSERT INTO teachers(user_id, name, subject, name_id) VALUES(?,?,?,?)''', (user_id, name, subject, name_id))

    db.commit()

def AddGroup(name, date, days, time, subject, teacher, lang, group_mode, link, tg_group_id, max_lessons):
    cur.execute('''INSERT INTO groups(name, date, days, time, subject, teacher, lang, group_mode, link_to_tg, tg_group_id, max_lessons) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (name, date, days, time, subject, teacher, lang, group_mode, link, tg_group_id, max_lessons))
    group_id = cur.lastrowid
    db.commit()
    AddSchedule(group_id, date,days,time, max_lessons, teacher)

def AddSubject(name, id_name, max_lessons):
    cur.execute('''INSERT INTO subjects(name, id_name, max_lessons) VALUES (?, ?, ?)''', (name, id_name, max_lessons))
    db.commit()
