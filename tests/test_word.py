import unittest
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK

class TestWord(unittest.TestCase):
    def test_part_of_speech(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''])
        self.assertTrue(n.part_of_speech == 'noun')
    
    def test_chapter(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''], ch='5')
        self.assertTrue(n.chapter == '5')
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''], ch='hello')
        self.assertTrue(n.chapter == 'hello')

    def test_meaning(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''], meaning='letter')
        self.assertTrue(n.meaning == 'letter')

    def test_keywords(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''], keywords='test1 test2 test3')
        self.assertTrue('test1' in n.keywords)
        self.assertTrue('test2' in n.keywords)
        self.assertTrue('test3' in n.keywords)

    def test_apply_keywords(self):
        n = word_utils.make_word('other', ['test', '', '', ''])
        n.inflections = {
                WK('pass', 's', '1st'): 'test1',
                WK('pass', 'p', '1st'): 'test1',
                WK('pass', 's', '2nd'): 'test1',
                WK('pass', 'p', '2nd'): 'test1',
                WK('act', 's', '1st'): 'test1',
                WK('act', 'p', '1st'): 'test1',
                WK('act', 's', '2nd'): 'test1',
                WK('act', 'p', '2nd'): 'test1',
                }
        
        n.keywords = set(['del-pass'])
        for k,v in n.apply_keywords().items():
            self.assertTrue(k.contains(WK('act')))

        n.keywords = set(['delnot-pass-1st'])
        for k,v in n.apply_keywords().items():
            self.assertTrue(k.contains(WK('pass', '1st')))

        n.keywords = set(['add-pass-s-1st', 'del-pass'])
        inflections = n.apply_keywords()
        self.assertTrue(WK('pass', 's', '1st') in inflections)
        self.assertFalse(WK('pass', 'p', '1st') in inflections)

        n.keywords = set(['addnot-pass-s-1st', 'del-pass'])
        inflections = n.apply_keywords()
        self.assertFalse(WK('pass', 's', '1st') in inflections)
        self.assertTrue(WK('pass', 'p', '1st') in inflections)

        n.keywords = set(['del-'])
        self.assertFalse(n.apply_keywords())
