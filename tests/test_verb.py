import unittest
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK

class TestVerb(unittest.TestCase):
    def test_conjugation(self):
        n = word_utils.make_word('verb', ['', 'putāre', '', ''])
        self.assertTrue(n.conjugation == '1')
        n = word_utils.make_word('verb', ['', 'lūcēre', '', ''])
        self.assertTrue(n.conjugation == '2')
        n = word_utils.make_word('verb', ['', 'bibere', '', ''])
        self.assertTrue(n.conjugation == '3')
        n = word_utils.make_word('verb', ['', 'venīre', '', ''])
        self.assertTrue(n.conjugation == '4')

    def test_i_stem(self):
        n = word_utils.make_word('verb', ['bibō', 'bibere', '', ''])
        self.assertTrue(n.subgroup == 'reg')
        n = word_utils.make_word('verb', ['faciō', 'facere', '', ''])
        self.assertTrue(n.subgroup == 'i-stem')

    def test_stems(self):
        n = word_utils.make_word('verb', ['', 'amāre', 'amavī', 'amatus'])
        self.assertTrue(n.present_stem == 'am')
        self.assertTrue(n.perfect_stem == 'amav')
        self.assertTrue(n.supine_stem == 'amat')

    def test_stems_deponent(self):
        n = word_utils.make_word('verb', ['', 'loquī', 'locūtus sum', ''])
        self.assertTrue('deponent' in n.keywords)
        self.assertTrue(n.present_stem == 'loqu')
        self.assertTrue(n.perfect_stem == '')
        self.assertTrue(n.supine_stem == 'locūt')

    def test_stems_deponent_i_stem(self):
        n = word_utils.make_word('verb', ['patior', 'patī', 'passus sum', ''])
        self.assertTrue('deponent' in n.keywords)
        self.assertTrue('i-stem' in n.keywords)
        self.assertTrue(n.present_stem == 'pat')
        self.assertTrue(n.perfect_stem == '')
        self.assertTrue(n.supine_stem == 'pass')

    def test_deponent_inflections(self):
        n = word_utils.make_word('verb', ['patior', 'patī', 'passus sum', ''])
        for infl in n.inflections.keys():
            self.assertTrue(infl['voice'] == 'act')

    def test_no_passive(self):
        n = word_utils.make_word('verb', ['', 'valēre', 'valuī sum', 'valitum'], keywords="no-passive")
        for infl in n.inflections.keys():
            self.assertTrue(infl['voice'] == 'act')

