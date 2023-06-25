from verba.console import console
from verba.question.vocab import vocab_question_generator 
from verba.question.macron import macron_question_generator 
from verba.question.identify import identify_question_generator 

setting_ask_user_text = {
        'level': "Level: ",
        'chapters': "Chapters: ",
        'attributes': "Attributes: ",
        'match': "Match: ",
        'filters': "Filters: ",
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
            return int(input) 
        except:
            return None
    if setting == 'chapters':
        try:
            chapters = set()
            for s in input.replace(',', ' ').split():
                parts = s.split('-')
                if len(parts) == 1:
                    chapters.add(parts[0])
                elif len(parts) == 2:
                    start = int(parts[0])
                    end = int(parts[1]) + 1
                    chapters.update([str(x) for x in range(start, end)])
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
        question_type = input('Question Type: ')
        if question_type in question_types_setting_list:
            break
        console.print('Invalid')

    settings = {}
    settings['type'] = question_type
    for setting_name in question_types_setting_list[question_type]:
        while True:
            value = translate_setting_input(setting_name, input(setting_ask_user_text[setting_name]))
            if value != None:
                settings[setting_name] = value
                break
            console.print('Invalid')

    return settings

def does_word_match_filters(word, filters):
    for f in filters:
        if word.match_keywords(f):
            return True
    return False

def create_generator(settings, words, keys):
    if 'level' in settings:
        new_keys = {}
        if settings['level'] > 0:
            for pofs, list_v in keys.items():
                new_keys[pofs] = [key for chapter, key in list_v if chapter <= settings['level']]
        keys = new_keys
    if 'chapters' in settings:
        if '0' not in settings['chapters']:
            words = [w for w in words if w.chapter in settings['chapters']]
    if 'filters' in settings:
        words = [w for w in words if does_word_match_filters(w, settings['filters'])]

    if settings['type'] == 'macron':
        return macron_question_generator(words, keys)
    if settings['type'] == 'vocab':
        return vocab_question_generator(words, keys)
    if settings['type'] == 'identify':
        return identify_question_generator(words, keys, settings['attributes'])
