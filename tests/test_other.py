import unittest
import tests.word_utils as word_utils
from verba.word.inflection_key import InflectionKey as IK

class TestOther(unittest.TestCase):
    def test_single(self):
        n = word_utils.make_word('conjunction', ['et', '', '', ''])
        self.assertTrue(n.get_inflection(IK('1')) == 'et')

    def test_multiple(self):
        n = word_utils.make_word('conjunction', ['ā', 'ab', '', ''])
        self.assertTrue(n.get_inflection(IK('1')) == 'ā')
        self.assertTrue(n.get_inflection(IK('2')) == 'ab')

    def test_blanks(self):
        n = word_utils.make_word('conjunction', ['ā', '', '', 'ab'])
        self.assertTrue(n.get_inflection(IK('1')) == 'ā')
        self.assertFalse(n.has_inflection(IK('4')))
