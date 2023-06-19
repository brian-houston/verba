from verba.word.word import Word 
from verba.word.word_key import WordKey as WK

# for words that aren't inflected (e.g. prepositions)
class Other(Word):
    def __init__(self, data):
        super().__init__(data)
        self._set_parts_as_inflections()
        self.keywords.add('other')
