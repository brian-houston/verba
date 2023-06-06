import itertools
from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.endings as endings
import verba.word.utils as utils
from verba.word.word_key import WordKey as WK

present_stem_keys = [
        WK('ind', 'pres', 'act'),
        WK('ind', 'pres', 'pass'),
        WK('ind', 'imperf', 'act'),
        WK('ind', 'imperf', 'pass'),
        WK('ind', 'fut', 'act'),
        WK('ind', 'fut', 'pass'),
        WK('subj', 'pres', 'act'),
        WK('subj', 'pres', 'pass'),
        WK('subj', 'imperf', 'act'),
        WK('subj', 'imperf', 'pass'),
        ]

perfect_stem_keys = [
        WK('ind', 'perf', 'act'),
        WK('ind', 'plup', 'act'),
        WK('ind', 'futp', 'act'),
        WK('subj', 'perf', 'act'),
        WK('subj', 'plup', 'act'),
        ]

supine_stem_keys = [
        WK('ind', 'perf', 'pass'),
        WK('ind', 'plup', 'pass'),
        WK('ind', 'futp', 'pass'),
        WK('subj', 'perf', 'pass'),
        WK('subj', 'plup', 'pass'),
        ]

class Verb(Word):
    def __init__(self, data):
        super().__init__(data)

        self.is_inflected = True
        self.subgroup = 'reg'
        self.present_stem = ''
        self.perfect_stem = ''
        self.supine_stem = ''

        if 'irregular' in self.keywords:
            return

        self._init_present_stem_and_conjugation()

        if 'deponent' in self.keywords or 'semi-deponent' in self.keywords:
            self.supine_stem = self.parts[2][:-6] # remove 'us sum'
        else:
            self.perfect_stem = self.parts[2][:-1] # remove 'ī'

        if not self.supine_stem:
            self.supine_stem = self.parts[3][:-2] # remove 'us'

        self.keywords.add(self.subgroup)
        self.keywords.add(self.conjugation)

        self._init_present_inflections()

        if 'deponent' in self.keywords:
            self.inflections = {WK('act').union(k): v for k, v in self.inflections.items()}

    def _init_present_stem_and_conjugation(self):
        if not self.parts[1]:
            self.conjugation = 'na'
            return

        partial_keys = [
                WK('pres', 'act'),
                WK('pres', 'pass')
                ]

        (key, self.present_stem) = utils.identify_key_and_stem(
                self.parts[1], partial_keys, 'infinitive', definitions.verb_conjugations)

        if not key:
            Word._raise_error('Could not identify verb conjugation', self.data)
        
        self.conjugation = key['group']

        if self.conjugation == '3' and (self.parts[0][-2:] == 'iō' or self.parts[0][-3:] == 'ior'):
            self.subgroup = 'i-stem'

        if key['voice'] == 'pass':
            self.keywords.add('deponent')
        elif self.parts[2][-6:] == 'us sum':
            self.keywords.add('semi-deponent')

    def _init_present_inflections(self):
        if not self.present_stem:
            return

        person_number_keys = utils.make_key_products(definitions.persons, definitions.numbers) 
        keys = []
        for key1 in present_stem_keys: 
            if 'deponent' in self.keywords and key1['voice'] == 'act':
                continue
            if 'no-passive' in self.keywords and key1['voice'] == 'pass':
                continue
            keys += [key1.union(key2) for key2 in person_number_keys]

        self.inflections |= utils.make_inflections(self.present_stem, 'verb', keys, self.get_key())

    def get_key(self):
        return WK(self.conjugation, self.subgroup)
