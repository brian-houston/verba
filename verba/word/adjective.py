from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.utils as utils
from verba.word.inflection_key import InflectionKey as IK

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
        self.declension = ''
        self.subgroup = ''
        super().__init__(data)

        if 'invariable' in self.keywords:
            self._set_parts_as_inflections()
            return

        self.is_inflected = True
        if 'irregular' in self.keywords:
            return

        self.subgroup = utils.identify_subgroup(self.keywords, definitions.adjective_subgroups)

        partial_keys = [
                IK('pos', 'f', self.subgroup, 's', 'nom'),
                IK('pos', 'f', self.subgroup, 'p', 'nom'),
                ]

        (key, self.stem) = utils.identify_key_and_stem(
                self.parts[1], partial_keys, 'adjective', definitions.adjective_declensions)

        if self.parts[3][-2:] == 'is':
            self.declension = '3'
            self.stem = self.parts[3][:-2]
            self.default_number = 's'
            self.keywords.add('one-termination')
        elif not key:
            self._raise_error('Could not identify adjective declension', self.data)
        else:
            self.declension = key['group']
            self.default_number = key['number']

        self._init_inflections()

        self.parts[0] = self.inflections[IK('pos', 'm', 'nom', self.default_number)]
        self.parts[1] = self.inflections[IK('pos', 'f', 'nom', self.default_number)]
        self.parts[2] = self.inflections[IK('pos', 'n', 'nom', self.default_number)]

        self.keywords.add(self.declension)
        self.keywords.add(self.subgroup)
        self.inflections = self.apply_keywords()

    def _init_inflections(self):
        numbers = list(set([self.default_number, 'p'])) 
        keys = utils.make_key_products(definitions.degrees, definitions.genders, definitions.cases, numbers)
        self.inflections |= utils.make_inflections(self.stem, 'adjective', keys, self.get_key())

        # set irregular nominate singulars
        if self.parts[0]:
            self.inflections[IK('pos', 'm', 'nom', self.default_number)] = self.parts[0] 
        if self.parts[2]:
            self.inflections[IK('pos', 'n', 'nom', self.default_number)] = self.parts[2] 
            self.inflections[IK('pos', 'n', 'acc', self.default_number)] = self.parts[2] 

        # for one-termination adjectives
        # set nominatives to first principle part
        if 'one-termination' in self.keywords and self.parts[0]:
            self.inflections[IK('pos', 'm', 'nom', self.default_number)] = self.parts[0] 
            self.inflections[IK('pos', 'f', 'nom', self.default_number)] = self.parts[0] 
            self.inflections[IK('pos', 'n', 'nom', self.default_number)] = self.parts[0] 
            self.inflections[IK('pos', 'n', 'acc', self.default_number)] = self.parts[0] 

    def get_key(self):
        return IK(self.declension, self.subgroup)
