import unittest
from verba.question.identify_generator import IdentifyGenerator
import tests.word_utils as word_utils
import verba.word.definitions as definitions

class TestQuestion(unittest.TestCase):
    def test_question_invalid_part_of_speech(self):
        with self.assertRaises(ValueError):
            gen = IdentifyGenerator('whatever', '', ['gender', 'case', 'number'])

    def test_question_no_attributes(self):
        with self.assertRaises(ValueError):
            gen = IdentifyGenerator('noun', '', [])

    def test_question_invalid_attributes(self):
        with self.assertRaises(ValueError):
            gen = IdentifyGenerator('noun', '', ['tense'])

    def test_question_attributes_order(self):
        gen = IdentifyGenerator('noun', '', ['case', 'number', 'tense', 'gender'])
        self.assertTrue(gen.attributes == definitions.attribute_order['noun'])
