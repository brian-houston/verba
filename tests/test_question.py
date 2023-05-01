import unittest
from verba.question.identify_generator import IdentifyGenerator

class TestQuestion(unittest.TestCase):
    def test_question(self):
        gen = IdentifyGenerator('noun', '', '')
        self.assertTrue(True)

