from verbae.word.word import Word 
from verbae.word.word_type import WordType

class Noun(Word):
    def __init__(self, data):
        super().__init__(WordType.NOUN)
