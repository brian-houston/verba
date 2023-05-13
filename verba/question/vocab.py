from verba.question.question import Question
import verba.question.utils as utils

eng_format = 'What is the definition of "{word}"?'
lat_format = ''

def vocab_question_generator(words, inflection_keys, filters=None):
    for word, key in utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)

        eng_question = eng_format.format(word=inflection)
        lat_question = lat_format
        answers = set()
        answers.add(word.get_meaning())

        checker = make_checker(answers)
        yield Question(eng_question, lat_question, checker, answers, meaning="No Cheating!")

def make_checker(answers):
    first_input = True
    def checker(submissions):
        nonlocal first_input
        if first_input:
            print(list(answers)[0])
            first_input = False
            return 'continue'

        if 'c' in answers:
            return 'correct'

        return 'wrong'

    return checker
