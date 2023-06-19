import unittest
from verba.generator_setup import translate_setting_input

class TestKey(unittest.TestCase):
    def test_translate_level(self):
        self.assertTrue(translate_setting_input('level', '3') == 3)
        self.assertTrue(translate_setting_input('level', 'a') == None)
        self.assertTrue(translate_setting_input('level', '-1') == -1)

    def test_translate_chapters(self):
        self.assertTrue(translate_setting_input('chapters', '1') == set(['1']))
        self.assertTrue(translate_setting_input('chapters', '1 2') == set(['1', '2']))
        self.assertTrue(translate_setting_input('chapters', '1,2') == set(['1', '2']))
        self.assertTrue(translate_setting_input('chapters', '1 ,  2') == set(['1', '2']))
        self.assertTrue(translate_setting_input('chapters', '1-4') == set(['1', '2', '3', '4']))
        self.assertTrue(translate_setting_input('chapters', '1-4,1, 5 hello') == set(['1', '2', '3', '4', '5', 'hello']))
        self.assertTrue(translate_setting_input('chapters', '') == None)
        self.assertTrue(translate_setting_input('chapters', 'a') == set(['a']))
        self.assertTrue(translate_setting_input('chapters', 'a-5') == None)

    def test_translate_filters(self):
        self.assertTrue(translate_setting_input('filters', '') == [[]]) 
        self.assertTrue(translate_setting_input('filters', 'noun') == [['noun']])
        self.assertTrue(translate_setting_input('filters', 'noun, verb') == [['noun'], ['verb']])
        self.assertTrue(translate_setting_input('filters', 'noun 3 plural') == [['noun', '3', 'plural']])
        self.assertTrue(translate_setting_input('filters', 'noun 3 plural, verb deponent 2') == [['noun', '3', 'plural'], ['verb', 'deponent', '2']])

    def test_translate_attributes(self):
        self.assertTrue(translate_setting_input('attributes', '') == None)
        self.assertTrue(translate_setting_input('attributes', 'noun') == None)
        self.assertTrue(translate_setting_input('attributes', 'noun:') == None)
        self.assertTrue(translate_setting_input('attributes', 'noun: case') == {'noun': ['case']})
        self.assertTrue(translate_setting_input('attributes', 'noun: case number') == {'noun': ['case', 'number']})
        self.assertTrue(translate_setting_input('attributes', 'noun: case number, verb: tense person') == 
                        {'noun': ['case', 'number'], 'verb': ['tense', 'person']})
        self.assertTrue(translate_setting_input('attributes', ' noun: case number,verb:tense   person  ') == 
                        {'noun': ['case', 'number'], 'verb': ['tense', 'person']})

