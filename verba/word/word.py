from verba.word.word_key import WordKey as WK

class Word:
    def __init__(self, data):
        self.data = data
        self.part_of_speech = data['part_of_speech']
        self.is_inflected = False
        self.chapter = int(data['chapter'])
        self.parts = [data['pp1'], data['pp2'], data['pp3'], data['pp4']]
        self.parts = [p.strip() for p in self.parts]
        self.keywords = set(data['keywords'].split())
        self.meaning = data['meaning']
        self.inflections = {}

    def _raise_error(reason, obj):
        raise ValueError(f'{reason}: {obj}')

    def _set_parts_as_inflections(self):
        for i, p in enumerate(self.parts):
            if p:
                self.inflections[WK(str(i+1))] = p
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
        return WK()

    """
    Apply certain keywords to filter a word's inflections
    Returns the filtered dictionary of inflections

    del-[WK]: delete all inflections whose keys contain WK
    delnot-[WK]: delete all inflections whose keys do not contain WK

    add-[WK]: add all inflections whose keys contain WK
    addnot-[WK]: add all inflections whose keys do not contain WK

    The 'add' keywords do nothing if nothing has been deleted.
    All inflections can be deleted with 'del-'
    """
    def apply_keywords(self):
        del_inflections = self.inflections
        add_inflections = {} 
        for kw in self.keywords:
            if kw.startswith('del-'):
                key = WK(*kw[4:].split('-'))
                del_inflections = {k:v for k, v in del_inflections.items() if not k.contains(key)}
            if kw.startswith('delnot-'):
                key = WK(*kw[7:].split('-'))
                del_inflections = {k:v for k, v in del_inflections.items() if k.contains(key)}

            if kw.startswith('add-'):
                key = WK(*kw[4:].split('-'))
                add_inflections |= {k:v for k, v in self.inflections.items() if k.contains(key)}
            if kw.startswith('addnot-'):
                key = WK(*kw[7:].split('-'))
                add_inflections |= {k:v for k, v in self.inflections.items() if not k.contains(key)}

        return del_inflections | add_inflections

    def __repr__(self):
        parts_str = ', '.join([p for p in self.parts if p])
        return f'{self.part_of_speech}: {parts_str}'

