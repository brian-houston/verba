from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.utils as utils
from verba.word.inflection_key import InflectionKey as IK

"""
A noun's principal parts should be given as:
(nominative), (genitive), (gender), -
If the nominative is regular, it can be omitted.
If the noun is plural, the genitive should be plural.

Examples:
    regular:
    -, feminae, f, -

    irregular
    puer, puerī, m, -

    plural
    -, liberōrum, m, -
"""

noun_id_endings = {
    'ae': IK('1', 's', 'reg'),
    'ī': IK('2', 's', 'reg'),
    'is': IK('3', 's', 'reg'),
    'ūs': IK('4', 's', 'reg'),
    'ēī': IK('5', 's', 'reg'),
    'eī': IK('5', 's', 'short-e'),
    'ārum': IK('1', 'p', 'reg'),
    'ōrum': IK('2', 'p', 'reg'),
    'um': IK('3', 'p', 'reg'),
    'ium': IK('3', 'p', 'i-stem'),
    'uum': IK('4', 'p', 'reg'),
    'ērum': IK('5', 'p', 'reg'),
}

class Noun(Word):
    def __init__(self, data):
        self.declension = ''
        self.subgroup = ''
        self.gender = ''
        super().__init__(data)

        if 'invariable' in self.keywords:
            self._set_parts_as_inflections()
            return

        self.is_inflected = True
        if 'irregular' in self.keywords:
            return

        self.gender = self.parts[2] 
        if self.parts[2] not in definitions.genders:
            self._raise_error('Invalid gender', data)

        (key, self.stem) = utils.identify_key_and_stem(self.parts[1], noun_id_endings)

        if not key:
            self._raise_error('Could not identify ending of second principal part', self.data)
            return

        self.declension = key['group']
        self.default_number = key['number']
        self.subgroup = utils.identify_subgroup(key['subgroup'], self.keywords, definitions.noun_subgroups)

        self._init_inflections()

        self.parts[0] = self.inflections[IK('nom', self.default_number)]
        
        self.keywords.add(self.declension)
        self.keywords.add(self.subgroup)
        self.keywords.add(self.gender)
        self.inflections = self.apply_keywords()

    def _init_inflections(self):
        numbers = list(set([self.default_number, 'p'])) 
        keys = utils.make_key_products(definitions.cases, numbers)
        self.inflections |= utils.make_inflections(self.stem, 'noun', keys, self.get_key())

        # set nominative (usually singular) for nouns with irregular forms (e.g puer, 3rd declension)
        if self.parts[0]:
            self.inflections[IK('nom', self.default_number)] = self.parts[0] 

        # nominative and accusative always the same for neuter 
        if self.gender == 'n':
            self.inflections[IK('acc', self.default_number)] = self.inflections[IK('nom', self.default_number)] 

    def get_key(self):
        return IK(self.declension, self.gender, self.subgroup)
