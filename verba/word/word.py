class Word:
    def __init__(self, part_of_speech, data):
        self.part_of_speech = part_of_speech
        self.meaning = data['meaning']
        self.chapter = int(data['chapter'])

    def get_pofs(self):
        return self.part_of_speech

