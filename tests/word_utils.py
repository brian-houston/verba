from verba.word.noun import Noun

def make_noun(ch='1', dec='1', ns='', genitive='litterae', gender='f', meaning='This is a Latin word', special=''):
    data = {
            'chapter': ch,
            'declension': dec,
            'nominative_singular': ns,
            'genitive': genitive,
            'gender': gender,
            'meaning': meaning,
            'special': special,
            }
    return Noun(data)
