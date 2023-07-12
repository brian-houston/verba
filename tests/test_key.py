import unittest
from verba.word.inflection_key import InflectionKey as IK

class TestKey(unittest.TestCase):
    def test_duplicate_attributes(self):
        self.assertTrue(IK('s', 'p') == IK('p'))

    def test_equality(self):
        key1 = IK('nom', 's')
        key2 = IK('s', 'nom')
        self.assertTrue(key1 == key2)

    def test_union(self):
        key1 = IK('nom', 's')
        key2 = IK('f')
        key3 = IK('s', 'f', 'nom')
        self.assertTrue(key1.union(key2) == key3)

    def test_union_duplicates(self):
        key1 = IK('nom', 's')
        key2 = IK('f', 'p', '1')
        key3 = IK('1', 's', 'f', 'nom')
        self.assertTrue(key1.union(key2) == key3)

    def test_index(self):
        key1 = IK('nom', 's')
        self.assertTrue(key1['number'] == 's')
        self.assertTrue(key1['case'] == 'nom')
        self.assertTrue(key1['tense'] == None)

    def test_hash(self):
        key1 = IK('nom', 's')
        key2 = IK('s', 'nom')
        d = {key1: 4} 
        self.assertTrue(d[key2] == 4)

    def test_repr(self):
        key1 = IK('s', 'nom', 'f')
        self.assertTrue(repr(key1) == '(f, nom, s)')

    def test_filter(self):
        key1 = IK('s', 'nom', 'f', '1')
        key2 = IK('s')
        self.assertTrue(key1.filter(['number']) == key2)

    def test_contains(self):
        key1 = IK('s', 'nom', 'f', '1')
        key2 = IK()
        self.assertTrue(key1.contains(key2) == True)

        key1 = IK('s', 'nom', 'f', '1')
        key2 = IK('s', 'nom')
        self.assertTrue(key1.contains(key2) == True)

        key1 = IK('s', 'nom')
        key2 = IK('s', 'nom', 'f', '1')
        self.assertTrue(key1.contains(key2) == False)

        key1 = IK('s', 'nom')
        key2 = IK('p')
        self.assertTrue(key1.contains(key2) == False)
