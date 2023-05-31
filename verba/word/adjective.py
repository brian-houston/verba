import itertools
from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.endings as endings
from verba.word.word_key import WordKey as WK

class Adjective(Word):
    def __init__(self, data):
        super().__init__(data)

        self.default_number = 'p' if 'plural' in self.keywords else 's'

        self.subgroup = 'reg'
        if 'ius' in self.keywords:
            self.subgroup = 'ius'

        self.__init_stem_and_declension()
        self.__init_inflections()

    def __init_stem_and_declension(self):
        neuter_part = '' 
        for i in range(4,0,-1):
            if self.data[f'pp{i}']:
                neuter_part = self.data[f'pp{i}']
                break

        max_ending_len = 0
        for d in definitions.adjective_declensions:
            key = WK(d, self.subgroup, 'pos', 'n' , 'nom', self.default_number)
            if key not in endings.endings['adjective']:
                continue

            ending = endings.endings['adjective'][key]
            ending_len = len(ending)
            if neuter_part[-ending_len:] == ending and ending_len > max_ending_len:
                self.declension = d
                self.stem = neuter_part[:-ending_len]
                max_ending_len = ending_len

        # check if one-termination 3rd declension adjective
        # indicated by genitive in last part
        if neuter_part[-2:] == 'is':
            self.declension = '3'
            self.stem = neuter_part[:-2]
            self.keywords.add('one-termination')
        elif max_ending_len == 0:
            Word.raise_error('Could not identify adjective declension', self.data)

    def __init_inflections(self):
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
                Word.raise_error('Could not find ending:', ending_key)
            ending = endings.endings['adjective'][ending_key]
            self.inflections[infl_key] = self.stem + ending

        # set irregular nominate singular 
        # always for 1st/2nd decl. if it is provided
        # only if 3 principal parts provided to 3rd decl.
        if (self.data['pp1'] and self.declension == '1|2' or 
            self.data['pp3'] and self.declension == '3'):
            self.inflections[WK('pos', 'm', 'nom', self.default_number)] = self.data['pp1'] 

        # nominate singular the same for one-termination adj.
        if self.data['pp1'] and 'one-termination' in self.keywords:
            self.inflections[WK('pos', 'f', 'nom', self.default_number)] = self.data['pp1'] 
            self.inflections[WK('pos', 'm', 'nom', self.default_number)] = self.data['pp1'] 
            self.inflections[WK('pos', 'n', 'nom', self.default_number)] = self.data['pp1'] 

    def __repr__(self):
        principal_parts = ''
        return f'Adjective: {principal_parts}'

    def get_key(self):
        return WK(self.declension, self.subgroup)
