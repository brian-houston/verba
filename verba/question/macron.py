from verba.question.question import Question
import verba.question.utils as question_utils
import verba.utils as verba_utils

def macron_question_generator(words, inflection_keys):
    for word, key in question_utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)

        answers = set()
        answers.add(verba_utils.lower_latin(inflection))

        checker = make_checker()
        yield Question(f'Macron: "{verba_utils.demacronify(inflection)}"', checker, answers, 
                       meaning=word.meaning, pofs=word.part_of_speech, key=str(key))

def make_checker():
    def checker(answers, submissions):
        if len(submissions) != 1:
            return 'wrong'

        if verba_utils.lower_latin(submissions[0]) in answers:
            return 'correct'
        
        return 'wrong'

    return checker
