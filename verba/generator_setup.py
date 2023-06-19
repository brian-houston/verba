from verba.console import console
from verba.question.vocab import vocab_question_generator 
from verba.question.macron import macron_question_generator 
from verba.question.identify import identify_question_generator 

setting_ask_user_text = {
        'level': "Up to what chapter's level of grammer do you want to practice? ",
        'chapters': "What chapters' vocabulary lists do you want to practice? ",
        'attributes': "What attributes do you want to identify? ",
        'match': "What parts of speech do you want to match? ",
        'filters': "How do you want to filter the words selected? ",
        }

question_types_setting_list = {
        'identify': ['level', 'chapters', 'attributes', 'filters'],
        'compose': ['level', 'chapters', 'filters'],
        'vocab': ['level', 'chapters', 'filters'],
        'macron': ['level', 'chapters', 'filters'], 
        'matching': ['level', 'chapters', 'match', 'filters'], 
        }

def translate_setting_input(setting, input):
    if setting == 'level':
        try:
            return max(1, int(input))
        except:
            return None
    if setting == 'chapters':
        try:
            chapters = set()
            for s in input.replace(',', ' ').split():
                digits = s.split('-')
                if len(digits) == 1:
                    chapters.add(int(digits[0]))
                elif len(digits) == 2:
                    start = int(digits[0])
                    end = int(digits[1]) + 1
                    chapters.update(range(start, end))
            return chapters if chapters else None
        except:
            return None
    if setting == 'filters':
        try:
            input = input.strip()
            filters = input.split(',')
            filters = [s.split() for s in filters]
            return filters
        except:
            return None
    if setting == 'attributes':
        try:
            attr_table = {}
            for s in input.split(','):
                s = s.strip()
                parts = s.split(':')
                part_of_speech = parts[0]
                attributes = parts[1].split()
                if not attributes:
                    return None
                attr_table[part_of_speech] = attributes 
            return attr_table
        except:
            return None

    return None 

def select_generator_settings():
    question_type = ''
    while True:
        question_type = input('What type of question do you want to practice? ')
        if question_type in question_types_setting_list:
            break
        console.print("What you entered is not valid, so let's try again.")

    settings = {}
    settings['type'] = question_type
    for setting_name in question_types_setting_list[question_type]:
        while True:
            value = translate_setting_input(setting_name, input(setting_ask_user_text[setting_name]))
            if value != None:
                settings[setting_name] = value
                break
            console.print("What you entered is not valid, so let's try again.")

    return settings

def does_word_match_filters(word, filters):
    for f in filters:
        if word.match_keywords(f):
            return True
    return False

def create_generator(settings, words, keys):
    if 'level' in settings:
        new_keys = {}
        for pofs, list_v in keys.items():
            new_keys[pofs] = [key for chapter, key in list_v if chapter <= settings['level']]
        keys = new_keys
    if 'chapters' in settings:
        words = [w for w in words if w.chapter in settings['chapters']]
    if 'filters' in settings:
        words = [w for w in words if does_word_match_filters(w, settings['filters'])]

    if settings['type'] == 'macron':
        return macron_question_generator(words, keys)
    if settings['type'] == 'vocab':
        return vocab_question_generator(words, keys)
    if settings['type'] == 'identify':
        return identify_question_generator(words, keys, settings['attributes'])
