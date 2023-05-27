from verba.word.noun import Noun
from verba.word.other import Other
def make_word(data):
    if 'part_of_speech' not in data:
        return None
    if data['part_of_speech'] == 'noun':
        return Noun(data)

    return Other(data)
