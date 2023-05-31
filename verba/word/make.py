from verba.word.noun import Noun
from verba.word.adjective import Adjective
from verba.word.other import Other
def make_word(data):
    if 'part_of_speech' not in data:
        return None
    if data['part_of_speech'] == 'noun':
        return Noun(data)
    if data['part_of_speech'] == 'adjective':
        return Adjective(data)

    return Other(data)
