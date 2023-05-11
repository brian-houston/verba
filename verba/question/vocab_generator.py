from verba.question.question_generator import QuestionGenerator
from verba.question.question import Question

class VocabGenerator(QuestionGenerator):
    eng_format = 'What is the definition of "{word}"?'
    lat_format = ''

    def __init__(self, inflection_keys, filters=None):
        self.inflection_keys = inflection_keys
        self.filters = filters

    def generate(self, words):
        fails = 0
        while True:
            if fails > 10:
                return StopIteration()

            word = QuestionGenerator.choice(words)
            possible_inflection_keys = set(self.inflection_keys).intersection(word.get_inflection_keys())
            possible_inflection_keys = list(possible_inflection_keys)

            if not possible_inflection_keys:
                fails += 1
                continue
            else: 
                fails = 0

            selected_key = QuestionGenerator.choice(possible_inflection_keys)
            inflection = word.get_inflection(selected_key)

            eng_question = self.eng_format.format(word=inflection)
            lat_question = self.lat_format
            answers = set()
            answers.add(word.get_meaning())

            checker = self.make_checker(answers)
            yield Question(eng_question, lat_question, checker, answers)
        

    def make_checker(self, answers):
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

