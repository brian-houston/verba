import itertools
from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.endings as endings
from verba.word.word_key import WordKey as WK

"""
An adjective's principle parts should be given as:
(masc nom), (fem nom), (neut nom), (genitive).
For regular adjectives only the feminine nominative is required.
If the masculine or neuter doesn't follow the regular pattern (e.g pulcher, aliud), it must be provided.
For one-termination adjectives, the genitive must be provided in the last slot.
The nominative of one-termination adjectives can just be provided in the first slot and not repeated three times.
The keyword 'ius' should be given to words like 'nullus' which have 'īus' in the genitive

Examples:
    1/2, regular 
    -, bona, -, - 

    1/2, irregular masc nom
    pulcher, pulchra, -, - 

    1/2, irregular neut nom
    -, alia, aliud, -

    regular
    -, brevis, -, -

    3, irregular masc nom
    acer, acris, -, -

    3, one-termination
    pars, -, -, partis
"""

class Adjective(Word):
    def __init__(self, data):
        super().__init__(data)

        self.is_inflected = True
        self.default_number = 'p' if 'plural' in self.keywords else 's'

        self.subgroup = 'reg'
        if 'ius' in self.keywords:
            self.subgroup = 'ius'

        self._init_stem_and_declension()
        self._init_inflections()

        self.parts[0] = self.inflections[WK('pos', 'm', 'nom', self.default_number)]
        self.parts[1] = self.inflections[WK('pos', 'f', 'nom', self.default_number)]
        self.parts[2] = self.inflections[WK('pos', 'n', 'nom', self.default_number)]

    def _init_stem_and_declension(self):
        # check if one-termination 3rd declension adjective
        # indicated by genitive in last part
        if self.parts[3][-2:] == 'is':
            self.declension = '3'
            self.stem = self.parts[3][:-2]
            self.keywords.add('one-termination')
            return

        feminine_part = self.parts[1] 
        max_ending_len = 0
        for d in definitions.adjective_declensions:
            key = WK(d, self.subgroup, 'pos', 'f' , 'nom', self.default_number)
            if key not in endings.endings['adjective']:
                continue

            ending = endings.endings['adjective'][key]
            ending_len = len(ending)
            if feminine_part[-ending_len:] == ending and ending_len > max_ending_len:
                self.declension = d
                self.stem = feminine_part[:-ending_len]
                max_ending_len = ending_len

        if max_ending_len == 0:
            Word._raise_error('Could not identify adjective declension', self.data)

    def _init_inflections(self):
        self_key = self.get_key() 
         
        cases = definitions.cases
        genders = definitions.genders
        degrees = ['pos']
        numbers = ['s', 'p'] 

        if 'plural' in self.keywords:
            numbers = ['p']
        elif 'singular' in self.keywords:
            numbers = ['s']

        products = itertools.product(cases, degrees, numbers, genders)
        for prod in products:
            infl_key = WK(*prod)
            ending_key = self_key.union(infl_key)
            if ending_key not in endings.endings['adjective']:
                Word._raise_error('Could not find ending:', ending_key)
            ending = endings.endings['adjective'][ending_key]
            self.inflections[infl_key] = self.stem + ending

        # set irregular nominate singulars
        if self.parts[0]:
            self.inflections[WK('pos', 'm', 'nom', self.default_number)] = self.parts[0] 
        if self.parts[2]:
            self.inflections[WK('pos', 'n', 'nom', self.default_number)] = self.parts[2] 
            self.inflections[WK('pos', 'n', 'acc', self.default_number)] = self.parts[2] 

        # for one-termination adjectives
        # set nominatives to first principle part
        if 'one-termination' in self.keywords and self.parts[0]:
            self.inflections[WK('pos', 'm', 'nom', self.default_number)] = self.parts[0] 
            self.inflections[WK('pos', 'f', 'nom', self.default_number)] = self.parts[0] 
            self.inflections[WK('pos', 'n', 'nom', self.default_number)] = self.parts[0] 
            self.inflections[WK('pos', 'n', 'acc', self.default_number)] = self.parts[0] 

    def get_key(self):
        return WK(self.declension, self.subgroup)
