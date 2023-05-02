from verba.question.question_generator import QuestionGenerator
from verba.question.question import Question

class IdentifyGenerator(QuestionGenerator):
    eng_format = 'What {verb} the {attributes} of the word "{word}"?'
    lat_format = ''
    def __init__(self, part_of_speech, filters, attributes):
        self.attributes = attributes
        eng_verb = 'are' if len(attributes) > 1 else 'is'
        eng_attributes = ', '.join(attributes)
        self.eng_format = self.eng_format.format(verb=eng_verb, attributes=eng_attributes, word='{word}')
        super().__init__(part_of_speech, filters)

    def generate(self, count, words):
        questions = []
        # filter words

        for i in range(count):
            word = words[i].get_inflection('nom-s')['word']
            eng_question = self.eng_format.format(word = word)
            lat_question = self.lat_format
            answers = [[words[i].gender]]
            questions.append(Question(eng_question, lat_question, answers))
        
        return questions


