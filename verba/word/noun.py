import itertools
from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.endings as endings

class Noun(Word):
    def __init__(self, data):
        super().__init__('noun', data)

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

        key_prefix = f'{self.declension}-{self.gender}'
        cases = list(definitions.cases)
        numbers = list(definitions.numbers)

        if 'plural' in self.special:
            numbers = ['p']

        if 'singular' in self.special:
            numbers = ['s']

        products = itertools.product(cases, numbers)
        for p in products:
            key_suffix = '-'.join(list(p)) 
            key = f'{key_prefix}-{key_suffix}'
            ending = endings.endings["noun"][key]
            self.inflections[key_suffix] = self.stem + ending

        if 'nominative_singular' in data and data['nominative_singular']:
            self.inflections['nom-s'] = data['nominative_singular']

    def __repr__(self):
        return f'Noun: {self.stem}'

    def has_inflection(self, key):
        return key in self.inflections

    def get_inflection(self, key):
        word = self.inflections[key]
        keys = [k for (k, v) in self.inflections.items() if v == word]
        return {
                'word': word,
                'keys': keys,
                'gender': self.gender,
                }
