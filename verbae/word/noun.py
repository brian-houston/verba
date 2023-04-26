from verbae.word.word import Word 
import verbae.word.definitions as definitions

class Noun(Word):
    def __init__(self, data):
        self.stem = data['stem'] 

        if data['declension'] in definitions.declensions:
            self.declension = data['declension']
        else:
            raise ValueError(f'Provided invalid noun declension for "{self.stem}"')

        if data['gender'] in definitions.genders:
            self.gender = data['gender']
        else:
            raise ValueError(f'Provided invalid noun gender for "{self.stem}"')

        self.special = data['special'].split(',')
        self.inflections = {}
        super().__init__('noun', data)

    def __repr__(self):
        return f'Noun: {self.stem}'


