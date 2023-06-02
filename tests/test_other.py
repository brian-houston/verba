import unittest
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK

class TestOther(unittest.TestCase):
    def test_single(self):
        n = word_utils.make_word('conjunction', ['et', '', '', ''])
        self.assertTrue(n.get_inflection(WK('1')) == 'et')

    def test_multiple(self):
        n = word_utils.make_word('conjunction', ['ā', 'ab', '', ''])
        self.assertTrue(n.get_inflection(WK('1')) == 'ā')
        self.assertTrue(n.get_inflection(WK('2')) == 'ab')

    def test_blanks(self):
        n = word_utils.make_word('conjunction', ['ā', '', '', 'ab'])
        self.assertTrue(n.get_inflection(WK('1')) == 'ā')
        self.assertFalse(n.has_inflection(WK('4')))
