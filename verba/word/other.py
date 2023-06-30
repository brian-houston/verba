from verba.word.word import Word 

# for words that aren't inflected (e.g. prepositions)
class Other(Word):
    def __init__(self, data):
        super().__init__(data)
        self.keywords.add('other')
        if 'inflected' in self.keywords:
            return
        self._set_parts_as_inflections()
