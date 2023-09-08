from verba.question.question import Question
import verba.question.utils as question_utils

def vocab_question_generator(words, inflection_keys):
    for word, key in question_utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)

        answers = set()
        answers.add(word.meaning)

        checker = make_checker()
        yield Question(f'Vocab: "{inflection}"', checker, answers, 
                       meaning="No cheating!", pofs=word.part_of_speech, key=str(key))

def make_checker():
    first_input = True
    def checker(answers, submissions):
        nonlocal first_input
        if first_input:
            first_input = False
            return 'answer'

        if 'c' in submissions:
            return 'correct'

        return 'wrong'

    return checker
