import unittest
from verbae.word.noun import Noun
import verbae.word.endings as endings

class TestNoun(unittest.TestCase):
    def make_noun(ch='1', dec='1', ns='', stem='litter', gender='f', meaning='This is a Latin word', special=''):
        data = {
                'chapter': ch,
                'declension': dec,
                'nominative_singular': ns,
                'stem': stem,
                'gender': gender,
                'meaning': meaning,
                'special': special,
                }
        return Noun(data)

    def test_noun_is_noun(self):
        n = TestNoun.make_noun()
        self.assertTrue(n.part_of_speech == 'noun')

    def test_noun_chapter(self):
        n = TestNoun.make_noun(ch='5')
        self.assertTrue(n.chapter == 5)

    def test_noun_gender(self):
        n = TestNoun.make_noun(gender='m')
        self.assertTrue(n.gender == 'm')

    def test_noun_bad_gender(self):
        with self.assertRaises(ValueError):
            n = TestNoun.make_noun(gender='z')

    def test_noun_declension(self):
        n = TestNoun.make_noun(dec='2')
        self.assertTrue(n.declension == '2')

    def test_noun_bad_declension(self):
        with self.assertRaises(ValueError):
            n = TestNoun.make_noun(dec='8')

    # test 1st declension endings
    def test_noun_inflections_dec_1(self):
        n = TestNoun.make_noun(dec='1', gender='f', stem='litter')
        self.assertTrue(n.has_inflection('nom', 's'))
        self.assertTrue(n.get_inflection('nom', 's') == 'littera')
        self.assertTrue(n.get_inflection('acc', 's') == 'litteram')
        self.assertTrue(n.get_inflection('gen', 's') == 'litterae')
        self.assertTrue(n.get_inflection('dat', 's') == 'litterae')
        self.assertTrue(n.get_inflection('abl', 's') == 'litterā')
        self.assertTrue(n.get_inflection('nom', 'p') == 'litterae')
        self.assertTrue(n.get_inflection('acc', 'p') == 'litterās')
        self.assertTrue(n.get_inflection('gen', 'p') == 'litterārum')
        self.assertTrue(n.get_inflection('dat', 'p') == 'litterīs')
        self.assertTrue(n.get_inflection('abl', 'p') == 'litterīs')

    # test 2nd declension endings with different ending in the nominative singular
    def test_noun_inflections_dec_2_nom_s(self):
        n = TestNoun.make_noun(dec='2', gender='m', stem='vir', ns='vir')
        self.assertTrue(n.has_inflection('nom', 's'))
        self.assertTrue(n.get_inflection('nom', 's') == 'vir')
        self.assertTrue(n.get_inflection('acc', 's') == 'virum')
        self.assertTrue(n.get_inflection('gen', 's') == 'virī')
        self.assertTrue(n.get_inflection('dat', 's') == 'virō')
        self.assertTrue(n.get_inflection('abl', 's') == 'virō')
        self.assertTrue(n.get_inflection('nom', 'p') == 'virī')
        self.assertTrue(n.get_inflection('acc', 'p') == 'virōs')
        self.assertTrue(n.get_inflection('gen', 'p') == 'virōrum')
        self.assertTrue(n.get_inflection('dat', 'p') == 'virīs')
        self.assertTrue(n.get_inflection('abl', 'p') == 'virīs')

    # test plural only noun
    def test_noun_plural(self):
        n = TestNoun.make_noun(dec='2', gender='m', stem='liber', special="plural")
        self.assertFalse(n.has_inflection('nom', 's'))
        self.assertTrue(n.has_inflection('nom', 'p'))
        self.assertTrue(n.get_inflection('nom', 'p') == 'liberī')
