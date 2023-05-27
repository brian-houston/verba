import unittest
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK

class TestWord(unittest.TestCase):
    def test_part_of_speech(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''])
        self.assertTrue(n.part_of_speech == 'noun')
    
    def test_chapter(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''], ch='5')
        self.assertTrue(n.chapter == 5)

    def test_chapter(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''], meaning='letter')
        self.assertTrue(n.meaning == 'letter')

    def test_keywords(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''], keywords='test1 test2 test3')
        self.assertTrue('test1' in n.keywords)
        self.assertTrue('test2' in n.keywords)
        self.assertTrue('test3' in n.keywords)

