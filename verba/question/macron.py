from verba.question.question import Question
from verba.input import demacronify
import verba.question.utils as utils

eng_format = 'Place macrons on the word "{word}" {key}.'
lat_format = ''

def macron_question_generator(words, inflection_keys, filters=None):
    for word, key in utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)

        eng_question = eng_format.format(word=demacronify(inflection), key=key)
        lat_question = lat_format
        answers = set()
        answers.add(inflection)

        checker = make_checker(answers)
        yield Question(eng_question, lat_question, checker, answers, meaning=word.get_meaning())

def make_checker(answers):
    def checker(submissions):
        if len(submissions) != 1:
            return 'wrong'

        if submissions[0] in answers:
            return 'correct'
        
        return 'wrong'

    return checker
