from verba.word.word import Word 
from verba.word.word_key import WordKey as WK

# for words that aren't inflected (e.g. prepositions)
class Other(Word):
    def __init__(self, data):
        super().__init__(data)
        for i in range(1,5):
            if data[f'pp{i}']:
                self.inflections[WK('default', str(i))] = data[f'pp{i}']
