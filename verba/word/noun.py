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

        if 'i-stem' in self.special:
            self.category = 'i-stem'
        elif 'short-e' in self.special:
            self.category = 'short-e'
        else:
            self.category = 'reg'

        self.__init_stem_and_declension(data)
        self.__init_inflections(data)

    def __init_stem_and_declension(self, data):
        genitive = data['genitive']
        number = 'p' if 'plural' in self.special else 's'
        max_ending_len = 0
        for d in definitions.noun_declensions:
            key = (d, self.gender, self.category, 'gen', number)
            if key not in endings.endings['noun']:
                continue

            ending = endings.endings['noun'][key]
            ending_len = len(ending)
            if genitive[-ending_len:] == ending and ending_len > max_ending_len:
                self.declension = d
                self.stem = genitive[:-ending_len]
                max_ending_len = ending_len

        if max_ending_len == 0:
            raise ValueError(f'Failed to identify declension for the noun whose genitive is {genitive}')


    def __init_inflections(self, data):
        self.inflections = {}

        key_prefix = (self.declension, self.gender, self.category)
        cases = list(definitions.cases)
        numbers = list(definitions.numbers)

        if 'plural' in self.special:
            numbers = ['p']
        elif 'singular' in self.special:
            numbers = ['s']

        products = itertools.product(cases, numbers)
        for key_suffix in products:
            key = key_prefix + key_suffix
            if key not in endings.endings['noun']:
                raise ValueError(f"Failed to find ending for {data['genitive']} in {key}")
            ending = endings.endings['noun'][key]
            self.inflections[key_suffix] = self.stem + ending

        if 'nominative_singular' in data and data['nominative_singular']:
            self.inflections[('nom', 's')] = data['nominative_singular']

    def __repr__(self):
        principal_parts = ''
        if 'plural' in self.special:
            principal_parts = f"{self.inflections[('nom', 'p')]}, {self.inflections[('gen', 'p')]}, {self.gender}"
        else:
            principal_parts = f"{self.inflections[('nom', 's')]}, {self.inflections[('gen', 's')]}, {self.gender}"
        return f'Noun: {principal_parts}'

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
