class Question:
    def __init__(self, english_question, latin_question, checker, answers, meaning=None):
        self.english_question = english_question
        self.latin_question = latin_question
        self.checker = checker
        self.answers = answers
        self.meaning = meaning

    def get_question_text(self, mode='english'):
        if mode == 'english':
            return self.english_question
        return self.latin_question

    def get_answers_text(self):
        return '; '.join(self.answers) 

    def get_meaning_text(self):
        if self.meaning:
            return self.meaning
        return 'There is no definition hint for this question.'

    def check_submissions(self, submissions):
        return self.checker(submissions)
