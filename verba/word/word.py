from verba.word.inflection_key import InflectionKey as IK

class Word:
    def __init__(self, data):
        self.data = data
        self.part_of_speech = data['part_of_speech']
        self.is_inflected = False # subclass should set to True if inflected
        self.chapter = data['chapter']
        self.parts = [data['pp1'], data['pp2'], data['pp3'], data['pp4']]
        self.keywords = set(data['keywords'].replace(',', ' ').split())
        self.meaning = data['meaning']
        self.inflections = {}

        self.keywords.add(self.part_of_speech)

    def _raise_error(self, reason, obj):
        raise ValueError(f'{reason}: {obj}')

    def _set_parts_as_inflections(self):
        for i, p in enumerate(self.parts):
            if p:
                self.inflections[IK(str(i+1))] = p
            else:
                break

    def has_inflection(self, key):
        return key in self.inflections

    def get_inflection(self, key):
        return self.inflections[key]

    def get_inflection_keys(self):
        return self.inflections.keys()

    def get_keys_for_inflection(self, inflection):
        return [k for k, v in self.inflections.items() if v == inflection]

    def get_key(self):
        return IK()

    """
    Apply certain keywords to filter a word's inflections
    Returns the filtered dictionary of inflections

    del-[IK]: delete all inflections whose keys contain IK
    delnot-[IK]: delete all inflections whose keys do not contain IK

    add-[IK]: add all inflections whose keys contain IK
    addnot-[IK]: add all inflections whose keys do not contain IK

    The 'add' keywords do nothing if nothing has been deleted.
    All inflections can be deleted with 'del-'
    """
    def apply_keywords(self):
        del_inflections = self.inflections
        add_inflections = {} 
        for kw in self.keywords:
            if kw.startswith('del-'):
                key = IK(*kw[4:].split('-'))
                del_inflections = {k:v for k, v in del_inflections.items() if not k.contains(key)}
            if kw.startswith('delnot-'):
                key = IK(*kw[7:].split('-'))
                del_inflections = {k:v for k, v in del_inflections.items() if k.contains(key)}

            if kw.startswith('add-'):
                key = IK(*kw[4:].split('-'))
                add_inflections |= {k:v for k, v in self.inflections.items() if k.contains(key)}
            if kw.startswith('addnot-'):
                key = IK(*kw[7:].split('-'))
                add_inflections |= {k:v for k, v in self.inflections.items() if not k.contains(key)}

        return del_inflections | add_inflections

    def match_keywords(self, filter):
        for kw in filter:
            if kw not in self.keywords:
                return False
        return True

    def __repr__(self):
        parts_str = ', '.join([p for p in self.parts if p])
        return f'{self.part_of_speech}: {parts_str}'

