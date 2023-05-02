import unittest
from verba.question.identify_generator import IdentifyGenerator
import tests.word_utils as word_utils

class TestQuestion(unittest.TestCase):
    def test_question(self):
        gen = IdentifyGenerator('noun', '', '')
        word = word_utils.make_noun()
        questions = gen.generate(1, [word])
        questions[0].print_english()
        self.assertTrue(True)

