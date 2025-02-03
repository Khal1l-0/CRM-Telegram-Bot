from .en import *
from .ru import *
from .uz import *

translations = {
    'ru': ru.dictionary,
    'en': en.dictionary,
    'uz': uz.dictionary,
}

def translate(lang, text, role=None):
    dictionary_lang = translations.get(lang, translations['ru'])
    if role is None:
        return dictionary_lang.get(text, text)
    else:
        return dictionary_lang[role].get(text, text)

