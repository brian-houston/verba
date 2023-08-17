import verba.user_input as user_input

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
        return '; '.join([str(x) for x in self.answers]) 

    def get_meaning_text(self):
        if self.meaning:
            return f'Def: "{self.meaning}"'
        return 'No definition hint'

    def get_pofs_text(self):
        if self.pofs:
            return f'PofS: "{self.pofs}"'
        return 'No part of speech hint'

    def get_key_text(self):
        if self.key:
            return f'Key: "{self.key}"'
        return 'No key hint'

    def check_submissions(self, submissions, ignore_macrons=False):
        answers = self.answers
        if ignore_macrons:
            answers = {user_input.demacronify(x) if isinstance(x, str) else x
                       for x in answers}
        return self.checker(answers, submissions)
