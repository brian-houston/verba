import unittest
import tests.word_utils as word_utils
from verba.word.inflection_key import InflectionKey as IK

class TestAdjective(unittest.TestCase):
    def test_declension(self):
        n = word_utils.make_word('adjective', ['magnus', 'magna', 'magnum', ''])
        self.assertTrue(n.declension == '1/2')

        n = word_utils.make_word('adjective', ['', 'magna', '', ''])
        self.assertTrue(n.declension == '1/2')

        n = word_utils.make_word('adjective', ['brevis', 'brevis', 'breve', ''])
        self.assertTrue(n.declension == '3')
        n = word_utils.make_word('adjective', ['', 'brevis', '', ''])
        self.assertTrue(n.declension == '3')

        n = word_utils.make_word('adjective', ['atrōx', 'atrōx', 'atrōx', 'atrōcis'])
        self.assertTrue(n.declension == '3')

    def test_irregular_masculine(self):
        n = word_utils.make_word('adjective', ['pulcher', 'pulchra', 'pulchrum', ''])
        self.assertTrue(n.get_inflection(IK('pos', 'm', 'nom', 's')) == 'pulcher')

        n = word_utils.make_word('adjective', ['ācer', 'ācris', 'ācre', ''])
        self.assertTrue(n.get_inflection(IK('pos', 'm', 'nom', 's')) == 'ācer')

    def test_plural(self):
        n = word_utils.make_word('adjective', ['', 'pulchrae', '', ''])
        self.assertFalse(n.has_inflection(IK('pos', 'm', 'nom', 's')))
        self.assertTrue(n.get_inflection(IK('pos', 'f', 'nom', 'p')) == 'pulchrae')

    def test_irregular_neuter(self):
        n = word_utils.make_word('adjective', ['alius', 'alia', 'aliud', ''])
        self.assertTrue(n.declension == '1/2')
        self.assertTrue(n.get_inflection(IK('pos', 'n', 'nom', 's')) == 'aliud')
        self.assertTrue(n.get_inflection(IK('pos', 'n', 'acc', 's')) == 'aliud')

    def test_ius(self):
        n = word_utils.make_word('adjective', ['alter', 'altera', 'alterum', ''], keywords='ius')
        self.assertTrue(n.get_inflection(IK('pos', 'f', 'gen', 's')) == 'alterīus')
        self.assertTrue(n.get_inflection(IK('pos', 'm', 'gen', 's')) == 'alterīus')
        self.assertTrue(n.get_inflection(IK('pos', 'n', 'gen', 's')) == 'alterīus')

        self.assertTrue(n.get_inflection(IK('pos', 'f', 'dat', 's')) == 'alterī')
        self.assertTrue(n.get_inflection(IK('pos', 'm', 'dat', 's')) == 'alterī')
        self.assertTrue(n.get_inflection(IK('pos', 'n', 'dat', 's')) == 'alterī')

    def test_one_termination(self):
        n = word_utils.make_word('adjective', ['', 'atrōx', '', 'atrōcis'])
        self.assertTrue(n.get_inflection(IK('pos', 'f', 'nom', 's')) == 'atrōx')
        self.assertTrue(n.get_inflection(IK('pos', 'm', 'nom', 's')) == 'atrōx')
        self.assertTrue(n.get_inflection(IK('pos', 'n', 'nom', 's')) == 'atrōx')

    def test_ns(self):
        n = word_utils.make_word('adjective', ['', 'prudens', '', 'prudentis'])
        self.assertTrue('ns' in n.keywords)

