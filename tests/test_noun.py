import unittest
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK

class TestNoun(unittest.TestCase):
    def test_gender(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''])
        self.assertTrue(n.gender == 'f')

    def test_bad_gender(self):
        with self.assertRaises(ValueError):
            n = word_utils.make_word('noun', ['', 'litterae', 'z', ''])

    def test_bad_genitive(self):
        with self.assertRaises(ValueError):
            n = word_utils.make_word('noun', ['', 'mille', 'f', ''])
        with self.assertRaises(ValueError):
            n = word_utils.make_word('noun', ['', 'res', 'f', ''])
        with self.assertRaises(ValueError):
            n = word_utils.make_word('noun', ['', 'rivus', 'f', ''])

    # test 1st declension endings
    def test_inflections_dec_1(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''])
        self.assertTrue(n.has_inflection(WK('nom', 's')))
        self.assertTrue(n.get_inflection(WK('nom', 's')) == 'littera')
        self.assertTrue(n.get_inflection(WK('acc', 's')) == 'litteram')
        self.assertTrue(n.get_inflection(WK('gen', 's')) == 'litterae')
        self.assertTrue(n.get_inflection(WK('dat', 's')) == 'litterae')
        self.assertTrue(n.get_inflection(WK('abl', 's')) == 'litterā')
        self.assertTrue(n.get_inflection(WK('nom', 'p')) == 'litterae')
        self.assertTrue(n.get_inflection(WK('acc', 'p')) == 'litterās')
        self.assertTrue(n.get_inflection(WK('gen', 'p')) == 'litterārum')
        self.assertTrue(n.get_inflection(WK('dat', 'p')) == 'litterīs')
        self.assertTrue(n.get_inflection(WK('abl', 'p')) == 'litterīs')

    # test 2nd declension endings with different ending in the nominative singular
    def test_inflections_nom_s(self):
        n = word_utils.make_word('noun', ['vir', 'virī', 'm', ''])
        self.assertTrue(n.has_inflection(WK('nom', 's')))
        self.assertTrue(n.get_inflection(WK('nom', 's')) == 'vir')

    # test plural only noun
    def test_plural(self):
        n = word_utils.make_word('noun', ['', 'liberōrum', 'm', ''], keywords='plural')
        self.assertFalse(n.has_inflection(WK('nom', 's')))
        self.assertTrue(n.has_inflection(WK('nom', 'p')))
        self.assertTrue(n.get_inflection(WK('nom', 'p')) == 'liberī')

    def test_inflections_keys(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''])
        keys = n.get_keys_for_inflection(n.get_inflection(WK('gen', 's')))
        self.assertTrue(WK('gen', 's') in keys)
        self.assertTrue(WK('dat', 's') in keys)
        self.assertTrue(WK('nom', 'p') in keys)

    def test_i_stem(self):
        n = word_utils.make_word('noun', ['animal', 'animalis', 'n', ''], keywords='i-stem')
        self.assertTrue(n.get_inflection(WK('nom', 'p')) == 'animalia')
        self.assertTrue(n.get_inflection(WK('acc', 'p')) == 'animalia')
        self.assertTrue(n.get_inflection(WK('abl', 's')) == 'animalī')

    def test_short_e(self):
        n = word_utils.make_word('noun', ['', 'reī', 'f', ''], keywords='short-e')
        self.assertTrue(n.get_inflection(WK('gen', 's')) == 'reī')
        self.assertTrue(n.get_inflection(WK('dat', 's')) == 'reī')

    def test_invariable(self):
        n = word_utils.make_word('noun', ['nihil', '', '', ''], keywords='invariable')
        self.assertTrue(n.get_inflection(WK('1')) == 'nihil')
