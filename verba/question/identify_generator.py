from verba.question.question_generator import QuestionGenerator
from verba.question.question import Question
import verba.word.definitions as definitions

class IdentifyGenerator(QuestionGenerator):
    eng_format = 'What {verb} the {attributes} of the word "{word}"?'
    lat_format = ''
    def __init__(self, part_of_speech, filters, attributes):
        self.attributes = attributes

        n_attr = len(attributes) 
        eng_verb = 'are' if n_attr > 1 else 'is'
        eng_attributes = attributes[0]
        if n_attr > 1:
            eng_attributes = ', '.join(attributes[:-1])
            comma = '' if n_attr == 2 else ','
            eng_attributes = f'{eng_attributes}{comma} and {attributes[-1]}'

        self.eng_format = self.eng_format.format(verb=eng_verb, attributes=eng_attributes, word='{word}')
        super().__init__(part_of_speech, filters)

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


