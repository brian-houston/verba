import unittest
import tests.word_utils as word_utils

class TestNoun(unittest.TestCase):
    def test_noun_is_noun(self):
        n = word_utils.make_noun()
        self.assertTrue(n.part_of_speech == 'noun')

    def test_noun_chapter(self):
        n = word_utils.make_noun(ch='5')
        self.assertTrue(n.chapter == 5)

    def test_noun_gender(self):
        n = word_utils.make_noun(gender='m')
        self.assertTrue(n.gender == 'm')

    def test_noun_bad_gender(self):
        with self.assertRaises(ValueError):
            n = word_utils.make_noun(gender='z')

    def test_noun_declension(self):
        n = word_utils.make_noun(dec='2')
        self.assertTrue(n.declension == '2')

    def test_noun_bad_declension(self):
        with self.assertRaises(ValueError):
            n = word_utils.make_noun(dec='8')

    # test 1st declension endings
    def test_noun_inflections_dec_1(self):
        n = word_utils.make_noun(dec='1', gender='f', stem='litter')
        self.assertTrue(n.has_inflection('nom-s'))
        self.assertTrue(n.get_inflection('nom-s')['word'] == 'littera')
        self.assertTrue(n.get_inflection('acc-s')['word'] == 'litteram')
        self.assertTrue(n.get_inflection('gen-s')['word'] == 'litterae')
        self.assertTrue(n.get_inflection('dat-s')['word'] == 'litterae')
        self.assertTrue(n.get_inflection('abl-s')['word'] == 'litterā')
        self.assertTrue(n.get_inflection('nom-p')['word'] == 'litterae')
        self.assertTrue(n.get_inflection('acc-p')['word'] == 'litterās')
        self.assertTrue(n.get_inflection('gen-p')['word'] == 'litterārum')
        self.assertTrue(n.get_inflection('dat-p')['word'] == 'litterīs')
        self.assertTrue(n.get_inflection('abl-p')['word'] == 'litterīs')

    # test 2nd declension endings with different ending in the nominative singular
    def test_noun_inflections_nom_s(self):
        n = word_utils.make_noun(dec='2', gender='m', stem='vir', ns='vir')
        self.assertTrue(n.has_inflection('nom-s'))
        self.assertTrue(n.get_inflection('nom-s')['word'] == 'vir')

    # test plural only noun
    def test_noun_plural(self):
        n = word_utils.make_noun(dec='2', gender='m', stem='liber', special="plural")
        self.assertFalse(n.has_inflection('nom-s'))
        self.assertTrue(n.has_inflection('nom-p'))
        self.assertTrue(n.get_inflection('nom-p')['word'] == 'liberī')

    def test_noun_inflections_keys(self):
        n = word_utils.make_noun(dec='1', gender='f', stem='litter')
        keys = n.get_inflection('gen-s')['keys']
        self.assertTrue('gen-s' in keys)
        self.assertTrue('dat-s' in keys)
        self.assertTrue('nom-p' in keys)

    def test_noun_inflections_gender(self):
        n = word_utils.make_noun(gender='m')
        keys = n.get_inflection('gen-s')['keys']
        self.assertTrue(n.get_inflection('gen-s')['gender'] == 'm')
