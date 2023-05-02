from verba.word.noun import Noun

def make_noun(ch='1', dec='1', ns='', stem='litter', gender='f', meaning='This is a Latin word', special=''):
    data = {
            'chapter': ch,
            'declension': dec,
            'nominative_singular': ns,
            'stem': stem,
            'gender': gender,
            'meaning': meaning,
            'special': special,
            }
    return Noun(data)
