import unittest
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK

class TestOther(unittest.TestCase):
    def test_single(self):
        n = word_utils.make_word('conjunction', ['et', '', '', ''])
        self.assertTrue(n.get_inflection(WK('default', '1')) == 'et')

    def test_multiple(self):
        n = word_utils.make_word('conjunction', ['ā', 'ab', '', ''])
        self.assertTrue(n.get_inflection(WK('default', '1')) == 'ā')
        self.assertTrue(n.get_inflection(WK('default', '2')) == 'ab')

    def test_blanks(self):
        n = word_utils.make_word('conjunction', ['ā', '', '', 'ab'])
        self.assertTrue(n.get_inflection(WK('default', '1')) == 'ā')
        self.assertTrue(n.get_inflection(WK('default', '4')) == 'ab')

    def test_empty(self):
        with self.assertRaises(ValueError):
            n = word_utils.make_word('conjunction', ['', '', '', ''])
