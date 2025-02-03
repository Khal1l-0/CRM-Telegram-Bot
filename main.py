import asyncio


# === Локальные модули ===
from app import bot, dp, app, cron, lesson_scheduler
from app import database as db
from app import handlers
    
# === Точка входа ===
async def on_startup():
    await db.database_start()
    print('База данных создана...')
    
    asyncio.create_task(app.start())
    print('Бот зашел в аккаунт...')

    cron.start()
    print('Cron запущен...')

    asyncio.create_task(lesson_scheduler())
    print('Планировщик запущен...')
    print('Бот успешно запущен...')

    
async def main():
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)  
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())