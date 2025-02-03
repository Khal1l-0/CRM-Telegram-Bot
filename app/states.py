from aiogram.dispatcher.filters.state import State, StatesGroup

class AddStuff(StatesGroup):
    name = State()
    phone = State()
    role = State()
    subject = State()
   
class AddGroup(StatesGroup):
    name = State()
    date = State()
    time = State()
    subject = State()
    teacher = State()
    lang = State()
    group_mode = State()

class GenCer(StatesGroup):
    name = State()

class AddSubject(StatesGroup):
    name = State()
    max_lessons = State()
 
class AddUsertoGroup(StatesGroup):
    name = State()
    get_doc = State()

class CancelLesson(StatesGroup):
    group_id = State()
    reason = State()
    
class CancelAllLessons(StatesGroup):
    reason = State()

class News(StatesGroup):
    text = State()

class Application(StatesGroup):
    text = State()

class SetLanguage(StatesGroup):
    lang = State()