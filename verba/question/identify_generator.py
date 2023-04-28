from verba.question.question_generator import QuestionGenerator

class IdentifyGenerator(QuestionGenerator):
    english_question_format = 'What is {attributes} of the word "{word}"'
    latin_question_format = 'Quod est {attributes} verbī "{word}"'
    def __init__(self, part_of_speech, filters, id_attributes):
        self.id_attributes = id_attributes
        super().__init__(part_of_speech, filters)

    def generate(self, number, words):
        questions = []
        # filter words

