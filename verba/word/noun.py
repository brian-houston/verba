import itertools
from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.endings as endings

class Noun(Word):
    def __init__(self, data):
        super().__init__('noun', data)

        if data['gender'] in definitions.genders:
            self.gender = data['gender']
        else:
            raise ValueError(f'Provided invalid noun gender')

        self.special = data['special'].split(',')
        self.init_stem(data['genitive'])
        self.init_inflections(data)

    def init_stem(self, genitive):
        if '5-long-e' in self.special:
            self.declension = '5'
            self.stem = genitive[:-2]
            return

        number = 'p' if 'plural' in self.special else 's'
        max_ending_len = 0
        for d in ['1', '2']:
            key = (d, self.gender, 'gen', number)
            ending = endings.endings['noun'][key]
            ending_len = len(ending)
            if genitive[-ending_len:] == ending and ending_len > max_ending_len:
                self.declension = d
                self.stem = genitive[:-ending_len]
                max_ending_len = ending_len


    def init_inflections(self, data):
        self.inflections = {}

        key_prefix = (self.declension, self.gender)
        cases = list(definitions.cases)
        numbers = list(definitions.numbers)

        if 'plural' in self.special:
            numbers = ['p']
        elif 'singular' in self.special:
            numbers = ['s']

        products = itertools.product(cases, numbers)
        for key_suffix in products:
            key = key_prefix + key_suffix
            ending = endings.endings['noun'][key]
            self.inflections[key_suffix] = self.stem + ending

        if 'nominative_singular' in data and data['nominative_singular']:
            self.inflections[('nom', 's')] = data['nominative_singular']

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
                'meaning': self.meaning
                }

    def get_inflection_keys(self):
        return self.inflections.keys()
