from verba.word.word_key import WordKey as WK

class Word:
    def __init__(self, data):
        self.data = data
        self.part_of_speech = data['part_of_speech']
        self.chapter = int(data['chapter'])
        self.parts = [data['pp1'], data['pp2'], data['pp3'], data['pp4']]
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
