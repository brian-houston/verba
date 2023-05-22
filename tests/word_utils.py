from verba.word.noun import Noun

def make_noun(ch='1', dec='1', ns='', genitive='litterae', gender='f', meaning='This is a Latin word', keywords=''):
    data = {
            'part_of_speech': 'noun',
            'chapter': ch,
            'declension': dec,
            '1': ns,
            '2': genitive,
            '3': gender,
            'meaning': meaning,
            'keywords': keywords,
            }
    return Noun(data)
