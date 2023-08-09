from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.utils as utils
from verba.word.inflection_key import InflectionKey as IK

"""
An adjective's principle parts should be given as:
(ind pres act 1st sing), (pres inf), (ind perf act 1st sing OR perf inf), (supine)
The 1st principal part is only required for i-stems.
If a verb doesn't pres/perf/supine stem, leave that part blank.

Examples:
    regular
    -, amāre, amavī, amatum

    i-stem
    facio, facere, fecisse, factum

    deponent
    -, loquī, -, locūtum
"""

present_stem_keys = [
        IK('ind', 'pres', 'act'),
        IK('ind', 'pres', 'pass'),
        IK('ind', 'imperf', 'act'),
        IK('ind', 'imperf', 'pass'),
        IK('ind', 'fut', 'act'),
        IK('ind', 'fut', 'pass'),
        IK('subj', 'pres', 'act'),
        IK('subj', 'pres', 'pass'),
        IK('subj', 'imperf', 'act'),
        IK('subj', 'imperf', 'pass'),
        ]

perfect_stem_keys = [
        IK('ind', 'perf', 'act'),
        IK('ind', 'plup', 'act'),
        IK('ind', 'futp', 'act'),
        IK('subj', 'perf', 'act'),
        IK('subj', 'plup', 'act'),
        ]

supine_stem_keys = [
        IK('ind', 'perf', 'pass'),
        IK('ind', 'plup', 'pass'),
        IK('ind', 'futp', 'pass'),
        IK('subj', 'perf', 'pass'),
        IK('subj', 'plup', 'pass'),
        ]

class Verb(Word):
    def __init__(self, data):
        super().__init__(data)

        self.conjugation = ''
        self.subgroup = ''
        self.present_stem = ''
        self.perfect_stem = ''
        self.supine_stem = ''

        if 'invariable' in self.keywords:
            self._set_parts_as_inflections()
            return

        self.is_inflected = True

        if 'irregular' in self.keywords:
            return

        self._init_present_stem_and_conjugation()

        # perfect stem can be given as 1st singular or infinitive
        if self.parts[2][-1:] == 'ī':
            self.perfect_stem = self.parts[2][:-1]
        elif self.parts[2][-4:] == 'isse':
            self.perfect_stem = self.parts[2][:-4]

        self.supine_stem = self.parts[3][:-2] # remove 'um'

        self.subgroup = 'reg'
        if self.conjugation == '3' and (self.parts[0][-2:] == 'iō' or self.parts[0][-3:] == 'ior'):
            self.subgroup = 'i-stem'

        if self.parts[1][-1:] == 'ī':
            self.keywords.add('deponent')
        elif not self.perfect_stem and self.supine_stem:
            self.keywords.add('semi-deponent')

        self.keywords.add(self.subgroup)
        self.keywords.add(self.conjugation)

        self._init_supine_inflections()

        if 'semi-deponent' in self.keywords:
            self.inflections = {IK('act').union(k): v for k, v in self.inflections.items()}

        self._init_perfect_inflections()
        self._init_present_inflections()

        if 'deponent' in self.keywords:
            self.inflections = {IK('act').union(k): v for k, v in self.inflections.items()}

        self.keywords.add(self.conjugation)
        self.keywords.add(self.subgroup)
        self.inflections = self.apply_keywords()

    def _init_present_stem_and_conjugation(self):
        if not self.parts[1]:
            self.conjugation = 'na'
            return

        partial_keys = [
                IK('pres', 'act'),
                IK('pres', 'pass')
                ]

        (key, self.present_stem) = utils.identify_key_and_stem(
                self.parts[1], partial_keys, 'infinitive', definitions.verb_conjugations)

        if not key:
            self._raise_error('Could not identify verb conjugation', self.data)
            return
        
        self.conjugation = key['group']

    def _init_present_inflections(self):
        if not self.present_stem:
            return

        person_number_keys = utils.make_key_products(definitions.persons, definitions.numbers) 
        keys = []
        for key1 in present_stem_keys: 
            if 'deponent' in self.keywords and key1['voice'] == 'act':
                continue
            keys += [key1.union(key2) for key2 in person_number_keys]

        self.inflections |= utils.make_inflections(self.present_stem, 'verb', keys, self.get_key())

    def _init_perfect_inflections(self):
        if not self.perfect_stem:
            return

        person_number_keys = utils.make_key_products(definitions.persons, definitions.numbers) 
        keys = []
        for key1 in perfect_stem_keys: 
            if 'deponent' in self.keywords and key1['voice'] == 'act':
                continue
            keys += [key1.union(key2) for key2 in person_number_keys]

        self.inflections |= utils.make_inflections(self.perfect_stem, 'verb', keys, self.get_key())

    def _init_supine_inflections(self):
        if not self.supine_stem:
            return

        person_number_keys = utils.make_key_products(definitions.persons, definitions.numbers) 
        keys = []
        for key1 in supine_stem_keys: 
            if 'deponent' in self.keywords and key1['voice'] == 'act':
                continue
            keys += [key1.union(key2) for key2 in person_number_keys]

        self.inflections |= utils.make_inflections(self.supine_stem, 'verb', keys, self.get_key())

    def get_key(self):
        return IK(self.conjugation, self.subgroup)
