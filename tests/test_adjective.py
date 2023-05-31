import unittest
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK

class TestNoun(unittest.TestCase):
    def test_declension(self):
        n = word_utils.make_word('adjective', ['magnus', 'magna', 'magnum', ''])
        self.assertTrue(n.declension == '1|2')

        n = word_utils.make_word('adjective', ['brevis', 'breve', '', ''])
        self.assertTrue(n.declension == '3')

        n = word_utils.make_word('adjective', ['ācer', 'ācris', 'ācre', ''])
        self.assertTrue(n.declension == '3')

        n = word_utils.make_word('adjective', ['atrōx', 'atrōcis', '', ''])
        self.assertTrue(n.declension == '3')

    def test_irregular_masculine(self):
        n = word_utils.make_word('adjective', ['pulcher', 'pulchera', 'pulcherum', ''])
        self.assertTrue(n.get_inflection(WK('pos', 'm', 'nom', 's')) == 'pulcher')

        n = word_utils.make_word('adjective', ['ācer', 'ācris', 'ācre', ''])
        self.assertTrue(n.get_inflection(WK('pos', 'm', 'nom', 's')) == 'ācer')

    def test_ius(self):
        n = word_utils.make_word('adjective', ['alter', 'altera', 'alterum', ''], keywords='ius')
        self.assertTrue(n.get_inflection(WK('pos', 'f', 'gen', 's')) == 'alterīus')
        self.assertTrue(n.get_inflection(WK('pos', 'm', 'gen', 's')) == 'alterīus')
        self.assertTrue(n.get_inflection(WK('pos', 'n', 'gen', 's')) == 'alterīus')

        self.assertTrue(n.get_inflection(WK('pos', 'f', 'dat', 's')) == 'alterī')
        self.assertTrue(n.get_inflection(WK('pos', 'm', 'dat', 's')) == 'alterī')
        self.assertTrue(n.get_inflection(WK('pos', 'n', 'dat', 's')) == 'alterī')

    def test_one_termination(self):
        n = word_utils.make_word('adjective', ['atrōx', 'atrōcis', '', ''])
        self.assertTrue(n.get_inflection(WK('pos', 'f', 'nom', 's')) == 'atrōx')
        self.assertTrue(n.get_inflection(WK('pos', 'm', 'nom', 's')) == 'atrōx')
        self.assertTrue(n.get_inflection(WK('pos', 'n', 'nom', 's')) == 'atrōx')

