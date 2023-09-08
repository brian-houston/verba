from verba.question.question import Question
from verba.word.inflection_key import InflectionKey as IK
import verba.question.utils as question_utils

def identify_question_generator(words, inflection_keys, pofs, attributes):
    # remove words with attributes to identify
    words = [w for w in words if w.part_of_speech == pofs]

    for word, key in question_utils.inflection_generator(words, inflection_keys):
        inflection = word.get_inflection(key)
        answers = set()

        all_keys = set(word.get_keys_for_inflection(inflection))
        if pofs in inflection_keys:
            all_keys = all_keys.intersection(inflection_keys[pofs]) 

        for key in all_keys:
            answers.add(key.union(word.get_key()).filter(attributes))

        checker = make_checker()
        yield Question(f'Identify: "{inflection}"', checker, answers, 
                       meaning=word.meaning, pofs=pofs, key='No cheating!')
    
def make_checker():
    def checker(answers, submissions):
        submissions = {IK(*x.split()) for x in submissions}

        if answers == submissions:
            return 'correct'
        return 'wrong'
            
    return checker

