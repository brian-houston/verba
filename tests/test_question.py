import unittest 
from verba.question.identify import identify_question_generator 
import tests.word_utils as word_utils
from verba.word.word_key import WordKey as WK

class TestQuestion(unittest.TestCase):
    def test_id_question_no_attributes(self):
        n = word_utils.make_noun()
        with self.assertRaises(ValueError):
            gen = identify_question_generator([n], [WK('nom', 'p')], [])
            next(gen)

    def test_id_question_invalid_attributes(self):
        n = word_utils.make_noun()
        with self.assertRaises(ValueError):
            gen = identify_question_generator([n], [WK('nom', 'p')], ['color'])
            next(gen)

    def test_id_question_check_answers(self):
        n = word_utils.make_noun()
        gen = identify_question_generator([n], [WK('nom', 'p')], ['number', 'case'])
        question = next(gen)
        self.assertTrue(question.check_submissions(['nom p']) == 'partial')
        self.assertTrue(question.check_submissions(['s dat']) == 'partial')
        self.assertTrue(question.check_submissions(['gen s']) == 'correct')
        question = next(gen)
        self.assertTrue(question.check_submissions(['nom p']) == 'partial')
        self.assertTrue(question.check_submissions(['s dat']) == 'partial')
        self.assertTrue(question.check_submissions(['gen s']) == 'correct')
