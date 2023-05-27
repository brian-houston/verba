import itertools
from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.endings as endings
from verba.word.word_key import WordKey as WK

class Noun(Word):
    def __init__(self, data):
        super().__init__(data)

        nominative = data['pp1']
        genitive = data['pp2']
        gender = data['pp3']

        if gender in definitions.genders:
            self.gender = gender 
        else:
            raise ValueError(f'Provided invalid noun gender for noun whose genitive is {genitive}')

        if 'i-stem' in self.keywords:
            self.category = 'i-stem'
        elif 'short-e' in self.keywords:
            self.category = 'short-e'
        else:
            self.category = 'reg'

        # the number used in noun's principal parts 
        self.default_number = 'p' if 'plural' in self.keywords else 's'

        self.__init_stem_and_declension(genitive)
        self.__init_inflections(nominative)

    def __init_stem_and_declension(self, genitive):
        # match genitive to longest ending
        # needs to be longest because ī and ēī are both genitive endings
        max_ending_len = 0
        for d in definitions.noun_declensions:
            key = WK(d, self.gender, self.category, 'gen', self.default_number)
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

    def __init_inflections(self, nominative):
        self_key = self.get_key() 
         
        cases = definitions.cases
        numbers = ['s', 'p'] 

        if 'plural' in self.keywords:
            numbers = ['p']
        elif 'singular' in self.keywords:
            numbers = ['s']

        products = itertools.product(cases, numbers)
        for prod in products:
            infl_key = WK(*prod)
            ending_key = self_key.union(infl_key)
            if ending_key not in endings.endings['noun']:
                raise ValueError(f"Failed to find ending for {data['genitive']} in {ending_key}")
            ending = endings.endings['noun'][ending_key]
            self.inflections[infl_key] = self.stem + ending

        # set nominative (usually singular) for nouns with irregular forms (e.g puer, 3rd declension)
        if nominative:
            self.inflections[WK('nom', self.default_number)] = nominative 

        # set nominative and accusative always the same for neuter nouns
        if self.gender == 'n':
            self.inflections[WK('acc', self.default_number)] = self.inflections[WK('nom', self.default_number)] 

    def __repr__(self):
        principal_parts = (f"{self.inflections[WK('nom', self.default_number)]}, "
                           f"{self.inflections[WK('gen', self.default_number)]}, "
                           f"{self.gender}")
        return f'Noun: {principal_parts}'

    def get_key(self):
        return WK(self.declension, self.gender, self.category)
