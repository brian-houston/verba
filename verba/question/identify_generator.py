from verba.question.question_generator import QuestionGenerator
from verba.question.question import Question
import verba.word.definitions as definitions
from verba.word.word_key import WordKey as WK

class IdentifyGenerator(QuestionGenerator):
    eng_format = 'What {verb} the {attributes} of the word "{word}"?'
    lat_format = ''

    def __init__(self, part_of_speech, attributes, inflection_keys, filters=None):
        if part_of_speech in definitions.parts_of_speech:
            self.part_of_speech = part_of_speech
        else:
            raise ValueError(f'Provided invalid part of speech "{part_of_speech}"')

        # filter out attributes which do not apply to this part of speech
        attributes = [attr for attr in attributes 
                      if attr in definitions.key_order]

        if not attributes:
            raise ValueError(f'No valid attributes provided for part of speech "{part_of_speech}"')

        self.attributes = attributes
        self.inflection_keys = inflection_keys
        self.filters = filters

        n_attr = len(attributes) 
        eng_verb = 'are' if n_attr > 1 else 'is'
        eng_attributes = attributes[0]
        if n_attr > 1:
            eng_attributes = ', '.join(attributes[:-1])
            comma = '' if n_attr == 2 else ','
            eng_attributes = f'{eng_attributes}{comma} and {attributes[-1]}'

        self.eng_format = self.eng_format.format(verb=eng_verb, attributes=eng_attributes, word='{word}')

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
            eng_question = self.eng_format.format(word = inflection)
            lat_question = self.lat_format
            answers = set()

            for key in word.get_keys_for_inflection(inflection):
                answers.add(key.union(word.get_key()).filter(self.attributes))

            checker = self.make_checker(answers)
            yield Question(eng_question, lat_question, checker, answers, meaning=word.get_meaning())
        
    def make_checker(self, answers):
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

