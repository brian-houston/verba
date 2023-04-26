import unittest
from verbae.word.noun import Noun

class TestNoun(unittest.TestCase):
    def make_noun(ch='1', dec='1', ns='', stem='litter', gender='f', meaning='This is a Latin word', special=''):
        data = {
                'chapter': ch,
                'declension': dec,
                'nom_singular': ns,
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
        n = TestNoun.make_noun(dec='3')
        self.assertTrue(n.declension == '3')

    def test_noun_bad_declension(self):
        with self.assertRaises(ValueError):
            n = TestNoun.make_noun(dec='8')
