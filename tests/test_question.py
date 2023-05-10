import unittest
from verba.question.identify_generator import IdentifyGenerator
import tests.word_utils as word_utils
import verba.word.definitions as definitions
from verba.word.word_key import WordKey as WK

class TestQuestion(unittest.TestCase):
    def test_id_question_invalid_part_of_speech(self):
        with self.assertRaises(ValueError):
            gen = IdentifyGenerator('whatever', ['gender', 'case', 'number'], '')

    def test_id_question_no_attributes(self):
        with self.assertRaises(ValueError):
            gen = IdentifyGenerator('noun', [], '')

    def test_id_question_invalid_attributes(self):
        with self.assertRaises(ValueError):
            gen = IdentifyGenerator('noun', ['color'], '')

    def test_id_question_check_answers(self):
        gen = IdentifyGenerator('noun', ['number', 'case'], [WK('nom', 'p')])
        n = word_utils.make_noun()
        question = next(gen.generate([n]))
        self.assertTrue(question.check_submissions(['nom p']) == 'partial')
        self.assertTrue(question.check_submissions(['s dat']) == 'partial')
        self.assertTrue(question.check_submissions(['gen s']) == 'correct')
        question = next(gen.generate([n]))
        self.assertTrue(question.check_submissions(['nom p']) == 'partial')
        self.assertTrue(question.check_submissions(['s dat']) == 'partial')
        self.assertTrue(question.check_submissions(['gen s']) == 'correct')
