from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


# === Локальные модули ===
from app import bot
from app.bot import DEV
from app import database as db

cron = AsyncIOScheduler()

# Отправка лог файла разработчику, очистка мусора в 23:59:59
async def cron_task():
    file_path = 'app/logs/bot.log'

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    db.deletApplications()
    db.deleteOldSchedule()

    caption = f"Вот логи за {yesterday.strftime('%d.%m.%Y')}\nТакже удалены все логи и расписание"

    with open(file_path, 'rb') as file:
        await bot.send_document(DEV, file, caption=caption)

    with open(file_path, 'w'):
        pass

# Задача с CronTrigger, выполнение каждый день в 23:59:59
cron.add_job(cron_task, CronTrigger(hour=23, minute=59, second=59))
