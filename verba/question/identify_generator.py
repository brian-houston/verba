from verba.question.question_generator import QuestionGenerator
from verba.question.question import Question
import verba.word.definitions as definitions

def order_attributes(attr, part_of_speech):
    return definitions.attribute_order[part_of_speech].index(attr)

def order_values(val, part_of_speech):
    attr = definitions.value_to_attribute[val]
    return order_attributes(attr, part_of_speech)

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
                      if attr in definitions.attribute_order[self.part_of_speech]]

        if not attributes:
            raise ValueError(f'No valid attributes provided for part of speech "{part_of_speech}"')

        # sort attributes in the defined order
        attributes.sort(key = lambda x: order_attributes(x, self.part_of_speech))

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
        n = 0
        while (n < 1000):
            n += 1

            word = QuestionGenerator.choice(words)
            possible_inflection_keys = set(self.inflection_keys).intersection(word.get_inflection_keys())
            possible_inflection_keys = list(possible_inflection_keys)

            if not possible_inflection_keys:
                continue

            selected_key = QuestionGenerator.choice(possible_inflection_keys)

            inflection = word.get_inflection(selected_key)
            eng_question = self.eng_format.format(word = inflection['word'])
            lat_question = self.lat_format
            answers = set()
            for key in inflection['keys']:
                answer = []
                for attr in self.attributes:
                    if attr in inflection:
                        answer.append(inflection[attr])
                    else:
                        index = definitions.inflections_key_index[self.part_of_speech][attr]
                        answer.append(key[index])
                answers.add(tuple(answer))

            checker = self.make_checker(answers)
            yield Question(eng_question, lat_question, checker, answers)
        

    def make_checker(self, answers):
        def checker(submissions):
            nonlocal answers
            for submission in submissions:
                pieces = submission.split()
                submission = [val for val in pieces if val in definitions.value_to_attribute]

                # wrong number of attributes given 
                if len(pieces) != len(self.attributes):
                    return 'wrong'

                submission.sort(key = lambda x: order_values(x, self.part_of_speech))
                submission = tuple(submission)

                if submission not in answers:
                    return 'wrong'
                answers.remove(submission)

            if answers:
                return 'partial'
            return 'correct'
                

        return checker

