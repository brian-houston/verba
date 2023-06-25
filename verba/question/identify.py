from verba.question.question import Question
from verba.word.word_key import WordKey as WK
import verba.question.utils as utils

def identify_question_generator(words, inflection_keys, attributes):
    # remove words with attributes to identify
    words = [w for w in words if w.part_of_speech in attributes]

    for word, key in utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)
        pofs = word.part_of_speech
        answers = set()

        for key in word.get_keys_for_inflection(inflection):
            answers.add(key.union(word.get_key()).filter(attributes[pofs]))

        checker = make_checker(answers)
        yield Question(f'Identify: "{inflection}"', checker, [str(x) for x in answers], 
                       meaning=word.meaning, pofs=word.part_of_speech, key='No cheating!')
    
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

