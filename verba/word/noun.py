from verba.word.word import Word 
import verba.word.definitions as definitions
import verba.word.utils as utils
from verba.word.inflection_key import InflectionKey as IK

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

        self.subgroup = utils.identify_subgroup(self.keywords, definitions.noun_subgroups)
        partial_keys = [
                IK(self.gender, self.subgroup, 's', 'gen'),
                IK(self.gender, self.subgroup, 'p', 'gen'),
                ]

        (key, self.stem) = utils.identify_key_and_stem(
                self.parts[1], partial_keys, 'noun', definitions.noun_declensions)

        if not key:
            self._raise_error('Could not identify noun declension', self.data)
            return

        self.declension = key['group']
        self.default_number = key['number']

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
