from verba.question.question import Question
import verba.word.definitions as definitions
from verba.word.word_key import WordKey as WK
import verba.question.utils as utils

eng_format = 'What {verb} the {attributes} of the word "{word}"?'
lat_format = ''

def identify_question_generator(words, inflection_keys, attributes):
    n_attr = len(attributes) 
    eng_verb = 'are' if n_attr > 1 else 'is'
    eng_attributes = {}
    for pofs, attr_list in attributes.items():
        eng_attributes[pofs] = attr_list[0]
        if n_attr > 1:
            eng_attributes[pofs] = ', '.join(attr_list[-1])
            comma = '' if n_attr == 2 else ','
            eng_attributes[pofs] = f'{eng_attributes[pofs]}{comma} and {attr_list[-1]}'

    for word, key in utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)
        pofs = word.get_pofs()
        eng_question = eng_format.format(verb=eng_verb, attributes=eng_attributes[pofs], word = inflection)
        lat_question = lat_format
        answers = set()

        for key in word.get_keys_for_inflection(inflection):
            answers.add(key.union(word.get_key()).filter(attributes[pofs]))

        checker = make_checker(answers)
        yield Question(eng_question, lat_question, checker, answers, meaning=word.get_meaning())
    
def make_checker(answers):
    def checker(submissions):
        nonlocal answers
        for submission in submissions:
            key = WK(*submission.split())

            if key not in answers:
                return 'wrong'
            answers.remove(key)

        if answers:
            return 'partial'
        return 'correct'
            
    return checker

