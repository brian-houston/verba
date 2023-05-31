from verba.word.word_key import WordKey as WK

class Word:
    def __init__(self, data):
        self.data = data
        self.part_of_speech = data['part_of_speech']
        self.meaning = data['meaning']
        self.chapter = int(data['chapter'])
        self.keywords = set(data['keywords'].split())
        self.inflections = {}

    def raise_error(reason, obj):
        raise ValueError(f'{reason}: {obj}')

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
