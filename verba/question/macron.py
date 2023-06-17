from verba.question.question import Question
import verba.user_input as user_input
import verba.question.utils as utils

def macron_question_generator(words, inflection_keys, filters=None):
    for word, key in utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)

        answers = set()
        answers.add(user_input.lower_latin(inflection))

        checker = make_checker(answers)
        yield Question(f'Macron: "{user_input.demacronify(inflection)}"', '', checker, answers, meaning=word.meaning)

def make_checker(answers):
    def checker(submissions):
        if len(submissions) != 1:
            return 'wrong'

        if user_input.lower_latin(submissions[0]) in answers:
            return 'correct'
        
        return 'wrong'

    return checker
