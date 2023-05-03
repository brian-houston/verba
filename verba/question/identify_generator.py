from verba.question.question_generator import QuestionGenerator
from verba.question.question import Question
import verba.word.definitions as definitions

class IdentifyGenerator(QuestionGenerator):
    eng_format = 'What {verb} the {attributes} of the word "{word}"?'
    lat_format = ''

    def __init__(self, part_of_speech, filters, attributes):
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
        attributes.sort(key = lambda attr: definitions.attribute_order[self.part_of_speech].index(attr))

        self.attributes = attributes

        n_attr = len(attributes) 
        eng_verb = 'are' if n_attr > 1 else 'is'
        eng_attributes = attributes[0]
        if n_attr > 1:
            eng_attributes = ', '.join(attributes[:-1])
            comma = '' if n_attr == 2 else ','
            eng_attributes = f'{eng_attributes}{comma} and {attributes[-1]}'

        self.eng_format = self.eng_format.format(verb=eng_verb, attributes=eng_attributes, word='{word}')
        super().__init__(filters)

    def generate(self, count, words):
        questions = []
        # filter words

        for i in range(count):
            inflection = words[i].get_inflection(('nom', 'p'))
            eng_question = self.eng_format.format(word = inflection['word'])
            lat_question = self.lat_format
            answers = set()
            for key in inflection['keys']:
                answer = []
                for attr in self.attributes:
                    loc = definitions.inflections_lookup[self.part_of_speech][attr]
                    if loc == 'base':
                        answer.append(inflection[attr])
                    else:
                        answer.append(key[loc])
                answers.add(tuple(answer))

            print(answers)

            questions.append(Question(eng_question, lat_question, answers))
        
        return questions


