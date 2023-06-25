class Question:
    def __init__(self, question_text, checker, answers, meaning=None, pofs=None, key=None):
        self.question_text = question_text
        self.checker = checker
        self.answers = answers
        self.meaning = meaning
        self.pofs = pofs
        self.key = key

    def get_question_text(self):
        return self.question_text

    def get_answers_text(self):
        return '; '.join(self.answers) 

    def get_meaning_text(self):
        if self.meaning:
            return f'Meaning: "{self.meaning}"'
        return 'No definition hint'

    def get_pofs_text(self):
        if self.pofs:
            return f'Part of speech: "{self.pofs}"'
        return 'No part of speech hint'

    def get_key_text(self):
        if self.key:
            return f'Key: "{self.key}"'
        return 'No key hint'

    def check_submissions(self, submissions):
        return self.checker(submissions)
