class Question:
    def __init__(self, english_question, latin_question, checker, answers):
        self.english_question = english_question
        self.latin_question = latin_question
        self.checker = checker
        self.answers = answers

    def print_english(self):
        print(self.english_question)

    def print_latin(self):
        print(self.latin_question)

    def check_submissions(self, submissions):
        return self.checker(submissions)
