from verba.question.question import Question
import verba.question.utils as utils

def vocab_question_generator(words, inflection_keys, filters=None):
    for word, key in utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)

        answers = set()
        answers.add(word.meaning)

        checker = make_checker(answers)
        yield Question(f'Vocab: "{inflection}"', '', checker, answers, meaning="No Cheating!")

def make_checker(answers):
    first_input = True
    def checker(submissions):
        nonlocal first_input
        if first_input:
            first_input = False
            return 'answer'

        if 'c' in submissions:
            return 'correct'

        return 'wrong'

    return checker
