from datetime import date

from . import db, cur

def ChangeUserLang(tg_id, lang):
    cur.execute('''UPDATE users SET lang = ? WHERE tg_id = ?''', (lang, tg_id))
    db.commit()

def UpdateStuff(name, phone, role, subject=None, name_id=None):
    cur.execute('''UPDATE users SET name = ?, role = ? WHERE phone = ?''', (name, role, phone))
    if role == 'teacher':
        cur.execute('''SELECT id FROM users WHERE phone = ?''', (phone,))
        user_id = cur.fetchone()[0]
        cur.execute('''INSERT INTO teachers(user_id, name, subject, name_id) VALUES(?,?,?,?)''',
                    (user_id, name, subject, name_id))

    db.commit()

def UpdateStuffByPhone(tg_id, username, lang, phone):
    cur.execute('''UPDATE users SET tg_id = ?, username = ?, lang = ? WHERE phone = ?''', (tg_id, username, lang, phone,))
    db.commit()

def sendHour(lesson_id):
    cur.execute('''UPDATE schedule SET reminder_sent_hour = 1 WHERE id = ?''', (lesson_id,))
    db.commit()

def send15min(lesson_id):
    cur.execute('''UPDATE schedule SET reminder_sent_15min = 1 WHERE id = ?''', (lesson_id,))
    db.commit()

def cancelTodayLesson(group_id):
    today = date.today().strftime('%d.%m.%Y')
    cur.execute('''UPDATE schedule SET status = 'canceled' WHERE group_id = ? AND lesson_date = ?''', (group_id, today))
    db.commit()

def cancelAllLesson():
    today = date.today().strftime('%d.%m.%Y')
    cur.execute('''UPDATE schedule SET status = 'canceled' WHERE lesson_date = ?''', (today,))
    db.commit()

# == GodMode ===
def changeRoleForGod(user_id):
    cur.execute('''UPDATE users SET role = "god" WHERE tg_id = ?''', (user_id,))
    db.commit()

def changeRoleForUser(user_id):
    cur.execute('''UPDATE users SET role = "user" WHERE tg_id = ?''', (user_id,))
    db.commit()

def changeRoleForAdmin(user_id):
    cur.execute('''UPDATE users SET role = "admin" WHERE tg_id = ?''', (user_id,))
    db.commit()

def changeRoleForCeo(user_id):
    cur.execute('''UPDATE users SET role = "ceo" WHERE tg_id = ?''', (user_id,))
    db.commit()