import verba.word.definitions as definitions

"""
Class used to index a word's inflections.
"""
class WordKey:
    def __init__(self, *args):
        self.attributes = {}
        for arg in args:
            if arg not in definitions.value_to_attribute:
                continue

            attr_name = definitions.value_to_attribute[arg]
            self.attributes[attr_name] = arg

    """
    Union the attributes of two keys together.
    If an attribute is present in both keys, the value for self takes precedence.

    Examples:
        WK('nom').union(WK('s')) = WK('nom', 's')
        WK('nom', 'p').union(WK('f', 's')) = WK('f', 'nom', 'p')
    """
    def union(self, other):
        return WordKey(*(other.attributes | self.attributes).values()) 

    """
    Create a new WordKey which only has the attributes given attr_names.

    Examples:
        WK('f', 'nom', 'p').filter('case') = WK('nom')
    """
    def filter(self, attr_names):
        return WordKey(*[v for k, v in self.attributes.items() if k in attr_names])

    """
    Return True if other's attributes match self's attributes.
    If self has attributes which other does not, they are ignored.

    Examples:
        WK('f', 'nom', 'p').contains(WK('nom', 'p')) = True
        WK('f', 'nom', 'p').contains(WK('nom', 's')) = False
    """
    def contains(self, other):
        return self.filter(other.attributes.keys()) == other

    def __repr__(self):
        attributes = [x for x in self.attributes.items() if x[0] in definitions.key_order]
        pairs = sorted(self.attributes.items(), key=lambda x: definitions.key_order.index(x[0]))
        values = [x[1] for x in pairs]
        values_str = ', '.join(values)
        return f'({values_str})'

    def __getitem__(self, i):
        if i not in self.attributes:
            return None

        return self.attributes[i]

    def __hash__(self):
        return hash(tuple(sorted(self.attributes)))

    def __eq__(self, other):
        if not isinstance(other, WordKey):
            return False
        return self.attributes == other.attributes



