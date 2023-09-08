from verba.question.question import Question
import verba.question.utils as question_utils
import verba.utils as verba_utils

def compose_question_generator(words, inflection_keys):
    for word, key1, key2 in question_utils.double_inflection_generator(words, inflection_keys):
        question_inflection = word.get_inflection(key1)
        answer_inflection = word.get_inflection(key2)

        answers = {answer_inflection}

        checker = make_checker()
        yield Question(f'Compose: "{str(key2)}" from "{question_inflection}"', checker, answers, 
                       meaning=word.meaning, pofs=word.part_of_speech, key=str(key1))

def make_checker():
    def checker(answers, submissions):
        if len(submissions) != 1:
            return 'wrong'

        if verba_utils.lower_latin(submissions[0]) in answers:
            return 'correct'
        
        return 'wrong'

    return checker
