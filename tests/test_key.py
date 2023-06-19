import unittest
from verba.word.word_key import WordKey as WK

class TestKey(unittest.TestCase):
    def test_duplicate_attributes(self):
        self.assertTrue(WK('s', 'p') == WK('p'))

    def test_equality(self):
        key1 = WK('nom', 's')
        key2 = WK('s', 'nom')
        self.assertTrue(key1 == key2)

    def test_union(self):
        key1 = WK('nom', 's')
        key2 = WK('f')
        key3 = WK('s', 'f', 'nom')
        self.assertTrue(key1.union(key2) == key3)

    def test_union_duplicates(self):
        key1 = WK('nom', 's')
        key2 = WK('f', 'p', '1')
        key3 = WK('1', 's', 'f', 'nom')
        self.assertTrue(key1.union(key2) == key3)

    def test_index(self):
        key1 = WK('nom', 's')
        self.assertTrue(key1['number'] == 's')
        self.assertTrue(key1['case'] == 'nom')
        self.assertTrue(key1['tense'] == None)

    def test_hash(self):
        key1 = WK('nom', 's')
        key2 = WK('s', 'nom')
        d = {key1: 4} 
        self.assertTrue(d[key2] == 4)

    def test_repr(self):
        key1 = WK('s', 'nom', 'f')
        self.assertTrue(repr(key1) == '(f, nom, s)')

    def test_filter(self):
        key1 = WK('s', 'nom', 'f', '1')
        key2 = WK('s')
        self.assertTrue(key1.filter(['number']) == key2)

    def test_contains(self):
        key1 = WK('s', 'nom', 'f', '1')
        key2 = WK()
        self.assertTrue(key1.contains(key2) == True)

        key1 = WK('s', 'nom', 'f', '1')
        key2 = WK('s', 'nom')
        self.assertTrue(key1.contains(key2) == True)

        key1 = WK('s', 'nom')
        key2 = WK('s', 'nom', 'f', '1')
        self.assertTrue(key1.contains(key2) == False)

        key1 = WK('s', 'nom')
        key2 = WK('p')
        self.assertTrue(key1.contains(key2) == False)
