import unittest 
from verba.question.identify import identify_question_generator 
from verba.question.macron import macron_question_generator 
from verba.question.vocab import vocab_question_generator 
from verba.question.utils import inflection_generator
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK
test_keys = {
        'noun': [WK('nom', 'p')]
        }

class TestQuestion(unittest.TestCase):
    def test_id_question_check_answers(self):
        n = word_utils.make_word('noun', ['', 'litterae', 'f', ''])
        gen = identify_question_generator([n], test_keys, 'noun', ['number', 'case'])
        question = next(gen)
        self.assertTrue(question.check_submissions(['nom']) == 'wrong')
        self.assertTrue(question.check_submissions(['p']) == 'wrong')
        self.assertTrue(question.check_submissions(['afdkl']) == 'wrong')
        self.assertTrue(question.check_submissions(['nom p']) == 'partial')
        self.assertTrue(question.check_submissions(['s dat']) == 'partial')
        self.assertTrue(question.check_submissions(['gen s']) == 'correct')

        gen = identify_question_generator([n], test_keys, 'noun', ['number', 'case'])
        question = next(gen)
        self.assertTrue(question.check_submissions(['gen s', 's dat', 'nom p']) == 'correct')

    def test_macron_question_check_answers(self):
        n = word_utils.make_word('noun', ['', 'fēminae', 'f', ''])
        gen = macron_question_generator([n], test_keys)
        question = next(gen)
        self.assertTrue(question.check_submissions(['feminae']) == 'wrong')
        self.assertTrue(question.check_submissions(['fēminae']) == 'correct')

    def test_vocab_question_check_answers(self):
        n = word_utils.make_word('noun', ['', 'fēminae', 'f', ''])
        gen = vocab_question_generator([n], test_keys)
        question = next(gen)
        self.assertTrue(question.check_submissions(['whatever']) == 'answer')
        self.assertTrue(question.check_submissions(['whatever']) == 'wrong')
        self.assertTrue(question.check_submissions(['c']) == 'correct')

    def test_inflection_generator(self):
        n = word_utils.make_word('noun', ['', 'puellae', 'f', ''])
        gen = inflection_generator([n], test_keys)
        self.assertTrue(next(gen) == (n, WK('nom', 'p')))

    def test_inflection_generator_invariable(self):
        n = word_utils.make_word('noun', ['nihil', '', '', ''], keywords='invariable')
        gen = inflection_generator([n], test_keys)
        self.assertTrue(next(gen) == (n, WK('1')))

