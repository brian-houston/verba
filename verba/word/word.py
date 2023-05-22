class Word:
    def __init__(self, data):
        self.part_of_speech = data['part_of_speech']
        self.meaning = data['meaning']
        self.chapter = int(data['chapter'])
        self.keywords = data['keywords'].split()
        self.inflections = {}
