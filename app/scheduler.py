import asyncio
from datetime import datetime, timedelta

# === Локальные модули===
from app import bot, translate
from app import database as db

async def lesson_scheduler():
    while True:
        now = datetime.now()
        lessons = db.getNearLesson()
        tasks = []
        for lesson in lessons:
            id, group_id, lesson_time, lesson_date, reminder_sent_hour, reminder_sent_15min, status = lesson
            lesson_datetime = datetime.strptime(f"{lesson_date} {lesson_time}", '%d.%m.%Y %H:%M')
            if status == 'active':
                if reminder_sent_hour == 0 and now + timedelta(minutes=60) >= lesson_datetime > now:
                    (tasks.append(asyncio.create_task(bot.send_message(db.getTgId(group_id), f"{translate(f'{db.getGroupLangById(group_id)}', 'remind_hour').format(lesson_time=lesson_time)}"))))
                    db.sendHour(id)
                if reminder_sent_15min == 0 and now + timedelta(minutes=15) >= lesson_datetime > now:
                    tasks.append(asyncio.create_task(bot.send_message(db.getTgId(group_id), f"{translate(f'{db.getGroupLangById(group_id)}', 'remind_15min').format(lesson_time=lesson_time)}")))
                    db.send15min(id)

        if tasks:
            await asyncio.gather(*tasks)

        await asyncio.sleep(60)  # Проверяем каждую минуту
