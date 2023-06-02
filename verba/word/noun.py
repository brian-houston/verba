import itertools
from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.endings as endings
from verba.word.word_key import WordKey as WK

class Noun(Word):
    def __init__(self, data):
        super().__init__(data)
        if 'indeclinable' in self.keywords:
            self._set_parts_as_inflections()
            self.part_of_speech = 'noun-indeclinable'
            return

        if self.parts[2] in definitions.genders:
            self.gender = self.parts[2] 
        else:
            Word._raise_error('Bad Gender', data)

        if 'i-stem' in self.keywords:
            self.subgroup = 'i-stem'
        elif 'short-e' in self.keywords:
            self.subgroup = 'short-e'
        else:
            self.subgroup = 'reg'

        # the number used in noun's principal parts 
        self.default_number = 'p' if 'plural' in self.keywords else 's'

        self._init_stem_and_declension()
        self._init_inflections()

    def _init_stem_and_declension(self):
        # match genitive to longest ending
        # needs to be longest because ī and ēī are both genitive endings
        genitive = self.parts[1] 
        max_ending_len = 0
        for d in definitions.noun_declensions:
            key = WK(d, self.gender, self.subgroup, 'gen', self.default_number)
            if key not in endings.endings['noun']:
                continue

            ending = endings.endings['noun'][key]
            ending_len = len(ending)
            if genitive[-ending_len:] == ending and ending_len > max_ending_len:
                self.declension = d
                self.stem = genitive[:-ending_len]
                max_ending_len = ending_len

        if max_ending_len == 0:
            Word._raise_error('Could not identify noun declension', self.data)

    def _init_inflections(self):
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
                Word._raise_error('Could not find ending', ending_key)
            ending = endings.endings['noun'][ending_key]
            self.inflections[infl_key] = self.stem + ending

        # set nominative (usually singular) for nouns with irregular forms (e.g puer, 3rd declension)
        if self.parts[0]:
            self.inflections[WK('nom', self.default_number)] = self.parts[0] 

        # nominative and accusative always the same for neuter 
        if self.gender == 'n':
            self.inflections[WK('acc', self.default_number)] = self.inflections[WK('nom', self.default_number)] 

    def __repr__(self):
        principal_parts = (f"{self.inflections[WK('nom', self.default_number)]}, "
                           f"{self.inflections[WK('gen', self.default_number)]}, "
                           f"{self.gender}")
        return f'Noun: {principal_parts}'

    def get_key(self):
        return WK(self.declension, self.gender, self.subgroup)
