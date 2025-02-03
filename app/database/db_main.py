from datetime import datetime, timedelta, date
import sqlite3 as sq

db = sq.connect('database.db')
cur = db.cursor()

async def database_start():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        tg_id NUMERIC UNIQUE, 
        name TEXT, 
        phone NUMERIC, 
        username TEXT, 
        role TEXT DEFAULT user NOT NULL,
        lang TEXT DEFAULT ru NOT NULL
        );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS teachers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        subject TEXT,
        name_id TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS groups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date DATE,
        days TEXT NOT NULL,
        time TIME,
        subject TEXT NOT NULL,
        teacher TEXT,
        lang TEXT,
        group_mode TEXT,
        link_to_tg TEXT,
        tg_group_id TEXT,
        max_lessons INTEGER NOT NULL
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        id_name TEXT UNIQUE,
        max_lessons INTEGER NOT NULL
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            lesson_date TEXT NOT NULL,
            lesson_time TEXT NOT NULL,
            reminder_sent_hour INTEGER DEFAULT 0,
            reminder_sent_15min INTEGER DEFAULT 0,
            teacher_id TEXT NOT NULL,
            status TEXT DEFAULT 'scheduled',
            FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
        )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            text TEXT
        )""")
    cur.execute("""CREATE INDEX IF NOT EXISTS idx_schedule_date_time ON schedule(lesson_date, lesson_time)""")
    cur.execute("""CREATE INDEX IF NOT EXISTS idx_schedule_status ON schedule(status)""")
    db.commit()




