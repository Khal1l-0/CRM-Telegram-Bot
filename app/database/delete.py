from datetime import datetime

from . import db, cur


def deleteOldSchedule():
    now = datetime.now()
    # Получаем ближайшие занятия
    cur.execute('''DELETE FROM schedule WHERE lesson_date < ?''', (now.strftime('%d.%m.%Y'),))
    db.commit()


def deletApplications():
    cur.execute('''DELETE FROM applications''')
    db.commit()